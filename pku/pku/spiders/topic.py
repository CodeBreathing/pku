# -*-coding:utf8-*-

from scrapy.selector import Selector
from pku.items import TopicItem
import re

# 在板块中抓取标题，在此页抓取topic的信息
def get_topic_item(response):
    selector = Selector(response)
    check_value = lambda x: x if x else ''

    articleinfo = selector.xpath("//div[@class='list-item-topic list-item']")
    for infolist in articleinfo:
        topicitem = TopicItem()
        article = infolist.xpath("a/@href").extract_first()
        topicidurl = re.search(r'threadid=(\d*)', article, re.M | re.I)
        topicid = topicidurl.group(1)
        topicname = infolist.xpath("div[3]/div/text()").extract_first()
        userid = infolist.xpath("div[5]/div[1]/text()").extract_first()
        replynum = infolist.xpath("div[6]/text()").extract_first()

        topicitem['topicid'] = check_value(topicid)
        topicitem['topicname'] = check_value(topicname)
        topicitem['userid'] = check_value(userid)
        topicitem['replynum'] = check_value(replynum)
        topicitem['classid'] = check_value(classid)
        yield topicitem
        # articleurl = rooturl + article
        # yield Request(articleurl, callback=self.parse_content)
    # 另一种策略，存储完本topic列表信息后，重新抓每个链接并进去每个topic内容，考虑到scrapy抓取url自动去重，不采用
    # article=selector.xpath("//div[@class='list-item-topic list-item']/a/@href").extract()
    # for articlelist in article:
    #     articleurl =rooturl +articlelist
    #     yield Request(articleurl, callback=self.parse_content)

    # # 抓取完本页后处理分页
    # try:
    #     nextpage = selector.xpath('//a/@href[contains(.,"mode=topic")]').extract()
    #     for nextpagelist in nextpage:
    #         # 过滤掉不需要的链接
    #         if nextpagelist.find("v2/thread.php") == -1:
    #             nextpageurl = newrooturl + nextpagelist
    #             yield Request(nextpageurl, callback=self.parse_boardpage)
    # except:
    #     # 如果没有新的页面了，pass，抓下一个topic
    #     pass