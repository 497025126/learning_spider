# -*- coding:utf-8 -*-
from scrapy import cmdline
import os

os.chdir('Bigwork/spiders')
cmdline.execute('scrapy runspider job2_51job.py'.split())

