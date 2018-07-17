import pickle
from _sha1 import sha1
from enum import Enum
from random import random
from threading import Thread
from time import sleep

import pymongo
import redis
import requests
import zlib
from bs4 import BeautifulSoup
from bson import Binary


class SpiderStatus(Enum):
    IDLE = 0  # 休息
    WORKING =1  # 工作


def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except:
            pass
    return page_html


class Retry(object):
    def __init__(self, *, retry_times=3, wait_secs=5, errors=(Exception)):
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
                except:
                    sleep(self.wait_secs * (random() + 1))
        return wrapper


class Spider(object):

    def __init__(self):
        """
        蜘蛛工作状态
        """
        self.status = SpiderStatus.IDLE

    @Retry
    def fetch(self, current_url, *, charsets=('utf-8',), user_agent=None, proxies=None):
        """
        抓取页面
        :param current_url:
        :param charsets:
        :param user_agent:
        :param proxies:
        :return:
        """
        head= {'user-agent': user_agent} if user_agent else ''
        resp = requests.get(current_url, headers=head, proxies=proxies)
        return decode_page(resp.content, charsets) if resp.status_code == 200 else None

    def parse(self, html_page, *, domain='geyanw.com'):
        soup = BeautifulSoup(html_page, 'lxml')

        title_dict = {}
        a_list = soup.body.find_all('div', {'class': 'listbox'}).dl.dt.a
        for a in a_list:
            title_dict[a.attrs['href']] = a.get_text()

        url_dict = {}
        url_list = soup.body.find_all('div', {'class': 'listbox'}).dl.dd.a
        for url in url_list:
            url_dict[url.attrs['href']] = url.get_text()

            if not redis_client.sismember('visited_urls', url.attrs['href']):
                redis_client.rpush('geyan_task', url.attrs['href'])

    # 抽取title
    def extract_title(self, soup):
        title_dict = {}
        a_list = soup.body.find_all('div', {'class': 'listbox'}).dl.dt.a
        for a in a_list:
            title_dict[a.attrs['href']] = a.get_text()
        return title_dict

    # 抽取url
    def extract_url(self, soup):
        url_dict = {}
        url_list = soup.body.find_all('div', {'class': 'listbox'}).dl.dd.a
        for url in url_list:
            url_dict[url.attrs['href']] = url.get_text()
        return url_dict


    #抽取内容
    def extract_content(self, soup):
        pass


    # 存数据
    def store(self, ):
        mongo_client = pymongo.MongoClient(host='47.106.171.59', port=27017)
        return mongo_client


class SpiderThread(Thread):

    def __init__(self, name, spider):
        super().__init__(name, daemon=True)
        self.spider = spider

    def run(self):
        current_url = redis_client.lpop('geyan_task')
        while not current_url:
            current_url = redis_client.lpop('geyan_task')
        current_url = current_url.decode('utf-8')
        if not redis_client.sismember('visited_ursl', current_url):
            redis_client.sadd('visited_urls', current_url)
            self.spider.status = SpiderStatus.WORKING  # 开始工作
            html_page = self.spider.fetch(current_url)  # 抓取页面
            if html_page not in [None, '']:
                # 加密，存储
                hasher = hasher_proto.copy()
                hasher.update(current_url.encode('utf-8'))
                doc_id = hasher.hexdigest()
                if not geyan_data_coll.find_one({'_id': doc_id}):
                    geyan_data_coll.insert_one({
                        '_id': doc_id,
                        'url': current_url,
                        'page': Binary(zlib.compress(pickle.dumps(html_page)))
                    })

                self.spider.parse(html_page)  # 解析页面
            self.spider.status = SpiderStatus.IDLE  # 工作完成

def is_any_alive(spider_threads):
    return any([spider_thread.spider.status == SpiderStatus.WORKING for spider_thread in spider_threads])


redis_client = redis.Redis(host='47.106.171.59', port=6379, password='123456')  # 链接redis数据库。
mongo_client = pymongo.MongoClient(host='47.106.171.59', port=27017)
db = mongo_client.geyan
geyan_data_coll = db.content
hasher_proto = sha1()


def main():
    if not redis_client.exists('m_sohu_task'):
        redis_client.rpush('m_sohu_task', 'http://m.sohu.com/')
    spider_threads = [SpiderThread('thread-%d' % i, Spider()) for i in range(10)]  # 创建10个线程
    for spider_thread in spider_threads:
        spider_thread.start()
    # 我的队列不为空，任意蜘蛛存活，就不结束
    while not redis_client.llen('m_sohu_task') or is_any_alive(spider_threads):
        pass

    print('Over')


if __name__ == '__main__':
    main()