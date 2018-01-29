# -*- coding:utf-8 -*-
from scrapy import cmdline
import os

os.chdir('Bigwork/spiders')
# cmdline.execute('scrapy runspider job4_zhyc.py'.split())
cmdline.execute('scrapy runspider job5_58.py'.split())
