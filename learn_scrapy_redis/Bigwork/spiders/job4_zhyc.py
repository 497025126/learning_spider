# -*- coding:utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
import datetime
from datetime import timedelta
import hashlib
from Bigwork.items import JOBItem

class ZhycSpider(RedisCrawlSpider):
    name = 'hmr_zhyc'
    redis_key = 'hmr_zhyc'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 0.1,
        'ITEM_PIPELINES':{
            # 'Bigwork.pipelines.LagouPipeline': 300,# 直接存入mysql的管道
            'Bigwork.pipelines.BigworkPipeline': 300,# 输出至控制台的管道
            'scrapy_redis.pipelines.RedisPipeline': 888,# 把item存入redis 中如需取出存入mysql另写文件进行存取
        },
        'CONCURRENT_REQUESTS': 3,
    }

    rules = [
        Rule(LinkExtractor(allow=r'chinahr.com/jobs/'), follow=True),# 不同工作分类
        Rule(LinkExtractor(allow=r'chinahr.com/company/'), follow=True),# 进入公司页面
        # 详情页面 中华英才网中的详情页中还有其他职位的详情页链接 故follow可写True
        Rule(LinkExtractor(allow=r'chinahr.com/job/.*\.html'), follow=True,callback='parse_item',process_request='pr'),
    ]

    # setting中设置的是优先级队列  可在这里增加优先级
    def pr(self,request):
        request.priority = 1
        return request

    # 分析项目
    def parse_item(self, response):
        item = JOBItem()
        link = response.url  # 招聘链接
        jid = self.md5(link)  # 唯一链接

        try:
            title = response.xpath('//h1//span//text()').extract()[0]
        except:
            title = response.css('title::text').extract_first()
        salary = response.xpath('//div[@class="job_require"]//span[@class="job_price"]//text()').extract()[0]
        salary = self.salary_process(salary)
        salaryMin = salary[0]
        salaryMax = salary[1]
        exp = response.xpath('//div[@class="job_require"]//span//text()').extract()[-1]
        exp = self.exp_process(exp)
        # tags =

        date_pub = response.xpath('//p[@class="updatetime"]/text()').extract()[0]
        date_pub = self.date_pub_process(date_pub)
        advantage = ' '.join(response.xpath('//ul[@class="clear"]/li//text()').extract())
        company = response.xpath('//h4[1]/a/text()').extract()[0]
        addr = response.xpath('//div[@class="job_require"]/span/text()').extract()[1]

        # # 加载数据
        item['jid'] = jid
        item['title'] = title
        item['salaryMin'] = salaryMin
        item['salaryMax'] = salaryMax
        item['exp'] = exp
        # item['tags'] = tags
        item['date_pub'] = date_pub
        item['advantage'] = advantage
        item['company'] = company
        item['addr'] = addr
        item['link'] = link

        yield item

    # 处理页面中的发布日期  统一处理为类似 2018-01-25 的格式
    def date_pub_process(self,temp):
        if '今' in temp:
            res = datetime.datetime.now().strftime('%Y-%m-%d')
        elif '昨' in temp:
            days = timedelta(days=1)
            res = datetime.datetime.now() - days
            res = res.strftime('%Y-%m-%d')
        elif '前' in temp:
            days = timedelta(days=2)
            res = datetime.datetime.now() - days
            res = res.strftime('%Y-%m-%d')
        elif '2' in temp:
            res = temp.strip('更新')
        else:
            res = datetime.datetime.now().strftime('%Y-%m-%d')
        return res

    # 工作经验处理 1到3年 -> 1,3  三年以上-> 3
    def exp_process(self,temp):
        if '应届' in temp:
            res = '0'
        elif '在读' in temp:
            res = '0'
        elif '经验' in temp:
            res = temp.strip('经验年')
        else:
            res = '0'
        return res

    # 工资处理 结果为列表['工资下限','工资上限']
    def salary_process(self,temp):
        if '-' in temp:
            res = temp.split('-')
        else:
            res = ['0', '0']
        return res

    # 给url连接用md5加密存入数据后中 并对其设置唯一索引 使用BTREE
    # 保证数据库中的招聘信息不重复(有些公司同一职位发布多个招聘链接,暂时没有解决这个问题)
    def md5(self, value):
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()



