# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from threading import Thread
import time


class Downloader(object):
    def __init__(self, target):
        self._url = target

    """获取每一章节的url"""

    def get_url(self):
        req = requests.get(url=self._url)
        bf = BeautifulSoup(req.text, from_encoding='utf-8')
        div = bf.find_all('div', id='list')
        a_bf = BeautifulSoup(str(div[0]), from_encoding='utf-8')
        a = a_bf.find_all('a')
        return a

    """获取每一章正文内容"""

    def get_content(self, content_url, title):
        req = requests.get(url=content_url)
        bf = BeautifulSoup(req.text, from_encoding='utf-8')
        text_content = bf.find_all('div', id='content')
        content = text_content[0].text.replace('　　', '\n\n　　').replace('    ', '\n\n　　')
        txt = title + '\n' + content
        return txt

    """写入文件"""

    def write_txt(self, filename, txt):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(txt)


def main():
    class WriteThread(Thread):
        def __init__(self, first_num, last_num, thread_num, txt=''):
            super().__init__()
            self._first_num = first_num
            self._last_num = last_num
            self._txt = txt
            self._thread_num = thread_num

        def run(self):
            nonlocal txt_list, is_end_list
            print('线程%d启动' % self._thread_num)
            for i in range(9 + self._first_num, self._last_num):
                title = a[i].string
                content_url = a[i].get('href')
                self._txt += d.get_content(content_url, title)
            print('%s--%s完成' % (a[9 + self._first_num].string, a[self._last_num - 1].string))
            is_end_list[self._thread_num - 1] = True
            txt_list[self._thread_num - 1] = self._txt

    def all_end(thread_num):
        nonlocal is_end_list
        for i in range(thread_num):
            if is_end_list[i] == 'False':
                return False
        return True

    target = 'https://www.biquge5200.com/42_42714/'
    d = Downloader(target)
    a = d.get_url()
    running = True
    first_num = 0
    last_num = 109
    filename = '不朽凡人.txt'
    thread_num = 0
    txt_list = ['' for _ in range(100)]
    is_end_list = ['False' for _ in range(100)]
    start_time = time.time()
    while running:
        thread_num += 1
        txt = WriteThread(first_num, last_num, thread_num)
        txt.start()
        if len(a) - last_num >= 100:
            first_num = last_num - 9
            last_num += 100
        elif 0 < len(a) - last_num < 100:
            first_num = last_num - 9
            last_num = len(a)
        else:
            running = False
    while True:
        if all_end(thread_num):
            for txt in txt_list:
                if txt != '':
                    d.write_txt(filename, txt)
            end_time = time.time()
            print('耗时%ds' % (end_time - start_time))
            return


if __name__ == '__main__':
    main()
