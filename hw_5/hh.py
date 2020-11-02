import scrapy
from ..loaders import HhLoader, HhCompanyLoader


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def parse(self, response, **kwargs):
        for url in response.xpath(HhLoader.hh_path['employer_hh_page']).extract():
            yield response.follow(url, callback=self.employer_parse)
        for url in response.xpath(HhLoader.hh_path['pagination']).extract():
            yield response.follow(url, callback=self.parse)
        print(1)

    def employer_parse(self, response, **kwargs):
        loader = HhCompanyLoader(response=response)
        loader.add_value('employer_url', response.url)
        loader.add_xpath('employer_name', HhCompanyLoader.hh_path['employer_name'])
        loader.add_xpath('employer_web_url', HhCompanyLoader.hh_path['employer_web_url'])
        loader.add_xpath('employer_work', HhCompanyLoader.hh_path['employer_work'])
        loader.add_xpath('employer_self_introduce', HhCompanyLoader.hh_path['employer_self_introduce'])
        yield loader.load_item()

        yield response.follow(response.xpath(HhLoader.hh_path['employer_vacancy']).get(), callback=self.employer_vacancies_parse)
        print(2)

    def employer_vacancies_parse(self, response, **kwargs):
        for url in response.xpath('//a[contains(@data-qa, "vacancy-title")]/@href').extract():
            yield response.follow(url, callback=self.vacancy_parse)
        print(3)

    def vacancy_parse(self, response, **kwargs):
        loader = HhLoader(response=response)
        loader.add_xpath('vacancy', HhLoader.hh_path['vacancy'])
        loader.add_xpath('salary', HhLoader.hh_path['salary'])
        loader.add_xpath('vacancy_description', HhLoader.hh_path['vacancy_description'])
        loader.add_xpath('skills', HhLoader.hh_path['skills'])
        loader.add_xpath('employer_url', HhLoader.hh_path['employer_url'])
        loader.add_xpath('employer_name', HhLoader.hh_path['employer_url'])
        print(4)
        yield loader.load_item()
