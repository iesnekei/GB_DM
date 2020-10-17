# Источник: https://5ka.ru/special_offers/
# Задача организовать сбор данных,
# необходимо иметь метод сохранения данных в .json файлы
# результат: Данные скачиваются с источника, при вызове метода/
# функции сохранения в файл скачанные данные сохраняются в Json
# вайлы, для каждой категории товаров должен быть создан отдельный
# файл и содержать товары исключительно соответсвующие данной категории.
# пример структуры данных для файла:
# {
# "name": "имя категории",
# "code": "Код соответсвующий категории (используется в запросах)",
# "products": [{PRODUCT},  {PRODUCT}........] # список словарей
# товаров соответсвующих данной категории
# }



import requests
import json
import time

class Parse_category_and_prod:

    def __init__(self, start_url):
        self.start_url  = start_url

    def create_catalog_of_products_by_category(self):
        catalogs = {}
        url = self.start_url
        response = requests.get(url)
        data: dict = response.json()

        for category in data:
            catalogs[f"{category['parent_group_name']}"] = category[f"{'parent_group_code'}"]
        # print(catalogs)

        for category in catalogs:
            category_dict  = {'category name':category, 'category code':catalogs[category], 'products':[]}
            url = f'https://5ka.ru/api/v2/special_offers/?store=&records_per_page=12&page=1&categories={catalogs[category]}&ordering=&price_promo__gte=&price_promo__lte=&search='
            try:
                while url:
                    response = requests.get(url)
                    data: dict = response.json()
                    url = data['next']
                    if len(data['results']) != 0:
                        for i in data['results']:
                            category_dict['products'].append(i)
                with open(f'categories/{category}.json', 'w', encoding='UTF-8') as f:
                    json.dump(category_dict, f, ensure_ascii=False)
                time.sleep(0.01)
            except:
                print('Some problem accure ')









class Mining:
    def __init__(self, income_url):
        self.income_url = income_url

    def parse(self, url=None):
        if not url:
            url = self.income_url

        while url:

            response = requests.get(url)
            data: dict = response.json()

            url = data['next']

            for kind in data['results']:
                print(kind)
                self.save_to_json_file(kind)
            time.sleep(0.11)


    # def save_to_json_file(self, kind: dict):
    #     with open(f'products/{kind["promo['kind']"]}', 'a', encoding='UTF-8') as file:
    #         json.dump(product,  file,  ensure_ascii=False)

if __name__ ==  '__main__':
    parse = Parse_category_and_prod('https://5ka.ru/api/v2/categories/')
    parse.create_catalog_of_products_by_category()