import json
import scrapy
from ..loaders import InstagramLoader
import datetime as dt
from urllib.parse import urlencode
from ..items import InstaTag, InstaPost


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['http://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    api_url = '/graphql/query/'
    query_hash = {
        'posts': '56a7068fea504063273cc2120ffd54f3',
        'tag_posts': "9b498c08113f1e09617a1703c22b2f32",
    }

    def __init__(self, login, enc_password, *args, **kwargs):
        self.tags = ['python']
        self.login = login
        self.enc_password = enc_password
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.enc_password
                },
                headers={'X-CSRFToken': js_data['config']['csrf_token']},
            )
        except AttributeError as e:
            if response.json().get('authenticated'):
                for tag in self.tags:
                    yield response.follow(f'/explore/tags/{tag}/', callback=self.tag_parse,)  #cb_kwargs={'param': tag})

    def tag_parse(self, response):
        js_data = self.js_data_extract(response)['entry_data']['TagPage'][0]['graphql']['hashtag']
        print(1)
        yield InstaTag(
            extracted_time=dt.datetime.utcnow(),
            extracted_data={
                'id': js_data['id'],
                'name': js_data['name'],
                'profile_pic_url': js_data['profile_pic_url'],
            }
        )
        print(2)
        yield from self.posts_parse(response, js_data)
        print(1)

    def insta_api_parse(self, response):
        yield from self.posts_parse(response.json()['data']['hashtag'], response)
        print(4)
    def posts_parse(self, response, js_data):
        if js_data['edge_hashtag_to_media']['page_info']['has_next_page']:
            variables = {
                'tag_name': js_data['name'],
                'first': 100,
                'after': js_data['edge_hashtag_to_media']['page_info']['end_cursor']
            }
        url = f'{self.api_url}?query_hash={self.query_hash["tag_posts"]}&variables={json.dumps(variables)}'
        yield response.follow(
            url,
            callback=self.insta_api_parse,
        )
        print(3)
        yield from self.get_post_item(
            js_data['edge_hashtag_to_media']['edges']
        )

    @staticmethod
    def get_post_item(edges):
        for node in edges:
            yield InstaPost(
                extracted_time=dt.datetime.utcnow(),
                extracted_data=node['node']
            )

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window._sharedData = ")]//text()').get()
        return json.loads(script.replace('window._sharedData = ', '')[:-1])
