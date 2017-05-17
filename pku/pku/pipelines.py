# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.python import log
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
from pku.items import UserItem, TopicItem, CommentItem, ClassificationItem
# from pku.utils import MD5Utils

class PkuPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLStorePkuPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        #调用下面的md5函数
        # usermd5id = self._get_usermd5id(item)
        # topicmd5id = self._get_topicmd5id(item)
        # commentmd5id =self._get_commentmd5id(item)
        #后期尝试使用外面的md5函数统一处理
        # usermd5id = MD5Utils.md5_code(item['userid']).encode()
        # topicmd5id = MD5Utils.md5_code(item['topicmd5id']).encode()
        # commentmd5id = MD5Utils.md5_code(item['commentmd5id']).encode()
        #自己添加了cursor，教程里直接用的conn

        # item是useritem时
        if isinstance(item, UserItem):
            usermd5id = self._get_usermd5id(item)
            # print usermd5id
            #now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
            conn.execute("select 1 from user where userid = %s", usermd5id)
            userret = conn.fetchone()

            if userret:
                conn.execute("update user set nickname = %s, sex = %s, logintimes = %s, topicnum = %s,lifepower =%s, score= %s, grade= %s, originalscore =%s, lastlogintime= %s where userid = %s"
                ,( item['nickname'], item['sex'], item['logintimes'], item['topicnum'], item['lifepower'],item['score'],item['grade'],item['originalscore'],item['lastlogintime'], usermd5id))
                # print """
                #    update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
                # """, (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id)
            else:
                conn.execute("insert into user(userid, nickname, sex, logintimes, topicnum, lifepower, score, grade, originalscore, lastlogintime) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (usermd5id, item['nickname'], item['sex'],item['logintimes'], item['topicnum'], item['lifepower'],item['score'],item['grade'],item['originalscore'],item['lastlogintime']))
                # print """
                #    insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
                #    values(%s, %s, %s, %s, %s, %s)
                # """, (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now)
        elif isinstance(item, TopicItem):
            usermd5id = self._get_usermd5id(item)
            topicmd5id = self._get_topicmd5id(item)
            #now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
            conn.execute("select 1 from topic where topicid = %s", topicmd5id)
            topicret = conn.fetchone()
            if topicret:
                conn.execute("update topic set userid = %s, classid = %s, topicname = %s, replynum = %s where topicid = %s",( usermd5id, item['classid'], item['topicname'], item['replynum'],topicmd5id))
            else:
                conn.execute("insert into topic(topicid, userid, classid, topicname, replynum) values( %s, %s, %s, %s, %s)", (topicmd5id, usermd5id, item['classid'],item['topicname'], item['replynum']))
        elif isinstance(item, CommentItem):
            usermd5id = self._get_usermd5id(item)
            topicmd5id = self._get_topicmd5id(item)
            commentmd5id =self._get_commentmd5id(item)
            conn.execute("select 1 from comment where commentid = %s", commentmd5id)
            commentret =conn.fetchone()
            if commentret:
                conn.execute("update comment set topicid = %s, userid = %s, content = %s, time = %s, floornum = %s where commentid = %s",( topicmd5id, usermd5id, item['content'], item['time'],item['floornum'],commentmd5id))
            else:
                conn.execute("insert into comment(commentid, topicid, userid, content, time, floornum) values( %s, %s, %s, %s, %s, %s)", (commentmd5id, topicmd5id, usermd5id, item['content'],item['time'], item['floornum']))
        elif isinstance(item, ClassificationItem):
            #classid本来就是自己拼接的字符串，不加密
            conn.execute("select 1 from classification where classid = %s", item['classid'])
            classret =conn.fetchone()
            if classret:
                conn.execute("update classification set inboard = %s, inthread = %s where classid = %s",( item['inboard'], item['inthread'], item['classid']))
            else:
                conn.execute("insert into classification(classid, inboard, inthread) values(%s, %s, %s)", (item['classid'],item['inboard'], item['inthread']))
    # 获取userid的md5编码
    def _get_usermd5id(self, item):
        # url进行md5处理，为避免重复采集设计
        return md5(item['userid']).hexdigest()
    # 获取topicid的md5编码
    def _get_topicmd5id(self, item):
        # url进行md5处理，为避免重复采集设计
        return md5(item['topicid']).hexdigest()
    # 获取commentid的md5编码
    def _get_commentmd5id(self, item):
        # url进行md5处理，为避免重复采集设计
        return md5(item['commentid']).hexdigest()
    #异常处理
    def _handle_error(self, failure, item, spider):
        log.err(failure)
