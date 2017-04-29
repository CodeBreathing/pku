# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    nickname =Field()           #昵称
    sex =Field()                #性别
    logintimes =Field()         #登陆次数
    lifepower =Field()          #生命力
    score =Field()              #积分
    grade =Field()              #等级
    originalscore =Field()      #原创积分
    lastlogintime =Field()      #最后登陆时间

class TopicItem(Item):
    userid =Field()             #外键，关联用户表的用户id
    classid =Field()            #外键，关联分类表的分类id
    name =Field()               #话题的名字

class CommentItem(Item):
    topicid =Field()            #外键，关联话题表的话题id
    userid =Field()             #外键，关联用户表的用户id
    content =Field()            #评论的内容
    time =Field()               #评论的时间（最后修改时间）
    floor =Field()              #第几层楼

class ClassificationItem(Item):
    name =Field()               #类别的名字
    parent =Field()             #上级分类
