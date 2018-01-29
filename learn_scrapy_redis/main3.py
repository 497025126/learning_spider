# -*- coding:utf-8 -*-
from scrapy import cmdline
import os

os.chdir('Bigwork/spiders')
# cmdline.execute('scrapy runspider job3_zhilian.py'.split())
cmdline.execute('scrapy runspider job6_liepin.py'.split())
