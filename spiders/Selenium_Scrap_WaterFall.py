# -*- coding:utf-8 -*-
"""
百度图片 搜索
"""
from selenium import webdriver
from lxml import etree
import time,requests
from urllib import request

def parsePage(html):
    html = etree.HTML(html)
    img_div = html.xpath('//div[@class="imgpage"]')[-1]
    img_url = img_div.xpath('.//li//img/@data-imgurl')
    print(img_url)
    # return
    for url in img_url:
        # 下载图片
        print(url)
        fname = url.split('/')[-1]
        request.urlretrieve(url, './image/' + fname)

    # # 使用requests下载
    # for url in img_url:
    #     # 下载图片
    #     # request.urlretrieve(url, './baidu/' + fname)
    #     fname = url.split('/')[-1]
    #     file = open('./image/' + fname, 'wb')
    #     pic_bytes = requests.get(url=url)
    #     file.write(pic_bytes.content)
    #     print(url)

def getPage():
    # dc = {
    #     'phantomjs.page.customHeaders.User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    # }
    # 创建谷歌浏览器  需提前把驱动添加至环境变量中
    # chrome = webdriver.Chrome(executable_path='')
    chrome = webdriver.Chrome()
    base_url = 'https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%C3%C0%C5%AE&fr=ala&ala=1&alatpl=adress&pos=0&hs=2&xthttps=111111'
    chrome.get(base_url)
    time.sleep(2)
    html = chrome.page_source
    parsePage(html)

    # 获取下一页数据
    while True:
        chrome.execute_script('scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)
        html = chrome.page_source
        parsePage(html)
        time.sleep(5)

if __name__ == '__main__':
    getPage()