# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class crawlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class Article(Item):
    title=Field()
    link=Field()
    content=Field()
