# -*- coding:utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
import hashlib
from Bigwork.items import JOBItem

class Job51Spider(RedisCrawlSpider):
    name = 'hmr_job51'
    redis_key = 'hmr_job51'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 0.1,
        # 51不写请求头也可以 没有限制
        'DEFAULT_REQUEST_HEADERS': {
            "Cache-Control":"max-age=0",
            "Host": "search.51job.com",
            "Content-Type":"application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Origin":"http://search.51job.com",
            "Referer":"http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000&industrytype=32&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9",
            "Cookie": "user_trace_token=20180109204022-f1c36a3b-ec02-4059-b48d-09f6537fce3b; _ga=GA1.2.933628312.1515501607; LGUID=20180109204022-42635eab-f53a-11e7-a022-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; isCloseNotice=0; _gid=GA1.2.1119532081.1516602051; JSESSIONID=ABAAABAAAFCAAEGFB16AD6E4D3AFF29F55BE4ACAF0D9824; SEARCH_ID=9c2b9eb81fe04d44b35753c5618467ce; X_HTTP_TOKEN=35f80923f0968008439a204bd2b82605; ab_test_random_num=0; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516708383,1516708403,1516710032,1516711302; LGSID=20180123204204-d0ccf6b8-003a-11e8-bd38-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00f7Ghk60yUKm0FNkUs0pchIp00000PW4pNb00000XRRNRW.THL0oUhY1x60UWY4rj0knW03r7tdgvwM0ZnqmhDdPW6dPjcsnj0YrAcLmsKd5R7arRuAfYnsnYfzrRDvf1bznW9afbFDwbuKfRFjwW0s0ADqI1YhUyPGujY1njn1nW0dn10YFMKzUvwGujYkP6K-5y9YIZK1rBtEILILQhk9uvqdQhPEUitOIgwVgLPEIgFWuHdVgvPhgvPsI7qBmy-bINqsmsKWThnqPHfsnjn%26tpl%3Dtpl_10085_15730_11224%26l%3D1500117464%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E3%252580%252591%2525E5%2525AE%252598%2525E7%2525BD%252591-%2525E4%2525B8%252593%2525E6%2525B3%2525A8%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E8%252581%25258C%2525E4%2525B8%25259A%2525E6%25259C%2525BA%2526xp%253Did%28%252522m6c247d9c%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D220%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26issp%3D1%26f%3D8%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3D98012088_5_dg%26ch%3D3%26oq%3D%2525E5%252592%252596%2525E7%25258B%252597%2525E7%2525BD%252591%26inputT%3D17048; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; LGRID=20180123204209-d3fb8296-003a-11e8-bd38-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516711308",
        },
        'ITEM_PIPELINES':{
            'Bigwork.pipelines.BigworkPipeline': 300,# 输出至控制台的管道
            'scrapy_redis.pipelines.RedisPipeline': 888,# 把item存入redis 中如需取出存入mysql另写文件进行存取
        },
        'CONCURRENT_REQUESTS': 4,
    }
    # http://jobs.51job.com/beijing-hdq/66212646.html?s=01&t=0
    rules = [
        Rule(LinkExtractor(allow=r'search.51job.com/list/.*'), follow=True),
        Rule(LinkExtractor(allow=r'jobs.51job.com/.*\.html$'), follow=True),
        Rule(LinkExtractor(allow=r'jobs.51job.com/.*\.html?.*'), follow=False,callback='parse_item',process_request='pr'),
    ]

    # 详情页优先访问
    def pr(self,request):
        request.priority = 1
        return request

    # 解析项目
    def parse_item(self, response):
        item = JOBItem()

        link = response.url # 招聘链接
        jid = response.url
        jid = self.md5(jid) # 唯一链接

        title = response.xpath('//h1/text()').extract()[0] # 工作名称
        company = response.xpath('//p/a/@title').extract()[0]  # 公司名称

        # 工作位置  目前 360的是没有 ..
        addr = response.xpath("//p[@class='fp']/text()").extract()[-1].strip()
        exp = response.xpath('//div[@class="t1"]/span[1]/text()').extract()[0]
        exp = self.exp_modify(exp) # 经验
        # 工资 360 还是有的有有的没  ..
        try:
            salary = response.xpath('//div[@class="cn"]/strong/text()').extract()[0].strip('/月')  # 工资
            salary = self.salary_modify(salary)
            salaryMin = salary[0]
            salaryMax = salary[1]
        except:
            salaryMin = 0
            salaryMax = 0

        tags = response.xpath('//p[@class="msg ltype"]/text()').extract()[0].replace('\t','').split('|')[-1].strip().replace('/',',') # 标签
        date_pub = '2018-'+ [i.replace('发布','') for i in response.xpath('//div[@class="t1"]/span/text()').extract() if '发布' in i ][0]  # 发布时间
        advantage = ' '.join(response.xpath('//p[@class="t2"]/span/text()').extract()) # 职位诱惑

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

    # 工资处理
    def salary_modify(self,temp):
        res = ''
        if '以上' in temp:
            res = str(int(temp.strip('万以上')) * 10000)+','+str(int(temp.strip('万以上')) * 10000)
        elif '万' in temp:
            res = ','.join([str(int(j)) for j in [float(i) * 10000 for i in temp.strip('万').split('-')]])
        elif '千' in temp:
            res = ','.join([str(int(j)) for j in [float(i) * 1000 for i in temp.strip('千').split('-')]])
        elif '以下' in temp:
            if '千' in temp:
                res = str(int(temp.strip('千以下')) * 1000) + ',' + str(int(temp.strip('千以下')) * 1000)
            elif '万' in temp:
                res = str(int(temp.strip('万以上')) * 10000) + ',' + str(int(temp.strip('万以上')) * 10000)
        return res.split(',')

    # 工作经验处理
    def exp_modify(self,temp):
        res = ''
        if '以上' in temp:
            res = '10'
        elif '以下' in temp:
            res = '0'
        elif '年' in temp:
            res = temp.strip('年经验').replace('-',',')
        elif '无' in temp or '不' in temp:
            res = '0'
        else:
            res = '0'
        return res

    # 给url进行加密唯一值处理，在数据库设置唯一索引防止重复
    def md5(self, value):
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()



