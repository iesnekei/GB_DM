import re
import datetime
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from scrapy import Selector
from .items import YoulaAutoItem, HhItem, HhCompanyItem, InstagramItem


def search_author_id(itm):
    re_str = re.compile('youlaId%22%2C%22([0-9a-zA-Z]+)%22%2C%22avatar')
    result = re.findall(re_str, itm)
    return result


def create_user_url(itm):
    base_url = "https://youla.ru/user/"
    result = base_url + itm
    return result


def get_specification(itm):
    tag = Selector(text=itm)
    return {tag.xpath('//div/div[1]/text()').get(): tag.xpath('//div/div[2]/text()').get() or tag.xpath(
        '//div/div[2]/a/text()').get()}


def get_specification_our(itms):
    result = {}
    for itm in itms:
        if None not in itm:
            result.update(itm)

    print(1)
    return result


class YoulaAutoLoader(ItemLoader):
    default_item_class = YoulaAutoItem
    owner_in = MapCompose(search_author_id, create_user_url)
    owner_out = TakeFirst()
    title_out = TakeFirst()
    statistics_in = MapCompose(get_specification)
    statistics_out = get_specification_our

def get_salary(itm):
    result = ' '.join(itm)
    result = result.replace(u'\xa0', u'')
    result = result.rstrip()
    return result

def get_vacancy_description(itm):
    result = ''.join(itm)
    return result

def get_employer_url(itm):
    base_url = 'https://hh.ru'
    result = base_url + itm[0]
    return result

class HhLoader(ItemLoader):
    default_item_class = HhItem
    vacancy_out = TakeFirst()
    salary_out = get_salary
    vacancy_description_out = get_vacancy_description
    employer_url_out = get_employer_url
    hh_path = {
        'pagination': '//a[contains(@class, "HH-Pager")]/@href',
        'employer_hh_page': '//a[contains(@data-qa, "vacancy-employer")]/@href',
        'employer_vacancy': '//a[contains(@data-qa, "employer-vacancies")]/@href',
        'vacancy': '//div[contains(@class, "vacancy-title")]/h1/text()',
        'salary':'//div[contains(@class, "vacancy-title")]/p/span/text()',
        'vacancy_description': '//div[contains(@data-qa, "vacancy-description")]//*/text()',
        'skills': '//div[contains(@class,"tag-list")]//span/text()',
        'employer_url': '//a[contains(@data-qa, "vacancy-company-name")]/@href',
        'employer_name':'//div[contains(@class, "vacancy-company-name")]//a/span/text()',
        # 'employer_web_url':  '//div[@class="employer-sidebar-header"]//span//text()',
    }

def get_employer_name(itm):
    result = ' '.join(itm)
    result = result.replace(u'\xa0', u'')
    result = result.rstrip()
    return result

class  HhCompanyLoader(ItemLoader):
    default_item_class = HhCompanyItem
    employer_url_out = TakeFirst()
    employer_name_out = get_employer_name
    employer_web_url_out = TakeFirst()
    employer_self_introduce_out = get_employer_name
    hh_path = {
        'employer_name':  '//div[@class="employer-sidebar-header"]//span//text()',
        'employer_web_url': '//div[@class="employer-sidebar-content"]/a/@href',
        'employer_work': '//div[@class="employer-sidebar-block"]/p/text()',
        'employer_self_introduce': '//div[@class="company-description"]/div[@class="g-user-content"]//text()',
    }
def get_data(itm):
    instagram_data ={}
    instagram_data['post_id'] = itm[0]['node']['id']
    instagram_data['owner'] = itm[0]['node']['owner']['id']
    instagram_data['post_url'] = f'https://www.instagram.com/p/{itm[0]["node"]["shortcode"]}/'
    instagram_data['post_text'] = itm[0]['node']['edge_media_to_caption']['edges'][0]['node']['text']
    instagram_data['img'] = itm[0]['node']['thumbnail_src']

    return instagram_data
    print(1)

class InstagramLoader(ItemLoader):
    default_item_class = InstagramItem
    data_out = get_data
