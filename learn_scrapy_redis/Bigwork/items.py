# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JOBItem(scrapy.Item):
    title = scrapy.Field() # 工作名称
    company = scrapy.Field() # 公司名称
    addr = scrapy.Field() # 工作位置
    exp = scrapy.Field() # 经验
    salaryMin = scrapy.Field() # 工资下限
    salaryMax = scrapy.Field() # 工资上限
    tags = scrapy.Field() # 标签
    date_pub = scrapy.Field() # 发布时间
    advantage = scrapy.Field() # 职位诱惑
    link = scrapy.Field() # 详情链接

    spider = scrapy.Field()  # 爬虫名称
    crawled = scrapy.Field() # 抓取时间
    jid = scrapy.Field() # 加密的 url  唯一


    # job_type = scrapy.Field() # 工作类型
    # degree = scrapy.Field() # 学历
    # location = scrapy.Field() # 城市
    # industry = scrapy.Field() # 工作职责
