from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from new_pars import settings
from new_pars.spiders.hh import HhSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(crawl_settings)
    crawl_proc.crawl(HhSpider)
    crawl_proc.start()