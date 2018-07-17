# 面向对象来写爬虫
# 使用多进程，对I/O 密集型任务的性能没有实质性的改善
# 多进程 可以利用CPU的多核特性，对计算密集型任务有用
# 对于网络爬虫这种I/O 密集型任务，最好的方式是单线程+ 异步I/O
# 所谓的异步i/0是非阻塞式的i/o操作，也就是在I/O操作时没有中断CPU
# 多线程编程担心  多个线程竞争资源，

import logging
from enum import Enum, unique
from multiprocessing.pool import Pool
from random import random
from time import sleep


from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue

from os import getpid


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
        print(f'Process[{getpid()}][Fetch]:{current_url}')
        headers = {'user-agent': user_agent} if user_agent else {}
        resp = requests.get(current_url, headers=headers, proxies=proxies)
        return decode_page(resp.content, charsets) \
        if resp.status_code == 200 else None

    # 解析页面
    def parse(self, html_page, *, domain='m.sohu.com'):
        soup = BeautifulSoup(html_page, 'lxml')  # 创建一个树结构
        # soup.body.find_all('a')
        url_links = []
        for a_tag in soup.body.select('a[href]'):
            parser = urlparse(a_tag.attrs['href'])
            netloc = parser.netloc or domain
            if netloc != 'javascript' and netloc == domain:
                scheme = parser.scheme or 'http'
                path = parser.path
                query = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query}'

                url_links.append(full_url)
        return url_links


    # 抽取数据
    def extract(self, html_page):
        pass

    # 存储数据
    def store(self, data_dict):
        pass


class SpiderProcess(Process):
    # 爬虫线程
    def __init__(self, spider, tasks_queue):
        """
        守护爬虫线程，爬虫，任务队列
        :param spider:
        :param tasks:
        """
        super().__init__()  # 继承超类，守护线程
        self.daemon = True
        self.spider = spider  # 蜘蛛
        self.tasks_queue = tasks_queue  # url任务

    def run(self):
        """
        线程任务，1.获取页面，2.工作状态-工作 3，抓取页面4.解析页面，5.工作状态-空闲
        通过一个链接，找到其他链接，并把其他链接加到工作队列里。
        :return:
        """
        while True:
            current_url = self.tasks_queue.get()
            visited_urls.add(current_url)
            self.spider.status = SpiderStatus.WORKING # 开始工作
            html_page = self.spider.fetch(current_url)  # 抓取页面
            if html_page not in [None, '']:
                url_links = self.spider.parse(html_page)  # 解析页面
                for url_link in url_links:
                    self.tasks_queue.put(url_link)  # 将链接放到队列里
            self.spider.status = SpiderStatus.IDLE # 工作完成


def is_any_alive(spider_processes):
    """
    任意蜘蛛存活。返回真还是假。
    :param spider_threads:
    :return:
    """
    return any([spider_process.spider.status == SpiderStatus.WORKING for spider_process in spider_processes])


visited_urls = set()  # 设置了一个全局变量，这是很坏的，后期优化


def main():
    task_queue = Queue()  # FIFO   put/get  安全具有锁机制
    task_queue.put('http://m.sohu.com/')
    spider_processes = [SpiderProcess(Spider(), task_queue) for _ in range(10)]  # 生成式创建蜘蛛线

    # pool = Pool(10)
    for spider_process in spider_processes:
        # pool.apply_async(spider_process)
        spider_process.start()

    while not task_queue.empty() or is_any_alive(spider_processes):  # 队列不为空 和 蜘蛛还在工作则程序不能停
        sleep(5)

    # pool.close()
    print('Over!')


if __name__ == '__main__':
    main()