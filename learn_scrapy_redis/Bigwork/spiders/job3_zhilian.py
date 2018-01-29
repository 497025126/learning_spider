# -*- coding:utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
import hashlib
from Bigwork.items import JOBItem


class ZhilianSpider(RedisCrawlSpider):
    name = 'hmr_zhilian'
    redis_key = 'hmr_zhilian'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 0.2,
        'ITEM_PIPELINES':{
            # 'Bigwork.pipelines.LagouPipeline': 300,# 直接存入mysql的管道
            'Bigwork.pipelines.BigworkPipeline': 300,# 输出至控制台的管道
            'scrapy_redis.pipelines.RedisPipeline': 888,# 把item存入redis 中如需取出存入mysql另写文件进行存取
        },
        'CONCURRENT_REQUESTS': 2,
    }
    # http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&in=210500%3b160400%3b160000&jl=%E5%8C%97%E4%BA%AC&isadv=0&sg=ff240ed253994eb98665ff9b1250065f&p=1
    rules = [
        # 工作条件页面中 各个岗位爬取 以及分页都在此抓取
        Rule(LinkExtractor(allow=r'sou.zhaopin.com/jobs/searchresult.*'), follow=True),
        # 公司页面
        Rule(LinkExtractor(allow=r'company.zhaopin.com/.*'), follow=True),
        # 详情页
        Rule(LinkExtractor(allow=r'jobs.zhaopin.com/.*\.htm$'), follow=True, callback='parse_item',process_request='pr'),
    ]

    # 优先队列
    def pr(self,request):
        request.priority = 1
        return request

    # 解析项目
    def parse_item(self, response):
        item = JOBItem()

        link = response.url # 招聘链接
        jid = response.url
        jid = self.md5(jid) # 唯一链接

        title = response.xpath('//h1/text()').extract()[0]  # 工作名称
        company = response.xpath('//h2/a/text()').extract()[0]  # 公司名称
        addr = response.xpath('//h2/text()').extract()[0].strip() # 工作位置

        exp = response.xpath('//ul[@class="terminal-ul clearfix"]/li[5]//text()').extract()[1]  # 经验
        exp = self.exp_modify(exp)

        salary = response.xpath('//ul[@class="terminal-ul clearfix"]/li[1]//text()').extract()[1] # 工资
        salary = self.salary_process(salary)
        salaryMin = salary[0]
        salaryMax = salary[1]
        # tags = response.xpath()  # 标签
        tags = '互联网'
        date_pub = response.xpath('//ul[@class="terminal-ul clearfix"]/li[3]//text()').extract()[-1].split(' ')[0] # 发布时间
        if '00' in date_pub:
            date_pub = '2018-01-01'
        advantage = ' '.join(response.xpath('//div[@class="inner-left fl"]/div/span/text()').extract())  # 职位诱惑

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

    # 工资处理
    def salary_process(self,temp):
        if '面' in temp:
            res = ['0','0']
        elif ('-' in temp) and ('\xa0' in temp):
            res = temp.replace('元/月\xa0', '').split('-')
        else:
            res = ['0','0']
        return res

    # 工作经验处理
    def exp_modify(self, temp):
        if '不' in temp or '无' in temp or '以下' in temp:
            res = '0'
        elif '以上' in temp:
            res = '10'
        elif '年' in temp:
            res = temp.strip('年').replace('-', ',')
        else:
            res = '0'
        return res

    # 给url做个md5加密 再设置唯一索引  进一步防止抓取重复信息写入数据库
    def md5(self, value):
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()