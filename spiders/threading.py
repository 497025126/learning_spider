# -*- coding:utf-8 -*-
"""
多线程爬取糗事百科 每个页面的信息
"""
from queue import Queue
import threading,random
import requests,json
from lxml import etree

# 全局变量  线程数量 方便修改
Max_Threading = 4

# 爬取类
class Crawl(threading.Thread):
    # 代理ip
    proxies = [
        {"host": "61.155.164.111", "port": "3128"},
        {"host": "122.72.18.34", "port": "80"}
    ]

    def __init__(self,i,request_que,data_que):
        # 继承父类
        super(Crawl, self).__init__()
        self.i = i
        self.request_que = request_que
        self.data_que = data_que

    def run(self):
        # 请求队列非空
        while not self.request_que.empty():
            url = self.request_que.get()
            print("%d 号线程开启采集 %s" % (self.i,url))
            temp = random.choice(self.proxies)
            proxy = {
                'http': 'http://{}:{}'.format(temp['host'],temp['port']),
                'https': 'http://{}:{}'.format(temp['host'], temp['port'])
            }
            response = requests.get(url=url,proxies = proxy)
            if 200 <= response.status_code <= 300:
                html = response.text
                self.data_que.put(html)
            else:
                print('响应错误')

class Parse(threading.Thread):
    def __init__(self,i,data_queue,thread_list,f):
        super(Parse, self).__init__()
        self.number = i
        self.data_queue = data_que
        self.thread_list = thread_list
        self.f = f
        self.is_parse = True # 一个判断标志

    def run(self):
        while True:
            # for else 语句  如果当前线程在执行 跳出for 循环 进行之后的解析代码
            for temp in self.thread_list:
                if temp.is_alive():
                    break
            else:
                if self.data_queue.qsize() == 0:
                    self.is_parse = False
            if self.is_parse:
                try:
                    html = self.data_queue.get(timeout=3)
                    # 调用解析函数
                    self.parse(html)
                except Exception as e:
                    pass
            else:
                break
        print("%d 号线程开启解析完毕" % self.number)

    def parse(self,html):
        html = etree.HTML(html)
        dzs_div = html.xpath('//div[@id="content-left"]/div')
        for dz in dzs_div:
            nick_name = dz.xpath('.//h2/text()')[0].strip()
            age = dz.xpath(
                './/div[@class="articleGender manIcon"]/text() | .//div[@class="articleGender womenIcon"]/text()')
            if age:
                age = age[0]
            else:
                aeg = 0
            gender = dz.xpath('.//div[@class="content"]/span/text()')
            if gender:
                if "man" in gender[0]:
                    gender = "男"
                elif "women" in gender[0]:
                    gender = "女"
            else:
                gender = "MID"

            content = dz.xpath('.//div[@class="content"]/span/text()')
            content = ''.join(content).strip()

            stars = dz.xpath('.//span[@class="stats-vote"]/i/text()')[0]
            comments = dz.xpath('.//span[@class="stats-comments"]//i/text()')[0]

            data = {
                'nick': nick_name,
                'age': age,
                'gender': gender,
                'content': content,
                'starts': stars,
                'comments': comments
            }

            duanzi_img = dz.xpath('//div[@class="thumb"]//img/@src')
            if duanzi_img:  # 段子有图片
                duanzi_img = duanzi_img[0]

                duanzi_img = 'https:' + duanzi_img
                fname = duanzi_img.split('/')[-1]
                file = open('./image/' + fname, 'wb')
                pic_bytes = requests.get(url=duanzi_img)
                file.write(pic_bytes.content)
                # request.urlretrieve(duanzi_img, './image/' + fname)
            else:
                duanzi_img = ''
            self.f.write(json.dumps(data, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    # 请求队列
    request_que = Queue()
    # 数据队列
    data_que = Queue()
    # 文件
    f = open('dz.json','w',encoding='utf-8')
    base_url = 'https://www.qiushibaike.com/8hr/page/%d/'
    # 制作请求的url队列
    for page in range(1,14):
        full_url = base_url % page
        request_que.put(full_url)

    # 采集线程
    thread_list = []
    for i in range(Max_Threading):
        t = Crawl(i+1,request_que,data_que)
        t.start()
        thread_list.append(t)
    # 解析线程
    parse_list = []
    for i in range(Max_Threading):
        temp = Parse(i+1,data_que,thread_list,f)
        temp.start()
        parse_list.append(temp)
    # 采集线程完毕
    for i in thread_list:
        i.join()
    # 解析线程完毕
    for i in parse_list:
        i.join()
    # 关闭文件
    f.close()