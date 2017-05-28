# -*-coding:utf8-*-
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from spiders.user import get_user_item
from spiders.topic import get_topic_item
from spiders.comment import get_comment_item
from spiders.classification import get_classification_item


# class PkuSpider(CrawlSpider):
#
#     name = "pku"
class newsmthSpider(CrawlSpider):

    name = "pku"

    allowed_domains = ['bbs.pku.edu.cn']
    start_urls = ["https://bbs.pku.edu.cn/v2/zone.php"]

    boardpage_extract = LxmlLinkExtractor(
        allow=(
            'thread.php?',
        ),
        allow_domains=(
            'bbs.pku.edu.cn',
        ),
        # deny=(
        #     '/\$%7BblogDetail',
        #     '/\$%7Bx\.',
        #     '/\$%7Bfurl',
        # ),
        # deny_domains=(
        #
        # )
    )

    user_extract = LxmlLinkExtractor(
        allow=(
            # '/profile',
            'user.php'
        ),
        allow_domains=(
            'bbs.pku.edu.cn'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )
    comment_extract = LxmlLinkExtractor(
        allow=(
            'post-read.',
        ),
        allow_domains=(
            'bbs.pku.edu.cn'
        ),
        deny=(
            #置顶帖一般为版主发的通知，没用
            'post-read-single.php?'
        ),
        # deny_domains=(
        #
        # )
    )

    follow_extract = LxmlLinkExtractor(
        allow=(
            # '/s/[0-9]+',
            '&mode=topic&',
            'page =',
            'board.php?',
        ),
        allow_domains=(
            'bbs.pku.edu.cn'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    rules = (
        Rule(user_extract, follow=True, callback='parse_user'),
        Rule(boardpage_extract, follow=True, callback='parse_topicandclass'),
        # Rule(follow_extract, follow=True, callback='parse_follow'),
        Rule(follow_extract, follow=True),
        Rule(comment_extract, follow=True, callback='parse_comment')
    )
    a_count = 0
    p_count = 0
    f_count = 0

    def parse_user(self, response):
        # self.a_count += 1
        # print('author: ', self.a_count, '  ', response.url)
        useritem = get_user_item(response)
        yield useritem

    # def parse_follow(self, response):
    #     self.f_count += 1
    #     print('follow: ', self.f_count, '  ', response.url)

    def parse_comment(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)
        for commentitem in get_comment_item(response):
            yield commentitem

    def parse_topicandclass(self, response):
        classificationitem = get_classification_item(response)
        for topicitem in get_topic_item(response):
            yield topicitem
        yield classificationitem



