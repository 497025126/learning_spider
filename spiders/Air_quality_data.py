# -*- coding:utf-8 -*-
"""
输入开始结束日期: 格式如  2018-01-08
输入要查询的城市: 不输入城市默认全国
是否下载数据: 不输入默认不下载  随便输入下载数据
下载的数据文件是json格式
"""
from urllib import request,parse
import re
import json
def get_html(n):
    url = 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action'
    data = {
        'xmlname':'1462259560614',
        'V_DATE':start,
        'E_DATE':end,
        'queryflag':'close',
        'page.pageNo': n,
        'isdesignpatterns':'false',
        'CITY': city
    }
    data = parse.urlencode(data)
    headers = {
        "Content-Length":len(data),
        "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    }
    req = request.Request(url=url,data=bytes(data,encoding='utf-8'),headers=headers)
    response = request.urlopen(req)
    base_html = response.read().decode('utf-8','ignore')
    return base_html

def get_max_page():
    pattern = re.compile(r'总页数&nbsp;：(\d+)')
    res = pattern.search(html)
    if res:
        return res.group(1)
    else:
        return 1

def get_data(html):
    pattern = re.compile(r"""<input  type="hidden" name="gisDataJson"  id="gisDataJson"   value='(.*?)'/>""")
    res = pattern.search(html)
    res = res.group(1)
    json_data = json.loads(res)
    return json_data

def download(city):
    if city == '':
        city = '全国'
    name = city + '空气质量数据'
    f = open('{}.json'.format(name), 'a', encoding='utf-8')
    f.write('[\n')
    for item in lili:
        f.write(str(item) + ',\n')
    f.write(']')
    f.close()

def full_data():
    for i in range(int(max_page)):
        each_html = get_html(i)
        area_data = get_data(each_html)
        for j in area_data:
            # {'CITYCODE': '110000', 'GRADE': '二级',```}
            # j 是个长字典  其中有汉字 dumps第二个参数  不把汉字转换成ascii码
            lili.append(json.dumps(j, ensure_ascii=False))

if __name__ == '__main__':
    start = input('输入开始日期:')
    end = input('输入结束日期:')
    city = input('输入城市(不输入默认全国):')
    flag = input('是否下载天气数据:')
    html = get_html(1)
    max_page = get_max_page()
    lili = []
    full_data()
    for tmp in lili:
        print(tmp)
    if not flag == '':
        download(city)
