# 面向对象来写爬虫
import logging
from enum import Enum, unique
from random import random
from time import sleep


from queue import Queue
from threading import Thread

# 枚举，
import requests


@unique
class SpiderStatus(Enum):
    # 工作状态
    IDLE = 0
    WORKING = 1


class SpiderThread(Thread):
    # 爬虫线程

    def __init__(self, spider, tasks_queue):
        """
        守护爬虫线程，爬虫，任务队列
        :param spider:
        :param tasks:
        """
        super().__init__(daemon=True)  # 继承超类，守护线程
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
            self.spider.status = SpiderStatus.WORKING # 开始工作
            html_page = self.spider.fetch(current_url)  # 抓取页面
            if html_page not in [None, '']:
                url_links = self.spider.parse(html_page)  # 解析页面
                self.tasks_queue += url_links  # 将链接放到队列里
            self.spider.status = SpiderStatus.IDLE # 工作完成


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
                    sleep((random() + 1) * self.wait_secs)

        return wrapper


class Spider(object):

    def __init__(self):
        self.status = SpiderStatus.IDLE  # 调用蜘蛛状态


    # 抓取页面
    @Retry()
    def fetch(self, current_url, *, charsets=('utf-8',), user_agent=None, proxies=None):
        headers = {'user_agent': user_agent} if user_agent else {}
        resp = requests.get(current_url, headers=headers, proxies=proxies)
        return decode_page(resp.content, charsets) \
        if resp.status_code == 200 else None

    # 解析页面
    def parse(self, html):
        pass

    # 抽取数据
    def extract(self, html_page):
        pass

    # 存储数据
    def store(self, data_dict):
        pass


def is_any_alive(spider_threads):
    """
    任意蜘蛛存活。返回真还是假。
    :param spider_threads:
    :return:
    """
    return any([spider_thread.spider.status == SpiderStatus.WORKING for spider_thread in spider_threads])


def main():
    task_queue = Queue()  # 队列FIFO,先进先出,内部有安全锁，不会产生安全问题。
    # task_queue.put('http://m.sohu.com/')
    spider_threads = [SpiderThread(Spider(), task_queue) for _ in range(10)]  # 创建10个线程
    for spider_thread in spider_threads:
        spider_thread.start()
    # 我的队列不为空，任意蜘蛛存活，就不结束
    while not task_queue.empty() or is_any_alive(spider_threads):
        pass

    print('Over')


if __name__ == '__main__':
    main()