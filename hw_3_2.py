import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Table,

)


from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
url = ' https://geekbrains.ru/posts/'

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, unique=False, nullable=False)
    url = Column(String, unique=True, nullable=False)
    img_url = Column(String, unique=False, nullable=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    data = Column(DateTime, unique=False, nullable=False)
    author = relationship('Users', back_populates='posts')
    tag_rel = relationship('Tag_and_post', back_populates='post_rel')

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=False, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    url = Column(String, unique=True, nullable=False)
    posts = relationship('Post')

class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    post = relationship('Tag_and_post', back_populates='tag')

class Tag_and_post(Base):
    __tablename__ = 'tag_and_post'
    id = Column(Integer, autoincrement=True, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), unique=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), unique=False)
    tag = relationship('Tags')
    post_rel = relationship('Post')





class GB:

    def __init__(self, income_url):
        self.income_url = income_url
        self.post_list = []
        self.month = ['января',
                      'февраля',
                      'марта',
                      'апреля',
                      'мая',
                      'июня',
                      'июля',
                      'августа',
                      'сентября',
                      'октября',
                      'ноября',
                      'декабря']

    def get_soup(self, url):
        response = requests.get(self.income_url)
        self.soup = BeautifulSoup(response.text, 'lxml')

    def get_post(self):
        self.get_posts = self.soup.findAll('div', attrs={'class': 'post-item'})

    def get_info(self):
        post_dict = {}
        for i in range(0, len(self.get_posts)):
            post_dict[i] = {}
            post_dict[i]['url'] = self.get_posts[i].findAll('a', href=True)[0]['href']
            post_dict[i]['title'] = self.get_posts[i].find('a', attrs={'class': 'post-item__title'}).text
            post_dict[i]['first_img'] = self.get_posts[i].find('img', attrs={'class': 'img_preview'})['src']
            post_dict[i]['post_date'] = (self.get_posts[i].find('div', attrs={'class': 'm-t-xs'}).text).split()
            post_dict[i]['post_date'] = datetime.strptime((post_dict[i]['post_date'][0]
                                                           + '-' + f"{(self.month.index(post_dict[i]['post_date'][1]) + 1)}"
                                                           + '-' + post_dict[i]['post_date'][2]
                                                           ), '%d-%m-%Y').date()

            header = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15'}
            info_from_post = requests.get(('https://geekbrains.ru/' + post_dict[i]['url']), headers=header)
            post_soup = BeautifulSoup(info_from_post.text, 'lxml')
            post_dict[i]['user'] = post_soup.findAll('div', attrs={'class': 'm-t'})[1].find('div', attrs={
                'class': 'text-lg'}).text
            post_dict[i][
                'user_id'] = int((post_soup.findAll('div', attrs={'class': 'm-t'})[1].find('a', href=True)['href']).replace('/users/', '')) #f"https://geekbrains.ru/{}"
            post_dict[i]['tags'] = post_soup.findAll('i')[2]['keywords'].split()
            post_dict[i]['post_comments_id'] = post_soup.findAll('div', {'class': 'm-t-xl'})[0].find('comments')[
                'commentable-id']
            comments = requests.get(
                f"https://geekbrains.ru/api/v2/comments?commentable_type=Post&commentable_id={post_dict[i]['post_comments_id']}&order=desc")
            data: dict = comments.json()
            update = []
            for j in range(0, len(data)):
                user = data[j]['comment']['user']['id']
                body = data[j]['comment']['body']
                update.append({'user_id': user, 'text': body})
            post_dict[i]['comments'] = update
            self.post_list.append(post_dict[i])

    def parse_all_pages(self):
        pages = 1
        for i in range(1, pages):
            if i == 1:
                self.get_soup(url=self.income_url)
                self.get_post()
                self.get_info()
            else:
                new_url = self.income_url + f'?page={i}'
                self.get_soup(new_url)
                self.get_post()
                self.get_info()

        print(1)


if __name__ == '__main__':
    hw_3 = GB(url)
    hw_3.parse_all_pages()
    print(1)
