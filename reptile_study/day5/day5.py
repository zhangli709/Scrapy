import logging
import re
from enum import Enum
from random import random
from threading import Thread, current_thread
from time import sleep

import pymongo
import redis
import requests
from bs4 import BeautifulSoup


class SpiderStatus(Enum):
    WORKING = 1
    NOT_WORKING = 0


class Retry(object):
    def __init__(self, retry_time=3, wait_secs=5, errors=(Exception,)):
        self.retry_time = retry_time
        self.wait_secs = wait_secs
        self.errors = errors

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            for _ in range(self.retry_time):
                try:
                    return fn(*args, **kwargs)
                except self.errors as e:
                    logging.error(e)
                    sleep(self.wait_secs * (1 + random()))
            return None

        return wrapper


def decode_page(html_page, charsets):
    page_return = None
    for charset in charsets:
        try:
            page_return = html_page.decode(charset)
            break
        except UnicodeDecodeError:
            pass
    return page_return


class GeyanSpider(object):

    def __init__(self):
        self.status = SpiderStatus.NOT_WORKING

    @Retry()
    def fetch(self, current_url, decode=('utf-8', 'gbk', 'gb2312'),
              user_agent=None, proxies=None):
        thread_name = current_thread().name
        print(f'[{thread_name} Fetch]:{current_url}')
        headers = {'user-agent': user_agent} if user_agent else {}
        resp = requests.get(current_url, headers=headers, proxies=proxies)
        return decode_page(resp.content, decode) \
            if resp.status_code == 200 else None

    def parse(self, html_page, *, domain='https://geyanw.com'):
        if html_page not in [None, '']:
            soup = BeautifulSoup(html_page, 'lxml')
            for a_tag in soup.select('a[href]'):
                url = a_tag.attrs['href']
                if url.startswith('/'):
                    fullurl = domain + url
                    if not redis_client.sismember('geyan_visited_urls', fullurl):
                        redis_client.rpush('geyan_tasks', fullurl)

    def extract(self, html_page, current_url):
        soup = BeautifulSoup(html_page, 'lxml')
        title = soup.select_one('.title').text.strip('\n')
        contents = []
        i = 1
        for content in soup.select('.content p'):
            if content.text.strip() not in [None, '']:
                real_con = content.text.split('.', 1) if \
                    content.text.find('.') != -1 else content.text.split('、', 1)
                # print(real_con)
                if len(real_con) > 1:
                    contents.append(list(real_con))
                else:
                    contents.append([str(i), real_con[0]])
                    i += 1
        # print(contents)
        if 'lizhimingyan' in current_url:
            real_class = '励志名言'
        elif 'renshenggeyan' in current_url:
            real_class = '人生格言'
        elif 'mingyanjingju' in current_url:
            real_class = '名言警句'
        elif 'mingrenmingyan' in current_url:
            real_class = '名人名言'
        elif 'dushumingyan' in current_url:
            real_class = '读书名言'
        elif 'jingdianmingyan' in current_url:
            real_class = '经典名言'
        elif 'aiqingmingyan' in current_url:
            real_class = '爱情名言'
        elif 'jingdianduanju' in current_url:
            real_class = '经典段句'
        elif 'juzi' in current_url:
            real_class = '句子'
        elif 'lizhiwenzhang' in current_url:
            real_class = '励志文章'
        else:
            real_class = '其他未分类'
        create_time = soup.select_one('.info').text.strip('\n')
        data = {'url': current_url,
                'title': title,
                'create_time': create_time,
                'class': real_class,
                'content': dict(contents),
                }
        # print(data)
        return data

    def store(self, data_dict):
        # print(data_dict)
        data_coll.insert_one(data_dict)
        print('success')


class SpiderThread(Thread):

    def __init__(self, spider, name):
        super().__init__(name=name, daemon=True)
        self.spider = spider

    def run(self):
        while True:
            current_url = redis_client.lpop('geyan_tasks')
            while not current_url:
                current_url = redis_client.lpop('geyan_tasks')
            while redis_client.sismember('geyan_visited_urls', current_url):
                current_url = redis_client.lpop('geyan_tasks')
            if current_url:
                current_url = current_url.decode('utf-8')
                self.spider.status = SpiderStatus.WORKING
                redis_client.sadd('geyan_visited_urls', current_url)
                html_page = self.spider.fetch(current_url)
                pattern1 = re.compile('.*/\d+\.html$')
                m = re.match(pattern1, current_url)
                # print(m)
                if html_page:
                    if m != None:
                        data = self.spider.extract(html_page, current_url)
                        self.spider.store(data)
                    else:
                        self.spider.parse(html_page)
                self.spider.status = SpiderStatus.NOT_WORKING


def is_any_spider_alive(spider_threads):
    # 只要列表中存在任意一个true就是true
    return any([spider_thread.spider.status == SpiderStatus.WORKING
                for spider_thread in spider_threads])


redis_client = redis.Redis(host='47.106.81.203', port=1122, password='admin@123')
mongo_client = pymongo.MongoClient(host='47.106.81.203', port=27017)
db = mongo_client.geyanw
data_coll = db.geyandata

start_url = 'https://geyanw.com/'


def main():
    if not redis_client.exists('geyan_tasks'):
        redis_client.rpush('geyan_tasks', start_url)

    geyan_threads = [SpiderThread(GeyanSpider(), 't-%d' % i) for i in range(10)]

    for geyan_thread in geyan_threads:
        geyan_thread.start()
    # print(redis_client.llen('geyan_tasks'), is_any_spider_alive(geyan_threads))
    while redis_client.llen('geyan_tasks') or is_any_spider_alive(geyan_threads):
        pass

    print('Get All Complete!')


if __name__ == '__main__':
    main()
