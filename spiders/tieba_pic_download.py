# -*- coding:utf-8 -*-
"""
1. 输入贴吧名,以及页数区间
2. 在本文件同级目录下以贴吧名创建目录
3. 下载每个帖子的第一页,用户发出的图片
"""
from urllib import request,parse
import re
import os
def download_pic(url):
    for pic in url:
        print('downloading...%s' % pic)
        fname = pic.split('/')[-1]
        request.urlretrieve(pic, './{}/'.format(searchname)+fname)

#分析帖子 找出图片链接
def analysis_tiezi(url):
    pattern = re.compile(r'<img class="BDE_Image" src="(.*?)"')
    res = pattern.findall(url)
    return res


# 进入帖子
def in_tiezi(res):
    tiezi_url = 'https://tieba.baidu.com/'
    pattern = re.compile(r'href="(.*)"')
    for i in res:
        res = pattern.search(i)
        url = 'https://tieba.baidu.com'+res.group(1)
        response = request.urlopen(url)
        html = response.read().decode('utf-8')
        # ing_url 是个列表
        img_url = analysis_tiezi(html)
        download_pic(img_url)

def find_each_url(html):
    pattern = re.compile(r'href="/p/\d*"')
    res = pattern.findall(html)
    in_tiezi(res)

def search(start,end,searchname):
    while True:
        base_url = 'https://tieba.baidu.com/f?'
        queryset = {
            'kw': searchname,
            'ie': 'utf-8',
            'pn': 50 * (start-1),
        }
        if not os.path.exists(searchname):
            os.mkdir(searchname)
        queryset = parse.urlencode(queryset)
        req = request.Request(base_url+queryset)
        response = request.urlopen(req)
        # 第二个参数,防止部分页面中含有特殊符号无法用utf-8解析,遇到这些字符就忽略
        html = response.read().decode('utf-8','ignore')
        # 获取各个帖子的链接
        find_each_url(html)
        start = start + 1
        if start == end + 1:
            break

if __name__ == '__main__':
    searchname = input('请输入要下载的贴吧的名称:')
    start = int(input('请输入起始页:'))
    end = int(input('请输入结束页:'))
    search(start,end,searchname)
