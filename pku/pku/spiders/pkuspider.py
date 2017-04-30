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
    #第一层在首页中抓取分区链接
    def parse(self, response):
        rooturl="https://bbs.pku.edu.cn/v2/"
        selector = Selector(response)
        zone = selector.xpath("//a/@href[contains(.,'board.php')]").extract()
        for zonelist in zone:
            zoneurl = rooturl + zonelist
            yield Request(zoneurl, callback=self.parse_zonepage)
    #第二层：在分区中抓取板块
    def parse_zonepage(self, response):
        #print response.url
        rooturl="https://bbs.pku.edu.cn/v2/"
        selector = Selector(response)
        board = selector.xpath("//a/@href[contains(.,'thread.php')]").extract()
        for boardlist in board:
            boardurl = rooturl + boardlist
            yield Request(boardurl, callback=self.parse_boardpage)
    #第三层：在板块中抓取标题并处理翻页
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

    #第四层：抓取内容
    def parse_content(self, response):
        topicitem=TopicItem()
        commentitem=CommentItem()
        classificationitem=ClassificationItem()
        rooturl ="https://bbs.pku.edu.cn/v2/"
        selector =Selector(response)
        topic =selector.xpath("//h3/text()").extract()[0]
        topicitem['name'] = topic
        #获取本话题所在的版面
        inboard =selector.xpath("//div[@class='breadcrumb-trail']/a[4]/text()").extract()[0]
        inzone =selector.xpath("//div[@class='breadcrumb-trail']/a[3]/text()").extract()[0]
        classificationitem['inboard']=inboard
        classificationitem['inzone']=inzone
        #获取用户信息的链接
        user = selector.xpath("//div[@class='post-owner']/a[1]/@href").extract()
        for userlist in user:
            userurl =rooturl+userlist
            yield Request(userurl, callback=self.parse_user)

        #抓取一个topic的每层楼的内容
        floor =selector.xpath("//div[@class='post-card']")
        for floorlist in floor:
            floornum =floorlist.xpath("div[3]/span/text()").extract()[0]
            content = floorlist.xpath("div[3]/div[1]/div[1]/p/text()").extract()[0]
            user =floorlist.xpath("div[2]/p[1]/a/text()").extract()[0]
            time = floorlist.xpath("div[3]/div[2]/div[2]/div/span/span[1]/text()").extract()[0].encode("utf8").replace("发表于",'')
            commentitem['floornum'] =floornum
            commentitem['content'] =content
            commentitem['user'] =user
            commentitem['time'] =time


    #第五层,处理一个用户的所有信息，返回给UserItem
    def parse_user(self, response):
        useritem =UserItem()
        selector=Selector(response)
        username =selector.xpath("//span[@class='bbsid']/text()").extract()[0]
        nickname =selector.xpath("//span[@class='nickname']/text()").extract()[0]
        #下面要注意，打印出来的文本列表里面第一个是回车符，第二个才含着需要的内容
        sex =selector.xpath("//div[@class='profile']/div[1]/div[2]/text()").extract()[1].replace(" ","").replace("\n","")
        logintimes =selector.xpath("//div[@class='profile']/div[2]/div[1]/text()").extract()[1].replace(" ","").replace("\n","")
        topicnum =selector.xpath("//div[@class='profile']/div[2]/div[2]/text()").extract()[1].replace(" ","").replace("\n","")
        lifepower =selector.xpath("//div[@class='profile']/div[2]/div[3]/text()").extract()[1].replace(" ","").replace("\n","")
        score =selector.xpath("//div[@class='profile']/div[3]/div[1]/text()").extract()[1].replace(" ","").replace("\n","")
        grade =selector.xpath("//div[@class='profile']/div[3]/div[2]/text()").extract()[1].replace(" ","").replace("\n","")
        originalscore =selector.xpath("//div[@class='profile']/div[3]/div[3]/text()").extract()[1].replace(" ","").replace("\n","")
        lastlogintime =selector.xpath("//div[@class='profile']/div[4]/div[1]/text()").extract()[1].replace(" ","").replace("\n","")

        useritem['username']=username
        useritem['nickname'] =nickname
        useritem['sex'] =sex
        useritem['logintimes'] =logintimes
        useritem['topicnum'] =topicnum
        useritem['lifepower'] =lifepower
        useritem['score'] =score
        useritem['grade'] =grade
        useritem['originalscore'] =originalscore
        useritem['lastlogintime'] =lastlogintime

