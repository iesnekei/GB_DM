# Источник https://magnit.ru/promo/
# Регион любой
# Задача: Обойти все товары по акции и собрать данные в MongoDB
# следующей структуры:
#
# product_template = {
# 'url': ссылка на товар
# 'promo_name': Название акции,
# 'product_name': Название продукта,
# 'old_price': стоимость старая (Тип Float),
# 'new_price': стоимсоть новая (Тип Float),
# 'image_url': ссылка на изображение',
# 'date_from': дата начала акции (тип datetime),
# 'date_to': дата окончания (тип datetime),
# }
#
# если данные какго-либо поля не доступны записать None
# полученые структуры товаров сохраняем в коллекцию MongoDB
# дополнительно:
# составить запрос группирующий товары по названию акции


import requests
import json
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

class Parse_magnit:


    def __init__(self, start_url):
        self.start_url = start_url
        mongo_client = MongoClient()
        self.db  = mongo_client['hw_2']
        self.month = [ 'января' , 'февраля' , 'марта' , 'апреля' , 'мая' , 'июня' , 'июля' , 'августа' , 'сентября' , 'октября' , 'ноября' , 'декабря' ]

    def parse(self):
        products_dict   = {}
        product_template = {
            'url': None,
             'promo_name': None,
            'product_name': None,
            'old_price': None,
            'new_price': None,
            'image_url': None,
            'date_from': None,
            'date_to': None,
        }
        response = requests.get(self.start_url)
        soup = BeautifulSoup(response.text, 'lxml')
        promos = soup.findAll('a', attrs={'class': 'card-sale_catalogue'}, href=True)

        for i in range(0, len(promos)):
            products_dict[i] = {}
            try:
                products_dict[i]['url'] = promos[i]['href']
            except:
                products_dict[i]['url'] = None

            try:
                products_dict[i]['promo_name'] = promos[i].find(attrs={'class': 'card-sale__header'}).find('p').text
            except:
                products_dict[i]['promo_name'] = None

            try:
                products_dict[i]['product_name'] = promos[i].find(attrs={'class':'card-sale__title'}).text
            except:
                products_dict[i]['product_name'] = None

            try:
                products_dict[i]['old_price'] = float(promos[0].find(
                    attrs={'class':'label__price_old'}).find(
                    attrs={'class':'label__price-integer'}).text) + float(promos[0].find(
                    attrs={'class':'label__price_old'}).find(
                    attrs={'class':'label__price-decimal'}).text) / 100
            except:
                products_dict[i]['old_price'] = None

            try:
                products_dict[i]['new_price'] = float(promos[0].find(
                    attrs={'class':'label__price_new'}).find(
                    attrs={'class':'label__price-integer'}).text) + float(promos[0].find(
                    attrs={'class':'label__price_new'}).find(
                    attrs={'class':'label__price-decimal'}).text) / 100
            except:
                products_dict[i]['new_price'] = None

            try:
                products_dict[i]['image_url'] = promos[i].find('img')['data-src']
            except:
                products_dict[i]['image_url'] = None

            try:
                products_dict[i]['date_from']  = (promos[i].find(attrs={'class':'card-sale__date'}).findAll('p')[0].text)
                products_dict[i]['date_from'] = products_dict[i]['date_from'].split(' ')[1:]
                products_dict[i]['date_from'][1] = str(int(self.month.index(products_dict[0]['date_from'][1])) + 1)
                products_dict[i]['date_from'] = '-'.join(products_dict[i]['date_from'])
                products_dict[i]['date_from'] = datetime.strptime(products_dict[i]['date_from'], '%d-%m')

            except:
                products_dict[i]['date_from'] = None

            try:
                products_dict[i]['date_to'] = promos[i].find(attrs={'class': 'card-sale__date'}).findAll('p')[
                        1].text
                products_dict[i]['date_to'] = products_dict[i]['date_to'].split(' ')[1:]
                products_dict[i]['date_to'][1] = str(int(self.month.index(products_dict[0]['date_to'][1])) + 1)
                products_dict[i]['date_to'] = '-'.join(products_dict[i]['date_to'])
                products_dict[i]['date_to'] = datetime.strptime(products_dict[i]['date_to'], '%d-%m')
            except:
                products_dict[i]['date_to'] = None

        # self.save_to(products_dict)
        print(1)

    def save_to(self, product_data: dict):
        collection = self.db['magnit']
        collection.insert_one(product_data)


















                # urls = soup.findAll('a', attrs={'class': 'card-sale_catalogue'}, href=True)
        # for i in range(0, len(urls)):
        #     product_template['url'].append(urls[i]['href'])




        print(product_template)





if __name__ ==  '__main__':

    hw_2  =  Parse_magnit('https://magnit.ru/promo/?geo=moskva')
    hw_2.parse()
