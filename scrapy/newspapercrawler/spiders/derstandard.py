from newspapercrawler.items import StoryItem, PostingItem
import datetime
from scrapy.spiders import SitemapSpider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class DerStandardCrawler(SitemapSpider):
    name = "derstandard"

    # allowed_domains = ['derstandard.at']

    sitemap_urls = [
        "https://www.derstandard.at/robots.txt",
    ]

    sitemap_follow = ["/sitemap-2020-1"]

    sitemap_rules = [
        ("/story/", "parse_story"),
    ]

    custom_settings = {
        "LOG_FILE": "data/logs/crawler_" + name + ".log",
        "LOG_LEVEL": "INFO",
        "MEMDEBUG_ENABLED": "True",
    }

    def parse_story(self, response):
        # TODO: fetch lastmod from sitemap.xml
        # TODO: maybe change some xpaths to css selectors
        story_item_loader = ItemLoader(item=StoryItem(), response=response)
        story_item_loader.add_value("story_url", response.url)
        story_item_loader.add_xpath(
            "story_authors",
            'normalize-space(//div[@class="article-origins"]/text()[1])',
        )
        story_item_loader.add_xpath(
            "story_posting_count",
            'normalize-space(//p[@class="article-postingcount"]/button/text())',
        )
        story_item_loader.add_xpath(
            "story_breadcrumbs",
            '//nav[@class="site-contextnavigation-breadcrumbs-nav"]/a/@title',
        )
        story_item_loader.add_xpath(
            "story_publication_date", "string(//time/@datetime)"
        )
        story_item_loader.add_xpath(
            "story_modification_date", "string(//time/@datetime)"
        )
        story_item_loader.add_xpath(
            "story_json_data", '//script[@type="application/ld+json"]/text()'
        )
        story_item_loader.add_xpath(
            "story_kicker", '//h2[@class="article-kicker"]/text()'
        )
        story_item_loader.add_xpath(
            "story_title", '//h1[@class="article-title"]/text()'
        )
        story_item_loader.add_xpath(
            "story_subtitle", '//p[@class="article-subtitle"]/text()'
        )
        story_item_loader.add_xpath(
            "story_content", '//div[@class="article-body"]/*[self::p or self::h3]'
        )
        story_item_loader.add_value("story_id", response.url.split("/")[-2])
        story_item_loader.add_value("crawler_name", self.name)
        story_item_loader.add_value("store_date", datetime.datetime.now().timestamp())
        story_item_loader.add_value(
            "store_modification_date", datetime.datetime.now().timestamp()
        )
        story_item_loader.add_value("store_file", response.url.split("/")[-2] + ".html")

        story_item = story_item_loader.load_item()

        if story_item.get("story_posting_count"):
            # self.logger.info("found %s comments", story_item.get("story_posting_count"))

            story_posting_pages = calculate_story_posting_pages(
                story_item.get("story_posting_count")
            )

            for page_number in range(1, story_posting_pages + 1):
                story_posting_next_page_url = (
                    "https://apps.derstandard.at/forum/postings/Index/1/"
                    + str(story_item.get("story_id"))
                    + "?ForumKey.ForumKeyId="
                    + str(story_item.get("story_id"))
                    + "&ForumKey.ForumKeyType=1&CurrentPage="
                    + str(page_number)
                    + "&Filter.SelectedFilterType=0&SelectedSortType=0&SelectedPostingId=&X-Requested-With=XMLHttpRequest"
                )
                yield response.follow(
                    url=story_posting_next_page_url,
                    headers={
                        "Accept": "*/*",
                        "Accept-Language": "en-US,en;q=0.5",
                        "X-Requested-With": "XMLHttpRequest",
                        "Origin": "https://www.derstandard.at",
                        "Connection": "keep-alive",
                        "Referer": response.url,
                        "Pragma": "no-cache",
                        "Cache-Control": "no-cache",
                    },
                    callback=self.parse_postings,
                    cb_kwargs=dict(
                        posting_story_id=story_item.get("story_id"),
                        posting_page_number=page_number,
                    ),
                )
        # else:
        #     self.logger.info("no comments found %s", response.url)

        yield story_item

    def parse_postings(self, response, posting_story_id, posting_page_number):
        filename = f"{str(posting_page_number) + '_' + str(posting_story_id)}"
        with open("data/storage/" + self.name + "/posting/" + filename, "wb") as f:
            f.write(response.body)

        comments = response.xpath(
            '//div[@id="postinglist"]/div[contains(@class, "posting")]'
        )
        # comments = response.css('div.posting')
        # self.logger.info("comments %s", comments)
        for comment in comments:
            # self.logger.info("comment %s", comment)
            # self.logger.info(
            #     "comment text %s",
            #     comment.xpath('.//div[@class="upost-text"]').extract(),
            # )
            posting_item_loader = ItemLoader(item=PostingItem(), selector=comment)
            posting_item_loader.add_value("posting_story_id", posting_story_id)
            posting_item_loader.add_value("posting_page_number", posting_page_number)
            posting_item_loader.add_xpath(
                "posting_community_name",
                ".//@data-communityname",
            )
            posting_item_loader.add_value("posting_url", response.url)
            posting_item_loader.add_xpath(
                "posting_organization_id",
                './/span[@class="upost-organization-identity"]/text()',
            )
            # TODO:
            # sometimes also has this class
            # class="upost-verified-identity verified-identity-link"
            posting_item_loader.add_xpath(
                "posting_verified_id",
                './/span[@class="upost-verified-identity"]/@title',
            )
            posting_item_loader.add_xpath(
                "posting_supporter", './/span[@class="upost-supporter"]/@title'
            )
            posting_item_loader.add_xpath(
                "posting_id",
                ".//@data-postingid",
            )
            posting_item_loader.add_xpath(
                "posting_parent_posting_id",
                ".//@data-parentpostingid",
            )
            posting_item_loader.add_xpath(
                "posting_community_id",
                ".//@data-communityidentityid",
            )
            posting_item_loader.add_xpath(
                "posting_community_profile_url",
                './/a[@class="upost-usercontainer js-usercontainer"]/@href',
            )
            posting_item_loader.add_xpath(
                "posting_postdate", './/span[@class="js-timestamp"]/@data-livestamp'
            )
            posting_item_loader.add_xpath(
                "posting_title", './/h4[contains(@class, "upost-title")]/text()'
            )
            # TODO: parse content if it contains a link
            # use and operator:
            # "//category[@name='Sport' and ./author/text()='James Small']"
            posting_item_loader.add_xpath(
                "posting_content", './/div[contains(@class, "upost-text")]/text()'
            )
            posting_item_loader.add_xpath(
                "posting_ratings_positive",
                './/span[@class="js-ratings-positive-count ratings-positive-count"]/text()',
            )
            posting_item_loader.add_value("crawler_name", self.name)

            posting_item_loader.add_xpath(
                "posting_ratings_negative",
                './/span[@class="js-ratings-negative-count ratings-negative-count"]/text()',
            )
            posting_item_loader.add_xpath(
                "posting_follower", './/span[@class="upost-follower"]/text()'
            )
            posting_item_loader.add_value(
                "store_date", datetime.datetime.now().timestamp()
            )

            posting_item = posting_item_loader.load_item()
            yield posting_item

        # page = response.url.split('/')[-1]
        # filename = f'{page}.html'
        # with open('data/' + self.name + '/' + filename, 'wb') as f:
        #     f.write(response.body)
        # self.logger.info('crawled page %s', response.url)

        # def start_requests(self):
        #     self.logger.info('page downloaded from ', response.url)
        # for url in self.start_urls:
        #     yield scrapy.Request(url=url, callback=self.save_raw_page)

        # def save_raw_page(self, response):
        #     self.logger.info('received response ', response)
        # page = response.url.split('/')[-1]
        # self.logger.info('page downloaded from ', response.url)
        # filename = f'{page}.html'
        # with open('data/' + self.name + '/' + filename, 'wb') as f:
        #     f.write(response.body)


def calculate_story_posting_pages(story_posting_count):
    """Calculates the total pages of comments to parse with each page containing 25 comments.

    Args:
        story_posting_count (int): Total amount of comments

    Returns:
        int: Total pages of comments
    """
    return int(-(-story_posting_count // 25))


# def create_story_posting_urls(story_comment_pages):
#     """Creates a list of urls to fetch all pages of comments

#     Args:
#         story_comment_pages (int): Total amount of pages

#     Returns:
#         list: List of comment pages urls
#     """
#     for():
