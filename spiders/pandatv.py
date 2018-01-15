# -*- coding:utf-8 -*-
"""
本次抓取熊猫直播当前所有直播间的 : [标题 人数  主播名字  房间ID  直播标签  购买车票(道具)人数]

使用代码操作浏览器,模拟人访问浏览器的操作过程,在操作过程中抓取数据
webdriver  内置操作浏览器的很多函数
etree  标签过滤  筛选文本 属性等
"""
from selenium import webdriver
from lxml import etree
import json
import time,random

#全局变量 熊猫全部直播首页
base_url = "https://www.panda.tv/all?pdt=1.18.pheader-n.1.78h1ehidadq"
f = open('PandaTV.json', 'w', encoding='utf-8')
f.write('[\n')

def parse_html(html):
    html = etree.HTML(html)
    # 以下获取的都是房间的信息的列表
    video_title = html.xpath("//span[@class='video-title']/text()")
    # 列表推导式  去除无用的空格 换行 组成新的列表
    nick_name = [i.strip() for i in html.xpath("//span[@class='video-nickname']/text()") if not i =='\n                                                ']
    watching_number = html.xpath("//span[@class='video-number']/text()")
    bus_info = html.xpath("//span[@class='video-station-info']/i[@class='video-station-num']/text()")
    video_tags = [''.join(i.xpath(".//text()")).strip().replace(' ','').replace('\n',' ') for i in html.xpath("//div[@class='video-label-content']")]
    room_id = html.xpath("//a//@data-id")
    for i in range(len(video_title)):
        data = {
            "video_title": video_title[i],
            "nick_name": nick_name[i],
            "watching_number": watching_number[i],
            "bus_info": bus_info[i],
            "video_tags": video_tags[i],
            "room_id": room_id[i]
        }
        # print(data)
        f.write(json.dumps(data,ensure_ascii=False)+',\n')

def parse(url):
    # 随机睡眠 1.几秒 防止被认为机器操作封停
    time.sleep(random.random()+1)
    # get 方式访问链接  也就是在浏览器中输入 url
    browser.get(url)

    # 因为要有终止条件 但是第一页中上一页标签中也有 disabled属性 这个变量仅使用一次
    first = False
    while True:
        # 获取html代码
        html = browser.page_source
        # 分析代码中的数据 并保存
        parse_html(html)
        # 点击下一页
        browser.find_element_by_class_name('j-page-next').click()
        # 随机休息2.几秒
        time.sleep(random.random()+2)
        # 第一页中的上一页排除掉  到最后一页跳出循环
        if 'disabled' in html and first:
            break
        first = True

if __name__ == '__main__':
    # 制作一个浏览器 这里选择谷歌浏览器  需要提前把谷歌浏览器的驱动添加在环境变量中  或者
    # 在 Chorme(executable_path="路径")
    browser = webdriver.Chrome()
    # 解析链接
    parse(base_url)
    # 关闭浏览器窗口
    browser.quit()
    f.write(']')