import logging
import pickle
from _sha1 import sha1
from enum import Enum, unique
from random import random
from threading import Thread, current_thread
from time import sleep
from urllib.parse import urlparse

import pymongo
import redis
import requests
import zlib
from bs4 import BeautifulSoup
from bson import Binary


@unique
class SpiderStatus(Enum):
    IDLE = 0  # 休息
    WORKING = 1  # 工作


def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
    return page_html


class Retry(object):
    def __init__(self, *, retry_times=3, wait_secs=5, errors=(Exception,)):
        self.retry_times = retry_times
        self.wait_secs = wait_secs
        self.errors = errors

    def __call__(self, fn):
        """
        装饰器函数，
        :param fn:
        :return:
        """

        def wrapper(*args, **kwargs):
            for _ in range(self.retry_times):
                try:
                    return fn(*args, **kwargs)
                except self.errors as e:
                    logging.error(e)
                    logging.info('[Rery]')
                    sleep(self.wait_secs * (random() + 1))

        return wrapper


class Spider(object):

    def __init__(self):
        """
        蜘蛛工作状态
        """
        self.status = SpiderStatus.IDLE

    @Retry()
    def fetch(self, current_url, *, charsets=('utf-8',), user_agent=None, proxies=None):
        thread_name = current_thread().name  # 线程命名
        print(f'[{thread_name}]:{current_url}')
        head = {'user-agent': user_agent} if user_agent else ''
        resp = requests.get(current_url, headers=head, proxies=proxies)
        return decode_page(resp.content, charsets) if resp.status_code == 200 else None

    def parse(self, html_page, *, domain='geyanw.com'):
        soup = BeautifulSoup(html_page, 'lxml')  # 创建一个树结构
        # 用urlparse 处理链接，变成正规的url
        for a_tag in soup.body.select('a[href]'):
            parser = urlparse(a_tag.attrs['href'])
            scheme = parser.scheme or 'https'
            netloc = parser.netloc or domain
            if netloc != 'javascript' and netloc == domain:
                path = parser.path
                query = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query}'
                if not redis_client.sismember('visited_urls', full_url):
                    redis_client.rpush('geyan_task', full_url)

    # 抽取数据,标题和内容P
    def extract(self, html_page):
        soup = BeautifulSoup(html_page, 'lxml')
        title = soup.find('div', id='p_left').h2.get_text()
        p_content = soup.find('div', id='p_left').find_all('p')
        p_set = []
        for p in p_content:
            if p.get_text() not in ['', '&nbsp;', '\xa0']:
                p_set.append(p.get_text())
        my_tuple = (title, p_set)
        return my_tuple


class SpiderThread(Thread):

    def __init__(self, name, spider):
        super().__init__(name=name, daemon=True)
        self.spider = spider

    def run(self):
        while True:
            current_url = redis_client.lpop('geyan_task')
            while not current_url:
                current_url = redis_client.lpop('geyan_task')
            current_url = current_url.decode('gb2312')
            if not redis_client.sismember('visited_urls', current_url):
                redis_client.sadd('visited_urls', current_url)
                self.spider.status = SpiderStatus.WORKING  # 开始工作
                html_page = self.spider.fetch(current_url,charsets=('utf-8', 'gb2312', 'gbk'))  # 抓取页面
                if html_page not in [None, '']:
                    # 加密，存储
                    my_tuple = self.spider.extract(html_page)
                    my_dict = {
                        'title': my_tuple[0],
                        'page': my_tuple[1]
                    }
                    geyan_data_coll.insert_one(my_dict)
                self.spider.status = SpiderStatus.IDLE  # 工作完成


def is_any_alive(spider_threads):
    return any([spider_thread.spider.status == SpiderStatus.WORKING for spider_thread in spider_threads])


redis_client = redis.Redis(host='47.106.171.59', port=6379, password='123456')  # 链接redis数据库。
mongo_client = pymongo.MongoClient(host='47.106.171.59', port=27017)
db = mongo_client.geyan
geyan_data_coll = db.content


def main():
    spider = Spider()
    html = spider.fetch('https://geyanw.com/', charsets=('utf-8', 'gb2312', 'gbk'))
    spider.parse(html)
    spider_threads = [SpiderThread('thread-%d' % i, Spider()) for i in range(10)]  # 创建10个线程
    for spider_thread in spider_threads:
        spider_thread.start()
    # 我的队列不为空，任意蜘蛛存活，就不结束
    while not redis_client.llen('geyan_task') or is_any_alive(spider_threads):
        pass

    print('Over')


if __name__ == '__main__':
    main()
