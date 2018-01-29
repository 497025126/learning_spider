# -*- coding:utf-8 -*-
from scrapy import cmdline
import os

os.chdir('Bigwork/spiders')
cmdline.execute('scrapy runspider job1_lagou.py'.split())
# cmdline.execute('scrapy runspider job2_51job.py'.split())
# cmdline.execute('scrapy runspider job3_zhilian.py'.split())
# cmdline.execute('scrapy runspider job4_zhyc.py'.split())
