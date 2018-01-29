# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import pymysql

class BigworkPipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item

class LagouPipeline(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect('127.0.0.1', 'root', 'asd19960321', 'my_spider', charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    def process_item(self,item,spider):
        item['spider'] = spider.name
        item["crawled"] = datetime.utcnow()
        self.insertInDatabase(item)
        return item

    def insertInDatabase(self,item):
        sql = "insert into jobs( jid, title, salaryMin, salaryMax, exp, tags, date_pub, advantage, addr , company , spider , crawled ,link) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = [item['jid'] ,item['title'] ,item['salaryMin'] ,item['salaryMax'] ,item['exp'] ,item['tags'] ,item['date_pub'] ,item['advantage'] ,item['addr'] ,item['company'],item['spider'],item['crawled'],item['link']]
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()