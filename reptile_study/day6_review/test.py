from enum import Enum, unique
from random import random
from threading import Thread, current_thread
from time import sleep
from urllib.parse import urlparse

import redis
import requests
from bs4 import BeautifulSoup


@unique
class SpiderStatus(Enum):
    IDLE = 0
    WORKING = 1


def decode_page(html,charsets=('utf-8',)):
    html = None
    for charset in charsets:
        try:
            html.content.decode(charset)
            break
        except UnicodeDecodeError:
            pass
    return html


class Retry(object):
    def __init__(self,*, retry_times=3, wait_secs=5, error=(Exception,)):
        self.retry_times = retry_times
        self.wait_secs = wait_secs
        self.error = error

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args,**kwargs)
            except self.error as e:
                sleep((random()+1) * self.wait_secs)
        return wrapper


class Spider(object):

    def __init__(self):
        self.spider_status = SpiderStatus.IDLE

    # 抓取页面
    @Retry()
    def fetch(self, url,*, charsets=('utf-8',)):
        thread_name = current_thread().name
        print(f'[{thread_name}]:{url}')
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0'}
        resp = requests.get(url, headers=headers)
        return decode_page(resp, charsets) if resp.status_code == 200 else None

    # 解析页面
    def parse(self, html_page, *, domain='geyanw.com'):
        soup = BeautifulSoup(html_page, 'lxml')
        for a_tag in soup.select('a[href]'):
            parser = urlparse(a_tag.attrs['href'])  # 解析url
            scheme = parser.scheme or 'http'  # 为空时使用后面这个
            netloc = parser.netloc or domain
            if netloc != 'javascript':
                path = parser.path
                query = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query}'
                if not redis_client.sismember('visited_urls', full_url):
                    redis_client.rpush('geyanw_task', full_url)

    # 抽取数据
    def extract(self, html_page):
        pass

    # 存储数据
    def store(self, mydict):
        pass


class SpiderThread(Thread):
    def __init__(self, name, spider):
        super().__init__(name=name, daemon=True)
        self.spider = spider

    def run(self):
        while True:
            current_url = redis_client.lpop('geyanw_task')
            while not current_url:
                current_url = redis_client.lpop('geyanw_task')
            current_url = current_url.decode('utf-8')
            if not redis_client.sismember('visited_urls', current_url):
                redis_client.sadd('visited_urls', current_url)
                self.spider.status = SpiderStatus.WORKING
                html_page = self.spider.fetch(current_url)  # 抓取页面
                if html_page not in ['', None]:
                    self.spider.parse(html_page)  # 存储url,
                self.spider.status = SpiderStatus.IDLE


def is_any_alive(spider_threads):
    return any([spider_thread.spider.status==SpiderStatus.WORKING  for spider_thread in spider_threads])


redis_client = redis.Redis(host='47.106.171.59', port='6379',password=123456)


def main():
    if not redis_client.exists('geyanw_task'):
        redis_client.rpush('geyanw_task', 'http://geyanw.com')
    spider_threads = [SpiderThread('thread-%d' % i, Spider()) for i in range(10)]
    for spider_thread in spider_threads:
        spider_thread.start()
    while not redis_client.llen('geyanw_task') or is_any_alive(spider_threads):
        pass
    print('Over!')


if __name__ == '__main__':
    main()