import datetime as dt
import json
import scrapy

from ..items import InstagramFollowersList


class InstagramFriendListSpiderSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    api_url = '/graphql/query/'
    query_hash = {
        'posts': '56a7068fea504063273cc2120ffd54f3',
        'tag_posts': "9b498c08113f1e09617a1703c22b2f32",
        'following': 'd04b0a864b4b54837c0d870b0e77e076',
        'followers': 'c76146de99bb02f6415203be841dd25a'
    }
    follower_list = []
    following_list = []

    def __init__(self, login, enc_password, *args, **kwargs):
        self.tags = ['python', 'программирование', 'developers']
        self.users = ['royalty_beauty_space', ]
        self.login = login
        self.enc_passwd = enc_password
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
                    'enc_password': self.enc_passwd,
                },
                headers={'X-CSRFToken': js_data['config']['csrf_token']},
            )

        except AttributeError as e:
            if response.json().get('authenticated'):
                # for tag in self.tags:
                #     yield response.follow(f'/explore/tags/{tag}/', callback=self.tag_parse)
                for user in self.users:
                    if not self.follower_list:
                        self.follower_list = []
                        self.following_list = []
                    yield response.follow(f'/{user}/', callback=self.target_main_page_parse)

    def target_main_page_parse(self, response, *args, **kwargs):
        js_data = self.js_data_extract(response)
        user_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        variables = {
            "id": int(user_info["id"]),
            "first": 100,
        }
        url = f"{self.api_url}?query_hash={self.query_hash['followers']}&variables={json.dumps(variables)}"
        yield response.follow(url, callback=self.target_followers_parse, cb_kwargs={"user_info": user_info})

    def target_followers_parse(self, response, user_info):
        if b"application/json" in response.headers["Content-Type"]:
            user_info = user_info
            js_data = response.json()
            followers_list_data = js_data["data"]["user"]["edge_followed_by"]["edges"]
            yield from self.extract_followers_list_data(followers_list_data)
            does_it_has_next_page = js_data["data"]["user"]["edge_followed_by"]["page_info"]["has_next_page"]
            end_cursor = js_data["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
            if does_it_has_next_page:
                variables = {
                    "id": user_info["id"],
                    'first': 100,
                    'after': end_cursor,
                }
                url = f"{self.api_url}?query_hash={self.query_hash['followers']}&variables={json.dumps(variables)}"
                yield response.follow(url, callback=self.target_followers_parse, cb_kwargs={"user_info": user_info})

            else:
                variables = {
                    "id": int(user_info["id"]),
                    "first": 100,
                }
                url = f"{self.api_url}?query_hash={self.query_hash['following']}&variables={json.dumps(variables)}"
                yield response.follow(url, callback=self.target_following_parse, cb_kwargs={"user_info": user_info})

    def target_following_parse(self, response, user_info):
        if b"application/json" in response.headers["Content-Type"]:
            user_info = user_info
            js_data = response.json()
            following_list_data = js_data["data"]["user"]["edge_follow"]["edges"]
            yield from self.extract_following_list_data(following_list_data)
            does_it_has_next_page = js_data["data"]["user"]["edge_follow"]["page_info"]["has_next_page"]
            end_cursor = js_data["data"]["user"]["edge_follow"]["page_info"]["end_cursor"]
            if does_it_has_next_page:
                variables = {
                    "id": user_info["id"],
                    'first': 100,
                    'after': end_cursor,
                }
                url = f"{self.api_url}?query_hash={self.query_hash['following']}&variables={json.dumps(variables)}"
                yield response.follow(url, callback=self.target_following_parse, cb_kwargs={"user_info": user_info})

            else:
                yield InstagramFollowersList(
                    target_name = user_info["username"],
                    extracted_time=dt.datetime.utcnow(),
                    followers_list=self.follower_list,
                    following_list=self.following_list
                )

        print(1)

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window._sharedData =")]/text()').get()
        return json.loads(script.replace("window._sharedData =", '')[:-1])

    def extract_followers_list_data(self, followers_list):
        for follower in followers_list:
            yield self.follower_list.append(follower["node"]["username"])

    def extract_following_list_data(self, following_list):
        for following in following_list:
            yield self.following_list.append(following["node"]["username"])
