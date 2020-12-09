from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from newspapercrawler.spiders.pageavailability import PageavailabilitySpider
from newspapercrawler.spiders.derstandard import DerStandardCrawler

process = CrawlerProcess(get_project_settings())
process.crawl(DerStandardCrawler)
process.start()
