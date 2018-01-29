# -*- coding:utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
import datetime
from datetime import timedelta
import hashlib
from Bigwork.items import JOBItem

class ZhycSpider(RedisCrawlSpider):
    name = 'hmr_58'
    redis_key = 'hmr_58'
    custom_settings = {
        'COOKIES_ENABLED': False, # 浏览过程是否设置cookie
        'DOWNLOAD_DELAY': 0.1,
        'ITEM_PIPELINES':{
            # 'Bigwork.pipelines.LagouPipeline': 300,# 直接存入mysql的管道
            'Bigwork.pipelines.BigworkPipeline': 300,# 输出至控制台的管道
            'scrapy_redis.pipelines.RedisPipeline': 888,# 把item存入redis 中如需取出存入mysql另写文件进行存取
        },
        'CONCURRENT_REQUESTS': 3, # 并发数
    }
    rules = [
        Rule(LinkExtractor(allow=r'.58.com/job.shtml'), follow=True),  # city
        Rule(LinkExtractor(allow=r'qy.58.com'), follow=True),  # company
        Rule(LinkExtractor(allow=r'/\w+/$', deny=(r'/zi/', r'zshenglan', r'zhaopinhui')), follow=True),  # job_list
        Rule(LinkExtractor(allow=r'pn\d+'), follow=True), # page
        Rule(LinkExtractor(allow=r'com/jump'), follow=True, callback='parse_item', process_request='pr'),  # detail_page
        Rule(LinkExtractor(allow=r'gz.*\d+x\.shtml', deny=(r'404\.html',r'ktv',r'pet', r'zufang', r'hezu', r'fanchan', r'fan', r'cat', r'dog')),follow=True, callback='parse_item', process_request='pr'),
    ]

    # 优先级队列  遇到详情页直接解析
    def pr(self,request):
        request.priority = 1
        return request

    # 解析项目
    def parse_item(self, response):
        item = JOBItem()
        link = response.url  # 招聘链接
        jid = self.md5(link)  # 唯一链接
        title = response.xpath('//div[@class="pos_base_info"]/span/text()').extract()[0]
        salary = response.xpath('//div[@class="pos_base_info"]/span/text()').extract()[1]
        salary = self.salary_process(salary)
        salaryMin = salary[0]
        salaryMax = salary[1]
        exp = self.exp_process(response.xpath('//div[@class="pos_base_condition"]/span[3]/text()').extract()[0].strip())
        tags = response.xpath('//a[@class="comp_baseInfo_link"]/text()').extract()[0]
        date_pub = self.date_pub_process(''.join(response.xpath('//div[@class="pos_base_statistics"]/span[1]/span//text()').extract()).replace(' ',''))
        advantage = ' '.join(response.xpath('//div[@class="pos_welfare"]/span/text()').extract())
        company = response.xpath('//div[@class="baseInfo_link"]//text()').extract()[0]
        addr = response.xpath('//div[@class="pos-area"]/span[2]/text()').extract()[0]

        # # 加载数据
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
        if ('小时' in temp) or ('今' in temp):
            # days = timedelta(days=2)
            res = datetime.datetime.now()
            res = res.strftime('%Y-%m-%d')
        elif '天前' in temp:
            days = int(temp.strip('天前'))
            days = timedelta(days=days)
            res = datetime.datetime.now() - days
            res = res.strftime('%Y-%m-%d')
        else:
            res = datetime.datetime.now()
            res = res.strftime('%Y-%m-%d')
        return res

    # 工作经验处理 1到3年 -> 1,3  三年以上-> 3
    def exp_process(self,temp):
        if ('不' in temp) or ('下' in temp) or ('应' in temp):
            res = '0'
        elif '-' in temp :
            res = temp.strip('年').replace('-',',')
        elif '上' in temp:
            res = '10'
        else:
            res = '0'
        return res

    # 工资处理 结果为列表['工资下限','工资上限']
    def salary_process(self,temp):
        if '面' in temp:
            res = ['0','0']
        elif '-' in temp :
            res = temp.split('-')
        else:
            res = ['0','0']
        return res

    # 给url连接用md5加密存入数据后中 并对其设置唯一索引 使用BTREE
    # 保证数据库中的招聘信息不重复(有些公司同一职位发布多个招聘链接,暂时没有解决这个问题)
    def md5(self, value):
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()



