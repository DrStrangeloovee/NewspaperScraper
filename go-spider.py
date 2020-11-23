from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from mycrawler.spiders.pageavailability import PageavailabilitySpider
from mycrawler.spiders.derstandard import DerStandardCrawler

process = CrawlerProcess(get_project_settings())
process.crawl(DerStandardCrawler)
process.start()
