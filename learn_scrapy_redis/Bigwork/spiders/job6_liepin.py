# -*- coding:utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
import datetime
from datetime import timedelta
import hashlib
from Bigwork.items import JOBItem

class ZhycSpider(RedisCrawlSpider):
    name = 'hmr_liepin'
    redis_key = 'hmr_liepin'
    custom_settings = {
        'COOKIES_ENABLED': False, # 是否设置COOKIE
        'DOWNLOAD_DELAY': 0.1,
        # 管道选择
        'ITEM_PIPELINES':{
            # 'Bigwork.pipelines.LagouPipeline': 300, # 该管道直接存储mysql数据库
            'Bigwork.pipelines.BigworkPipeline': 300, # 该管道把item提交到控制台输出
            # 该管道把item 提交到redis 缓存中 如需从redis缓存中 需执行另一个文件 save2mysql
            'scrapy_redis.pipelines.RedisPipeline': 888,
        },
        'CONCURRENT_REQUESTS': 3,# 并发数
    }

    rules = [
        Rule(LinkExtractor(allow=r'/company/'), follow=True),  # company
        Rule(LinkExtractor(allow=r'curPage=\d+'), follow=True),  # 分页的链接
        Rule(LinkExtractor(allow=r'leipin.com/job/'), follow=True, callback='parse_item',process_request='pr'),
    ]

    # 优先解析详情页面
    def pr(self,request):
        request.priority = 1
        return request

    # 解析各个数据
    def parse_item(self, response):
        item = JOBItem()
        link = response.url  # 招聘链接
        jid = self.md5(link)  # 唯一链接
        title = response.xpath('//h1/text() | //div[@class="flexbox baseinfo-top"]/span/text()').extract()[0]
        salary = response.xpath('//div[@class="job-title-left"]/p[1]//text() | //div[@class="job-main-title"]/strong/text()').extract()[0].strip()
        salary = self.salary_process(salary)
        salaryMin = salary[0]
        salaryMax = salary[1]
        exp = self.exp_process(response.xpath('//div[@class="resume clearfix"]/span[2]/text() | //p[@class="job-qualifications"]/span[1]/text() | //div[@class="job-qualifications"]/span[2]/text()').extract()[0].strip())
        try:
            tags = response.xpath('//div[@class="content content-word"]/ul/li[3]/a/@title').extract()[0]
        except:
            tags = title
        date_pub = response.xpath('//p[@class="basic-infor"]/time//text() | //p[@class="job-main-tip"]/span[2]//text()').extract()[0]
        date_pub = self.date_pub_process(date_pub)
        # print(exp)
        try:
            advantage = ' '.join(response.xpath('//div[@class="tag-list"]/span//text()').extract())
        except:
            advantage = ''
        try:
            company = response.xpath('//div[@class="title-info"]//h3/a/text()').extract()[0].strip()
        except:
            company =  response.xpath('//div[@class="title-info"]/h3/text()').extract()[0].strip()

        addr = response.xpath('//ul[@class="new-compintro"]/li[3]//text() | //div[@class="side-content"]/p/text()').extract()[0].strip().strip('公司地址：')
        # 加载数据
        item['jid'] = jid
        item['title'] = title
        item['salaryMin'] = salaryMin
        item['salaryMax'] = salaryMax
        item['exp'] = exp
        item['tags'] = tags
        item['date_pub'] = date_pub
        item['advantage'] = advantage
        item['company'] = company
        item['addr'] = addr
        item['link'] = link

        yield item
    # 处理页面中的发布日期  统一处理为类似 2018-01-25 的格式
    def date_pub_process(self,temp):
        if '-' in temp:
            res = temp.strip()
        elif '小时' in temp:
            res = datetime.datetime.now().strftime('%Y-%m-%d')
        elif '分钟' in temp:
            res = datetime.datetime.now().strftime('%Y-%m-%d')
        elif '昨' in temp:
            res = datetime.datetime.now() - timedelta(days=1)
            res = res.strftime('%Y-%m-%d')
        elif '昨' in temp:
            res = datetime.datetime.now() - timedelta(days=2)
            res = res.strftime('%Y-%m-%d')
        else:
            res = datetime.datetime.now().strftime('%Y-%m-%d')
        return res

    # 工作经验处理 1到3年 -> 1,3  三年以上-> 3
    def exp_process(self,temp):
        if '年以上' in temp:
            res = temp.strip('年以上')
        elif '不限' in temp:
            res = '0'
        else:
            res = '0'
        return res

    # 猎聘网的工资都是年薪 结果为列表['工资下限','工资上限']
    def salary_process(self,temp):
        if '面' in temp:
            res = ['0','0']
        elif '万' in temp:
            res = [int(10000 * float(('%.1f' % (int(i) / 12)))) for i in temp.strip('万').split('-')]
        else:
            res = ['0','0']
        return res

    # 给url连接用md5加密存入数据后中 并对其设置唯一索引 使用BTREE
    # 保证数据库中的招聘信息不重复(有些公司同一职位发布多个招聘链接,暂时没有解决这个问题)
    def md5(self, value):
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()