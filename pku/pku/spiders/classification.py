# -*-coding:utf8-*-

from scrapy.selector import Selector
from pku.items import ClassificationItem
import re

# 在板块中抓取标题,在此页抓取分类
def get_classification_item(response):
    # print response.url

    classificationitem = ClassificationItem()

    selector = Selector(response)
    check_value = lambda x: x if x else ''
    # 获取本话题所在的版面及上级版面信息，存到classification表

    inthread = selector.xpath("//div[@class='breadcrumb-trail']/a[4]/text()").extract_first()
    inboard = selector.xpath("//div[@class='breadcrumb-trail']/a[3]/text()").extract_first()
    classificationitem['inboard'] = check_value(inboard)
    classificationitem['inthread'] = check_value(inthread)
    # 计算classid
    inboardurl = selector.xpath("//div[@class='breadcrumb-trail']/a[3]/@href").extract_first()
    inthreadurl = selector.xpath("//div[@class='breadcrumb-trail']/a[4]/@href").extract_first()
    # 正则提取board的bid和thread的bid
    boardbid = re.search(r'bid=(\d*)', inboardurl, re.M | re.I)
    threadbid = re.search(r'bid=(\d*)', inthreadurl, re.M | re.I)
    if boardbid and threadbid:
        classid = str(boardbid.group(1)) + "&" + str(threadbid.group(1))
        classificationitem['classid'] = classid
    else:
        print "cannot get the classbid!!"
    return classificationitem
