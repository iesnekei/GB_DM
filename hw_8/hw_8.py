import scrapy
import json
from new_pars.items import InstagramHandShaker
import datetime as dt


class Hw8Spider(scrapy.Spider):
    name = 'hw_8'
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
    follow_dict = {}

    def __init__(self, login, enc_password, *args, **kwargs):
        self.users = ["royalty_beauty_space", "kenichi_arai"]
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

        except AttributeError:
            if response.json().get('authenticated'):
                for user in self.users:
                    yield response.follow(f'/{user}/', callback=self.target_main_page_parse)

    def target_main_page_parse(self, response):
        user_info = self.js_data_extract(response)["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        yield from self.get_api_of_targets_follower(response, user_info)

    # Work with followers
    def get_api_of_targets_follower(self, response, user_info, variables=None):
        if not variables:
            variables = {
                "id": user_info["id"],
                "first": 100,
            }
        url = f"{self.api_url}?query_hash={self.query_hash['followers']}&variables={json.dumps(variables)}"
        yield response.follow(url, callback=self.get_followers_api, cb_kwargs={"user_info": user_info})

    def get_followers_api(self, response, user_info):
        if b'application/json' in response.headers['Content-Type']:
            data = response.json()
            yield from self.get_followers_list(user_info, data['data']['user']['edge_followed_by']['edges'])
            if data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
                variables = {
                    'id': user_info['id'],
                    'first': 100,
                    'after': data['data']['user']['edge_followed_by']['page_info']['end_cursor'],
                }
                yield from self.get_api_of_targets_follower(response, user_info, variables)
            else:
                yield from self.get_api_of_targets_following(response, user_info)

    # Work with following
    def get_api_of_targets_following(self, response, user_info, variables=None):
        if not variables:
            variables = {
                "id": user_info["id"],
                "first": 100,
            }
        url = f"{self.api_url}?query_hash={self.query_hash['following']}&variables={json.dumps(variables)}"
        yield response.follow(url, callback=self.get_following_api, cb_kwargs={"user_info": user_info})

    def get_following_api(self, response, user_info):
        if b'application/json' in response.headers['Content-Type']:
            data = response.json()
            yield from self.get_following_list(user_info, data['data']['user']['edge_follow']['edges'])
            if data['data']['user']['edge_follow']['page_info']['has_next_page']:
                variables = {
                    'id': user_info['id'],
                    'first': 100,
                    'after': data['data']['user']['edge_follow']['page_info']['end_cursor'],
                }
                yield from self.get_api_of_targets_following(response, user_info, variables)
            else:
                if "followers" in self.follow_dict[user_info["username"]] and "following" in self.follow_dict[
                    user_info["username"]]:
                    yield InstagramHandShaker(
                        user=user_info["username"],
                        extracted_time=dt.datetime.utcnow(),
                        data=self.follow_dict
                    )
                else:
                    yield from self.get_api_of_targets_following(response, user_info, variables=None)
                try:
                    for user in self.follow_dict[user_info["username"]]["connection"]:
                        if user not in self.follow_dict:
                            yield response.follow(f'/{user}/', callback=self.target_main_page_parse)
                except KeyError as e:
                    print(e)

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window._sharedData =")]/text()').get()
        return json.loads(script.replace("window._sharedData =", '')[:-1])

    def get_followers_list(self, user_info, data):
        username = user_info["username"]
        if username not in self.follow_dict:
            self.follow_dict[username] = {}
        if "followers" not in self.follow_dict[username]:
            self.follow_dict[username]["followers"] = []
        for user in data:
            if user not in self.follow_dict[username]["followers"]:
                yield self.follow_dict[username]["followers"].append(user['node']['username'])
        print(f"{username} get followers list")

    def get_following_list(self, user_info, data):
        username = user_info["username"]
        if username not in self.follow_dict:
            self.follow_dict[username] = {}
        if "following" not in self.follow_dict[username]:
            self.follow_dict[username]["following"] = []
        for user in data:
            if user not in self.follow_dict[username]["following"]:
                yield self.follow_dict[username]["following"].append(user['node']['username'])
        print(f"{username} get following list")
