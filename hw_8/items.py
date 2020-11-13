# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewParsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class YoulaAutoItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()
    statistics = scrapy.Field()
    description = scrapy.Field()
    owner = scrapy.Field()
    # phone_num = scrapy.Field()


class HhItem(scrapy.Item):
    # Часть 1 для обьявлений.
    _id = scrapy.Field()
    vacancy = scrapy.Field()
    salary = scrapy.Field()
    vacancy_description = scrapy.Field()
    skills = scrapy.Field()
    employer_url = scrapy.Field()
    employer_name = scrapy.Field()


class HhCompanyItem(scrapy.Item):
    # Часть 2 для работадателя.
    _id = scrapy.Field()
    employer_url = scrapy.Field()
    employer_name = scrapy.Field()
    employer_web_url = scrapy.Field()
    employer_work = scrapy.Field()
    employer_self_introduce = scrapy.Field()


class InstagramItem(scrapy.Item):
    _id = scrapy.Field()
    extracted_time = scrapy.Field()
    extracted_data = scrapy.Field()
    img = scrapy.Field()


class InstaTag(InstagramItem):
    pass


class InstaPost(InstagramItem):
    pass


class InstagramFollowersList(scrapy.Item):
    _id = scrapy.Field()
    target_name = scrapy.Field()
    extracted_time = scrapy.Field()
    followers_list = scrapy.Field()
    following_list = scrapy.Field()


class InstagramHandShaker(scrapy.Item):
    _id = scrapy.Field()
    user = scrapy.Field()
    extracted_time = scrapy.Field()
    data = scrapy.Field()
