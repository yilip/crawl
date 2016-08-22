# -*-coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc
from crawl.items import Article
class ArticleSpider (Spider):
    name = "dmoz"
    allowed_domains=["www.lutous.com"]
    start_urls = [
        "http://www.lutous.com/plus/list.php?tid=13"
    ]

    def parse(self, response):
        print response.headers['Content-Type']
        ##filename = response.url.split("/")[-2]
        ##open(filename, 'wb').write(response.body)
        sel = Selector(response)
        base_url = get_base_url(response)
        lists=[]
        TotalResult=431
        pages=44
        print base_url
        # pageList = sel.xpath('//div[@class="dede_pages"]/ul/li')
        # for item in pageList:
        #     p=p+1;
        #     link = item.xpath('a/@href').extract()
        #     print link
        #     if(link):
        #         lists.append(link)
        for pageNo in xrange(1,2):
            link=base_url+"&pageNo="+str(pageNo)+"&TotalResult=431"
            print link
            yield Request(urljoin_rfc(base_url,link), meta={'page':pageNo},callback=self.parse_list)

    def parse_list(self,response):
        sel = Selector(response)
        base_url = get_base_url(response)
        articles=sel.xpath('//div[@class="module"]/div/h5')
        lists=[]
        for article in articles:
            link=article.xpath('a/@href').extract()
            if(link):
                print  link
                lists.append(link)
        for link in lists:
            yield Request(urljoin_rfc(base_url,link[0]), meta={'link':link[0]},callback=self.parse_detail)
    def parse_detail(self,response):
        sel = Selector(response)
        item=Article()
        item["link"]=response.meta["link"]
        item["title"] =sel.xpath('//div[@class="article primaryContent"]/h1/text()').extract()[0]
        item["content"]=sel.xpath('//div[@id="resizeableText"]').extract()[0]
        yield item
