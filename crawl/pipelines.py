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
    def process_item(self, item, spider):
        file_name =item['id']+".html"
        fp = open(item["parent_dir"]+'/'+file_name, 'w')
        fp.write(item['title'])
        fp.write(item['content'])
        fp.close()
        return item