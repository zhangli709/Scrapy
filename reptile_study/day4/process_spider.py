# 面向对象来写爬虫
from enum import Enum, unique


# 枚举，
from queue import Queue
from threading import Thread


@unique
class SpiderStatus(Enum):
    # 工作状态
    IDLE = 0
    WORKING = 1


class SpiderThread(Thread):
    # 爬虫线程

    def __init__(self, spider, tasks):
        super().__init__(daemon=True)
        self.spider = spider
        self.tasks = tasks

    def run(self):
        pass


class Spider(object):

    def __init__(self):
        self.status = SpiderStatus.IDLE

    # 抓取页面
    def fetch(self, current_url):
        pass

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
    # 任意蜘蛛存活。
    return any([spider_thread.spider.status == SpiderStatus.WORKING for spider_thread in spider_threads])

def main():
    task_queue = Queue()  # 队列FIFO,先进先出。
    # task_queue.put('http://m.sohu.com/')
    spider_threads = [SpiderThread(Spider(), task_queue) for _ in range(10)]  # 创建10个线程
    for spider_thread in spider_threads:
        spider_thread.start()
    # 我的队列不为空，获取任意蜘蛛存活，就不结束
    while not task_queue.empty() or is_any_alive(spider_threads):
        pass

    print('Over')


if __name__ == '__main__':
    main()