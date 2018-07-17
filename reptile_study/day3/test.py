from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup
import redis
import requests


# 解码
def decode_func(text, charsets=('utf-8',)):
    html = None
    for charset in charsets:
        try:
            html = text.decode(charset)
            break
        except:
            pass
    return html


# 拿页面
def get_html(url, *, retry_times=3,charsets=('utf-8',)):
    head = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0'
    }
    html = None
    try:
        # html = decode_func(requests.get(url, headers=head).content, charsets)
        html = decode_func(urlopen(url).read(), charsets)

    except:
        if retry_times > 0:
            return get_html(url, retry_times=retry_times-1, charsets=charsets)
    return html


# 爬虫函数，实现url的跳转，和需要内容筛选的拿取，存储
def start_crawl(seed_url, max_depth=3):
    # 链接数据库
    db = redis.Redis(host='47.106.171.59', port='6379', password='123456')
    # 起始url
    url_list = [seed_url]
    visited_list = {seed_url:0}
    while url_list:
        current_url = url_list.pop(0)
        depth = visited_list[current_url]
        # 控制深度
        if depth != max_depth:
            # 拿页面
            page_html = BeautifulSoup(get_html(current_url, charsets=('utf-8','gbk', 'gb2312')), 'lxml')
            # 拿页面里的url.
            a_list = page_html.find_all('a')
            for a in a_list:
                if a.attrs['href']:
                    a_href = a.attrs['href']
                    if a_href not in visited_list:
                        url_list.append(a_href)
                        visited_list[a_href] = depth + 1
                        page_html = get_html(a_href, charsets=('utf-8','gbk', 'gb2312'))
                        if page_html

def main():
    pass

if __name__ == '__main__':
    main()