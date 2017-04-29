# -*-coding:utf8-*-

from scrapy.selector import Selector
from pku.items import UserItem
from pku.items import TopicItem
from pku.items import CommentItem
from pku.items import ClassificationItem
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import json

class newsmthSpider(CrawlSpider):

    name = "pku"

    start_urls = ["https://bbs.pku.edu.cn/v2/zone.php"]

    def parse(self, response):
        rooturl="https://bbs.pku.edu.cn/v2/"
        selector = Selector(response)
        zone = selector.xpath("//a/@href[contains(.,'board.php')]").extract()
        for zonelist in zone:
            zoneurl = rooturl + zonelist
            yield Request(zoneurl, callback=self.parse_zonepage)

    def parse_zonepage(self, response):
        #print response.url
        rooturl="https://bbs.pku.edu.cn/v2/"
        selector = Selector(response)
        board = selector.xpath("//a/@href[contains(.,'thread.php')]").extract()
        for boardlist in board:
            boardurl = rooturl + boardlist
            yield Request(boardurl, callback=self.parse_boardpage)
    def parse_boardpage(self, response):
        # print response.url
        rooturl = "https://bbs.pku.edu.cn/v2/"
        newrooturl="https://bbs.pku.edu.cn/v2/thread.php"
        selector = Selector(response)
        article=selector.xpath("//div[@class='list-item-topic list-item']/a/@href").extract()
        for articlelist in article:
            articleurl =rooturl +articlelist
            yield Request(articleurl, callback=self.parse_content)
        #抓取完本页后处理分页
        nextpage=selector.xpath('//a/@href[contains(.,"mode=topic")]').extract()
        for nextpagelist in nextpage:
            #过滤掉不需要的链接
            if nextpagelist.find("v2/thread.php")==-1:
                nextpageurl = newrooturl + nextpagelist
                yield Request(nextpageurl, callback=self.parse_boardpage)



    def parse_content(self, response):
        pass