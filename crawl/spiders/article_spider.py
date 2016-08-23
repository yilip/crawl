# -*-coding: utf-8 -*-
import os

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc
from crawl.items import Article
base="e:/data/articles/"
home="http://www.lutous.com/";
class ArticleSpider (Spider):
    name = "article"
    allowed_domains=["www.lutous.com"]
    start_urls = [
        "http://www.lutous.com/plus/list.php?tid=1"
    ]
    ##爬取导航栏
    def parse(self, response):
        print response.headers['Content-Type']
        ##filename = response.url.split("/")[-2]
        ##open(filename, 'wb').write(response.body)
        sel = Selector(response)
        base_url = get_base_url(response)
        lists=[]
        parent_dir_base=''
        parent_dir=''
        print base_url
        pageList = sel.xpath('//div[@class="navigation"]/div')
        listaItem=Article()
        for item in pageList:
            id=item.xpath('@id').extract()
            if(id):
                id=id[0]
            else:
                continue
            if(id.find('list_1')>-1 or id.find('list_2')>-1):
                parent_dir_base=base+item.xpath('a/text()').extract()[0]
                parent_dir_base=parent_dir_base.rstrip()
                if(not os.path.exists(parent_dir_base)):
                    os.makedirs(parent_dir_base)
            elif(id.find('lista')>-1):
                parent_dir=parent_dir_base+'/'+item.xpath('a/text()').extract()[0]
                if(not os.path.exists(parent_dir)):
                    os.makedirs(parent_dir)
                listaItem["link"]=item.xpath('a/@href').extract()[0]
                listaItem["parent_dir"]=parent_dir
            elif(id.find('listb')>-1):
                subitems=item.xpath('div/a')
                if(len(subitems)==0):##本级目录没有数据 返回去找到上级
                    lists.append(listaItem)
                    listaItem=Article()
                    continue
                for subitem in subitems:
                    link = subitem.xpath('@href').extract()[0]
                    content=subitem.xpath('text()').extract()[0]
                    file_name=parent_dir+'/'+content
                    if(not os.path.exists(file_name)):
                        os.makedirs(file_name)
                    print content+":"+link
                    article=Article()
                    article["link"]=link
                    article["content"]=content
                    article["title"]=content
                    article["parent_dir"]=file_name
                    lists.append(article)
        for article in lists:
            yield Request(urljoin_rfc(base_url,article["link"]),meta={'parent_dir':article["parent_dir"]}, callback=self.parse_nav)
    ##爬取目录中的每个子项的所有页数
    def parse_nav(self,response):
        sel = Selector(response)
        base_url = get_base_url(response)
        parent_dir=response.meta["parent_dir"]
        pageinfo = sel.xpath('//div[@class="dede_pages"]/ul/li/span[@class="pageinfo"]/strong')
        pages=int(pageinfo[0].xpath('text()').extract()[0])
        totalResult=pageinfo[1].xpath('text()').extract()[0]
        print str(pages)+"页-"+totalResult+"条:"+parent_dir
        for i in xrange(1,pages+1):
            url=base_url+"&TotalResult="+totalResult+"&PageNo="+str(i)
            yield Request(url=url,meta={'parent_dir':parent_dir}, callback=self.parse_list)
    ##爬取一页的数据
    def parse_list(self,response):
        sel = Selector(response)
        parent_dir=response.meta["parent_dir"]
        pageList = sel.xpath('//div[@class="module"]//h5/a')
        lists=[]
        for item in pageList:
            link=item.xpath('@href').extract()[0]
            url=home+link
            lists.append(url)
        for url in lists:
            yield Request(url=url,meta={'parent_dir':parent_dir}, callback=self.parse_detail)
    ##爬取一篇文章
    def parse_detail(self,response):
        sel = Selector(response)
        base_url = get_base_url(response)
        i=base_url.find("aid=")
        item=Article()
        parent_dir=response.meta["parent_dir"]
        item["id"]=base_url[(i+4):]
        item["link"]=base_url
        item["parent_dir"]=parent_dir
        item["title"] =sel.xpath('//div[@class="article primaryContent"]/h1').extract()[0]
        item["content"]=(sel.xpath('//div[@id="resizeableText"]').extract()[0]).replace("/uploads",home+"uploads/")
        yield item

