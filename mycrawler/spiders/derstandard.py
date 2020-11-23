from datetime import timedelta, date
from scrapy.spiders import SitemapSpider
from mycrawler.items import MycrawlerItem


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
        page = response.url.split('/')[-1]
        filename = f'{page}.html'
        with open('data/' + self.name + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.logger.info('crawled page %s', response.url)

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
