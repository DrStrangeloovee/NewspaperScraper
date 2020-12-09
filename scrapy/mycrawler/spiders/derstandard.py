from mycrawler.items import StoryItem, PostingItem
import datetime
from scrapy.spiders import SitemapSpider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

# from mycrawler.items import StoryItem


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
        # TODO: fetch authors from story_content
        # story_item_loader.add_xpath('story_authors_short', )
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

        # TODO: maybe create a function for this
        story_page_id = story_item_loader.get_output_value("story_id")
        filename = f"{story_page_id}.html"
        with open("data/" + self.name + "/" + filename, "wb") as f:
            f.write(response.body)
        self.logger.info("crawled page %s", response.url)

        story_item = story_item_loader.load_item()

        if story_item.get("story_posting_count"):
            self.logger.info("found %s comments", story_item.get("story_posting_count"))

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
                        posting_story_id=response.url, posting_page_number=page_number
                    ),
                )

                # TODO: create list of posting pages, iterate over it and yield each item
                # https://docs.scrapy.org/en/latest/topics/spiders.html#sitemapspider-examples <-- last example on the bottom
                # self.logger.info('fetching %s/' + str(story_posting_pages + 1) + ' of posting pages',
                #                  story_posting_current_page)
                # story_posting_next_page_url = 'https://apps.derstandard.at/forum/postings/Index/1/' + str(story_item.get('story_id')) + '?ForumKey.ForumKeyId=' + str(story_item.get(
                #     'story_id')) + '&ForumKey.ForumKeyType=1&CurrentPage=' + str(story_posting_current_page) + '&Filter.SelectedFilterType=0&SelectedSortType=0&SelectedPostingId=&X-Requested-With=XMLHttpRequest'
                # yield response.follow(url=story_posting_next_page_url, headers={
                #     'Accept': '*/*',
                #     'Accept-Language': 'en-US,en;q=0.5',
                #     'X-Requested-With': 'XMLHttpRequest',
                #     'Origin': 'https://www.derstandard.at',
                #     'Connection': 'keep-alive',
                #     'Referer': response.url,
                #     'Pragma': 'no-cache',
                #     'Cache-Control': 'no-cache'
                # }, callback=self.parse_postings, cb_kwargs=dict(posting_story_id=response.url))
                # TODO: calculate total posting pages --> story_posting_count/25
                # posting_page_request = Request(
                #     url='https://apps.derstandard.at/forum/postings/Index/1/' + str(story_item.get('story_id')) + '?ForumKey.ForumKeyId=' + str(story_item.get('story_id')) + '&ForumKey.ForumKeyType=1&CurrentPage=' + str(story_posting_current_page) + '&Filter.SelectedFilterType=0&SelectedSortType=0&SelectedPostingId=&X-Requested-With=XMLHttpRequest', method='GET', headers={
                #         'Accept': '*/*',
                #         'Accept-Language': 'en-US,en;q=0.5',
                #         'X-Requested-With': 'XMLHttpRequest',
                #         'Origin': 'https://www.derstandard.at',
                #         'Connection': 'keep-alive',
                #         'Referer': response.url,
                #         'Pragma': 'no-cache',
                #         'Cache-Control': 'no-cache'
                #     }, callback=self.parse_postings, cb_kwargs=dict(posting_story_id=response.url))
                # self.logger.info('request url %s', posting_page_request.url)
                # yield posting_page_request
                # story_posting_current_page = story_posting_current_page + 1
                # self.logger.info('parsing comment page ' + str(story_posting_current_page) + '/' + str(story_posting_pages))
        else:
            self.logger.info("no comments found %s", response.url)

        yield story_item

    """TODO: Calculates the total pages of comments to parse with each page containing 25 comments.

    Args:
        story_posting_count (int): Total amount of comments

    Returns:
        int: Total pages of comments
    """

    def parse_postings(self, response, posting_story_id, posting_page_number):
        self.logger.info("posting reponse %s", response.url)
        posting_item_loader = ItemLoader(item=PostingItem(), response=response)
        posting_item_loader.add_value("posting_story_id", posting_story_id)
        posting_item_loader.add_value("posting_page_number", posting_page_number)
        posting_item_loader.add_xpath("posting_content", '//div[@id="postinglist"]')
        posting_item = posting_item_loader.load_item()
        return posting_item

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
