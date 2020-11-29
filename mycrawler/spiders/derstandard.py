from mycrawler.items import StoryItem, CommentItem
import datetime
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import chompjs

# from mycrawler.items import StoryItem


class DerStandardCrawler(SitemapSpider):
    name = 'derstandard'

    # allowed_domains = ['derstandard.at']

    sitemap_urls = [
        'https://www.derstandard.at/robots.txt',
    ]

    sitemap_follow = [
        '/sitemap-2020-1'
    ]

    sitemap_rules = [('/story/', 'parse_story'), ]

    custom_settings = {
        'LOG_FILE': 'data/logs/crawler_' + name + '.log',
        'LOG_LEVEL': 'INFO'
    }

    def parse_story(self, response):
        # TODO: fetch lastmod from sitemap.xml
        # TODO: maybe change some xpaths to css selectors
        item_loader = ItemLoader(item=StoryItem(), response=response)
        item_loader.add_value('story_url', response.url)
        item_loader.add_xpath(
            'story_authors', 'normalize-space(//div[@class="article-origins"]/text()[1])')
        # TODO: fetch authors from story_content
        # item_loader.add_xpath('story_authors_short', )
        item_loader.add_xpath(
            'story_posting_count', 'normalize-space(//p[@class="article-postingcount"]/button/text())')
        item_loader.add_xpath(
            'story_breadcrumbs', '//nav[@class="site-contextnavigation-breadcrumbs-nav"]/a/@title')
        item_loader.add_xpath('story_publication_date',
                              'string(//time/@datetime)')
        item_loader.add_xpath('story_modification_date',
                              'string(//time/@datetime)')
        item_loader.add_xpath('story_json_data',
                              '//script[@type="application/ld+json"]/text()')
        item_loader.add_xpath(
            'story_kicker', '//h2[@class="article-kicker"]/text()')
        item_loader.add_xpath(
            'story_title', '//h1[@class="article-title"]/text()')
        item_loader.add_xpath(
            'story_subtitle', '//p[@class="article-subtitle"]/text()')
        item_loader.add_xpath(
            'story_content', '//div[@class="article-body"]/*[self::p or self::h3]')
        item_loader.add_value('story_id', response.url.split('/')[-2])
        item_loader.add_value('crawler_name', self.name)
        item_loader.add_value(
            'store_date', datetime.datetime.now().timestamp())
        item_loader.add_value('store_modification_date',
                              datetime.datetime.now().timestamp())
        item_loader.add_value(
            'store_file', response.url.split('/')[-2] + '.html')

        # page = item_loader.get_output_value('story_id')[0]
        # filename = f'{page}.html'
        # with open('data/' + self.name + '/' + filename, 'wb') as f:
        #     f.write(response.body)
        # self.logger.info('crawled page %s', response.url)

        story_item = item_loader.load_item()
        # self.logger.info('created item %s', story_item)
        yield story_item

        # def parse_comments(self, response):
        #     yield

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
