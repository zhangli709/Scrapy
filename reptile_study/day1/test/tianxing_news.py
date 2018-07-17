import json
from urllib.error import URLError
from urllib.request import urlopen

import requests


# def get_page_code(start_url, *, retry_times=3, charsets=('utf-8',)):
#     try:
#         for charset in charsets:
#             try:
#                 html = urlopen(start_url).read().decode(charset)
#                 break
#             except UnicodeDecodeError:
#                 html = None
#     except URLError as e:
#         print('Error', e)
#         if retry_times > 0:
#             return get_page_code(start_url, retry_times=retry_times-1,charsets=charsets)
#         else:
#             return None
#     return html
from bs4 import BeautifulSoup


def main():
    # 拿到页面里的10个url
    url = ('http://api.tianapi.com/guonei/?key=81085f5747a59581327b29d1bccfb925&num=10')
    resp = requests.get(url)
    mydic = json.loads(resp.text)
    url_lists = []
    for list in mydic['newslist']:
        url_lists.append(list['url'])

    url = url_lists[1]
    print(url)
    resp = requests.get(url)
    html = resp.content.decode('gbk')
    bs = BeautifulSoup(html, 'lxml')
    # print(bs)
    try:
        bs1 = bs.find('div', {'class': 'mutu-news'})
        # print(bs1)
        # 正则筛选，选出里面的url和标题
        if bs1:
            for elem in bs1.select('a'):
                link_url = elem.attrs['href']
                link_title = elem.get_text()
                print(link_url)
                print(link_title)

        else:
            return None
    except:
        return None


if __name__ == '__main__':
    main()