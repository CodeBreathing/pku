# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    userid =Field()             #用户id（对应页面分析中的bbsid,字符串类型）
    nickname =Field()           #昵称
    sex =Field()                #性别
    logintimes =Field()         #登陆次数
    topicnum =Field()           #发帖数
    lifepower =Field()          #生命力
    score =Field()              #积分
    grade =Field()              #等级
    originalscore =Field()      #原创积分
    lastlogintime =Field()      #最后登陆时间

class TopicItem(Item):
    topicid =Field()            #页面自带的topicid（threadid）
    userid =Field()             #同用户表的用户id
    classid =Field()            #关联分类表的分类id
    topicname =Field()          #话题的名字
    replynum =Field()           #回复数


class CommentItem(Item):
    topicid =Field()            #关联话题表的话题id（threadid）
    commentid=Field()
    userid =Field()             #同用户表的用户id
    content =Field()            #评论的内容
    time =Field()               #评论的时间（最后修改时间）
    floornum =Field()           #第几层楼


class ClassificationItem(Item):
    classid =Field()
    inboard = Field()           #所在分区名
    inthread = Field()            #所在话题名
