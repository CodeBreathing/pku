# -*-coding:utf8-*-

from scrapy.selector import Selector
from pku.items import CommentItem
from scrapy.http import Request
import re
# 抓取一个topic下的所有内容，包括评论、分类、作者信息（完全的作者信息交给下一层处理）
def get_comment_item(response):
    rooturl = "https://bbs.pku.edu.cn/v2/"
    contentrooturl = "https://bbs.pku.edu.cn/v2/post-read.php"
    selector = Selector(response)
    check_value = lambda x: x if x else ''
    # topicname =selector.xpath("//h3/text()").extract()[0]
    # topicitem['topicname'] = topicname

    # 在传入本函数的链接中获取本话题的id,存入topic表和comment表
    topicidurl = re.search(r'threadid=(\d*)', str(response.url), re.M | re.I)
    if topicidurl:
        # print topicid.group()
        # print topicid.group(1)
        topicid = topicidurl.group(1)
        # print matchObj.group(2)
    else:
        print "cannot get the topicid!!"

    # # 获取用户信息的链接
    # user = selector.xpath("//div[@class='post-owner']/a[1]/@href").extract()
    # for userlist in user:
    #     userurl = rooturl + userlist
    #     yield Request(userurl, callback=self.parse_user)

    # 抓取一个topic的每层楼的内容
    floor = selector.xpath("//div[@class='post-card']")
    for floorlist in floor:
        commentitem = CommentItem()
        commentid = floorlist.xpath("div[1]/@id").extract_first()
        floornum = floorlist.xpath("div[3]/span/text()").extract_first()
        contentlist = floorlist.xpath("div[3]/div[1]/div[1]/p[not(@class)]/text()").extract()
        userid = floorlist.xpath("div[2]/p[1]/a/text()").extract_first()
        time = floorlist.xpath("div[3]/div[2]/div[2]/div/span/span[1]/text()").extract_first().encode("utf8").replace(
            "发表于", '')

        content = ""
        for p in contentlist:
            content = content + p
        # print content
        commentitem['userid'] = check_value(userid)
        commentitem['commentid'] = check_value(commentid)
        commentitem['floornum'] = check_value(floornum)
        commentitem['content'] = check_value(content)
        commentitem['time'] = check_value(time)
        commentitem['topicid'] = check_value(topicid)
        yield commentitem
