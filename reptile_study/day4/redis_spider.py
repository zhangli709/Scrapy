# 面向对象来写爬虫

import logging
import pickle
from enum import Enum, unique
from hashlib import sha1
from random import random
from time import sleep

from threading import Thread, current_thread
from urllib.parse import urlparse

import pymongo
import redis
import requests
import zlib
from bs4 import BeautifulSoup
from bson import Binary


@unique
class SpiderStatus(Enum):
    # 工作状态
    IDLE = 0
    WORKING = 1


def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
            # logging.error('Decode:', error)
    return page_html


class Retry(object):
    # 装饰器类，

    def __init__(self, *, retry_times=3, wait_secs=5, errors=(Exception,)):
        """
        :param retry_times: 重试次数
        :param wait_secs: 最小避让时间
        :param errors: 异常
        """
        self.retry_times = retry_times
        self.wait_secs = wait_secs
        self.errors = errors

    def __call__(self, fn):
        """
        装饰器方法
        :param fn:被装饰函数
        :return: 装饰后的函数
        """
        def wrapper(*args, **kwargs):
            for _ in range(self.retry_times):
                try:
                    return fn(*args, **kwargs)
                except self.errors as e:
                    logging.error(e)
                    logging.info('[Retry]')
                    sleep((random() + 1) * self.wait_secs)

        return wrapper


class Spider(object):

    def __init__(self):
        self.status = SpiderStatus.IDLE  # 调用蜘蛛状态

    # 抓取页面
    @Retry()
    def fetch(self, current_url, *, charsets=('utf-8',), user_agent=None, proxies=None):
        thread_name = current_thread().name  # 线程命名
        print(f'[{thread_name}]:{current_url}')
        headers = {'user-agent': user_agent} if user_agent else {}
        resp = requests.get(current_url, headers=headers, proxies=proxies)
        return decode_page(resp.content, charsets) \
        if resp.status_code == 200 else None

    # 解析页面
    def parse(self, html_page, *, domain='m.sohu.com'):
        soup = BeautifulSoup(html_page, 'lxml')  # 创建一个树结构
        # 用urlparse 处理链接，变成正规的url
        for a_tag in soup.body.select('a[href]'):
            parser = urlparse(a_tag.attrs['href'])
            scheme = parser.scheme or 'http'
            netloc = parser.netloc or domain
            if netloc != 'javascript' and netloc == domain:
                path = parser.path
                query = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query}'
                if not redis_client.sismember('visited_urls', full_url):
                    redis_client.rpush('m_sohu_task', full_url)

    # 抽取数据
    def extract(self, html_page):
        pass

    # 存储数据
    def store(self, data_dict):
        pass


class SpiderThread(Thread):
    # 爬虫线程
    def __init__(self, name, spider):
        """
        守护爬虫线程，爬虫，任务队列
        :param spider:
        :param tasks:
        """
        super().__init__(name=name, daemon=True)  # 继承超类，守护线程
        self.spider = spider  # 蜘蛛

    def run(self):
        """
        线程任务，1.获取页面，2.工作状态-工作 3，抓取页面4.解析页面，5.工作状态-空闲
        通过一个链接，找到其他链接，并把其他链接加到工作队列里。
        :return:
        """
        while True:
            current_url = redis_client.lpop('m_sohu_task')
            while not current_url:
                current_url = redis_client.lpop('m_sohu_task')
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
                    if not sohu_data_coll.find_one({'_id': doc_id}):
                        sohu_data_coll.insert_one({
                            '_id': doc_id,
                            'url': current_url,
                            'page': Binary(zlib.compress(pickle.dumps(html_page)))
                        })

                    self.spider.parse(html_page)  # 解析页面
                self.spider.status = SpiderStatus.IDLE # 工作完成


def is_any_alive(spider_threads):
    """
    任意蜘蛛存活。返回真还是假。
    :param spider_threads:
    :return:
    """
    return any([spider_thread.spider.status == SpiderStatus.WORKING for spider_thread in spider_threads])


# 全局变量，宜少不宜多。
redis_client = redis.Redis(host='47.106.171.59', port=6379, password='123456')  # 链接redis数据库。
mongo_client = pymongo.MongoClient(host='47.106.171.59', port=27017)  # 链接mongo数据库。
db = mongo_client.msohu  # 创建sohu集合
sohu_data_coll = db.webpages
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