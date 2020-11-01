from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from new_pars import settings
from new_pars.spiders.youla import YoulaSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(crawl_settings)
    crawl_proc.crawl(YoulaSpider)
    crawl_proc.start()
