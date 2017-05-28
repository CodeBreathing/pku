# -*-coding:utf8-*-
from scrapy.selector import Selector
from pku.items import UserItem


def get_user_item(response):
    useritem = UserItem()
    selector = Selector(response)

    userid = selector.xpath("//span[@class='bbsid']/text()").extract()[0]
    try:
        nickname = selector.xpath("//span[@class='nickname']/text()").extract()[0]
    except:
        # 比如https://bbs.pku.edu.cn/v2/user.php?uid=85646
        nickname = selector.xpath("//div[@class='nick']/p/span[2]/text()").extract()[0]

    # 下面要注意，打印出来的文本列表里面第一个是回车符，第二个才含着需要的内容,用identity是否存在判断，并不需要存储identity
    try:
        identity = selector.xpath("//div[@class='profile']/div[2]/div[1]/span/text()").extract()[0]
        sex = selector.xpath("//div[@class='profile']/div[1]/div[2]/text()").extract()[1].replace(" ", "").replace("\n",
                                                                                                                   "")
        logintimes = selector.xpath("//div[@class='profile']/div[3]/div[1]/text()").extract()[1].replace(" ",
                                                                                                         "").replace(
            "\n", "")
        topicnum = selector.xpath("//div[@class='profile']/div[3]/div[2]/text()").extract()[1].replace(" ", "").replace(
            "\n", "")
        lifepower = selector.xpath("//div[@class='profile']/div[3]/div[3]/text()").extract()[1].replace(" ",
                                                                                                        "").replace(
            "\n", "")
        score = selector.xpath("//div[@class='profile']/div[4]/div[1]/text()").extract()[1].replace(" ", "").replace(
            "\n", "")
        grade = selector.xpath("//div[@class='profile']/div[4]/div[2]/text()").extract()[1].replace(" ", "").replace(
            "\n", "")
        originalscore = selector.xpath("//div[@class='profile']/div[4]/div[3]/text()").extract()[1].replace(" ",
                                                                                                            "").replace(
            "\n", "")
        lastlogintime = selector.xpath("//div[@class='profile']/div[5]/div[1]/text()").extract()[1].replace(" ",
                                                                                                            "").replace(
            "\n", "")

    except:
        # 下面要注意，打印出来的文本列表里面第一个是回车符，第二个才含着需要的内容
        sex = selector.xpath("//div[@class='profile']/div[1]/div[2]/text()").extract()[1].replace(" ", "").replace("\n",
                                                                                                                   "")
        logintimes = selector.xpath("//div[@class='profile']/div[2]/div[1]/text()").extract()[1].replace(" ",
                                                                                                         "").replace(
            "\n", "")
        topicnum = selector.xpath("//div[@class='profile']/div[2]/div[2]/text()").extract()[1].replace(" ", "").replace(
            "\n", "")
        lifepower = selector.xpath("//div[@class='profile']/div[2]/div[3]/text()").extract()[1].replace(" ",
                                                                                                        "").replace(
            "\n", "")
        score = selector.xpath("//div[@class='profile']/div[3]/div[1]/text()").extract()[1].replace(" ", "").replace(
            "\n", "")
        grade = selector.xpath("//div[@class='profile']/div[3]/div[2]/text()").extract()[1].replace(" ", "").replace(
            "\n", "")
        originalscore = selector.xpath("//div[@class='profile']/div[3]/div[3]/text()").extract()[1].replace(" ",
                                                                                                            "").replace(
            "\n", "")
        lastlogintime = selector.xpath("//div[@class='profile']/div[4]/div[1]/text()").extract()[1].replace(" ",
                                                                                                            "").replace(
            "\n", "")
    # useritem['url']=response.url
    useritem['userid'] = userid
    useritem['nickname'] = nickname
    useritem['sex'] = sex
    useritem['logintimes'] = logintimes
    useritem['topicnum'] = topicnum
    useritem['lifepower'] = lifepower
    useritem['score'] = score
    useritem['grade'] = grade
    useritem['originalscore'] = originalscore
    useritem['lastlogintime'] = lastlogintime
    return useritem
    # return useritem
