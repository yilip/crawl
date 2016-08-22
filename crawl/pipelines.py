# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class crawlPipeline(object):
    global base_dir
    base_dir="articles/"
    def process_item(self, item, spider):
        file_name = item['title']
        file_name += ".html"
        fp = open(base_dir+file_name, 'w')
        fp.write(item['content'])
        fp.close()
        return item