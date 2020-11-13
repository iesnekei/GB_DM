import os
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from new_pars import settings
from new_pars.spiders.hw_8 import Hw8Spider
from dotenv import load_dotenv

load_dotenv('.env')

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(Hw8Spider,
                     login=os.getenv('USERNAME'),
                     enc_password=os.getenv('ENC_PASSWORD'),
                     parse_resourse=['royalty_beauty_space'])
    crawl_proc.start()
