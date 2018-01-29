# -*- coding:utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
import datetime
from datetime import timedelta
import hashlib
from Bigwork.items import JOBItem

class Lagou2Spider(RedisCrawlSpider):
    name = 'hmr_lagou'
    redis_key = 'hmr_lagou'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 0.1,
        # 拉勾有时会让登陆 ，用自己的账号登陆后查看 www.lagou.com 中的请求头中cookie值
        'DEFAULT_REQUEST_HEADERS': {
            "Host": "www.lagou.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "",
        },
        'ITEM_PIPELINES':{
            'Bigwork.pipelines.LagouPipeline': 300, # 直接存入数据库  不把item存入redis
            # 'scrapy_redis.pipelines.RedisPipeline': 999,
        },
        'CONCURRENT_REQUESTS':3,
    }
    rules = [
        # 招聘类别
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        # 公司
        Rule(LinkExtractor(allow=r'gongsi/'), follow=True),
        # 校招
        Rule(LinkExtractor(allow=r'xiaoyuan\.lagou\.com'), follow=True),
        # 工作详情页
        Rule(LinkExtractor(allow=r'jobs/\d+\.html'), follow=False, callback='parse_item',process_request='pr'),
    ]

    # 详情页优先解析
    def pr(self,request):
        request.priority = 1
        return request

    # item解析
    def parse_item(self, response):
        item = JOBItem()

        # 招聘详情链接
        link = response.url

        # 加密URL
        jid = response.url
        jid = self.md5(jid)

        # 职位名称  工资  工作经验  标签
        title = response.xpath('//span[@class="name"]/text()').extract()[0]
        salary = response.xpath('//span[@class="salary"]/text()').extract()[0]
        salary = self.salary_process(salary)
        salaryMin = salary[0]
        salaryMax = salary[1]

        exp = response.xpath('//dd[@class="job_request"]/p/span[3]/text()').extract()[0]
        exp = self.exp_peocess(exp)
        tags = response.xpath('//ul[@class="position-label clearfix"]/li/text()').extract()
        tags = ','.join(tags)

        # 发布日期
        date_pub = response.xpath('//p[@class="publish_time"]/text()').extract()[0]
        date_pub = self.process_date(date_pub)

        advantage = response.xpath('//dd[@class="job-advantage"]/p/text()').extract()[0]

        # 公司地址
        addr = response.xpath('//div[@class="work_addr"]/a/text()').extract()[:-1]
        addr = ''.join(addr)
        # 公司名称
        company = response.xpath('//h2[@class="fl"]/text()').extract()[0].strip()

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

    # 拉勾的工资都是 9K-20K 类似的处理
    def salary_process(self,value):
        # 工资有大小写K
        try:
            res = ','.join([str(int(float(i) * 1000)) for i in value.replace('k', '').strip().split('-')])
            res = res.split(',')
        except:
            res = ','.join([str(int(float(i) * 1000)) for i in value.replace('K', '').strip().split('-')])
            res = res.split(',')
        return res

    # 工作经验处理
    def exp_peocess(self, value):
        res = value.replace('/', '').replace('经验','')
        if ('不限' in res) or ('应届' in res) or ('以下'in res):
            res = '0'
        elif '年' in res:
            res = res.replace('-',',').replace('年','')
        elif '以上' in res :
            res = '10'
        else:
            res = '0'
        return res

    # 发布日期处理 这里引用时间函数
    def process_date(self, value):
        value = value.replace('\xa0', '').strip(' 发布于拉勾网')
        if '天前' in value:
            days = int(value.strip('天前'))
            days = timedelta(days=days)
            res = datetime.datetime.now() - days
            res = res.strftime('%Y-%m-%d')
        elif ':' in value:
            res = datetime.datetime.now().strftime('%Y-%m-%d')
        else:
            res = value

        return res

    # 唯一加密
    def md5(self, value):
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()



