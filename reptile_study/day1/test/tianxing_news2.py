import json
from urllib.error import URLError
from bs4 import BeautifulSoup
import requests


def get_page_code(start_url, *, retry_times=3, charsets=('utf-8',)):
    try:
        for charset in charsets:
            try:
                html = requests.get(start_url).content.decode(charset)
                break
            except UnicodeDecodeError:
                html = None
    except URLError as e:
        print('Error', e)
        if retry_times > 0:
            return get_page_code(start_url, retry_times=retry_times-1, charsets=charsets)
        else:
            return None
    return html


def main():
    # 拿到页面里的10个url
    url = ('http://api.tianapi.com/guonei/?key=81085f5747a59581327b29d1bccfb925&num=10')
    resp = requests.get(url)
    mydic = json.loads(resp.text)
    url_lists = []
    for list1 in mydic['newslist']:
        url_lists.append(list1['url'])
    print(url_lists)
    visited_list = set([])
    mydict = {}
    n = 0
    while len(url_lists) > 0 and n < 100:
        n += 1
        current_url = url_lists.pop(0)
        visited_list.add(current_url)
        html = get_page_code(current_url, charsets=('utf-8', 'gbk'))
        if html:
            bs = BeautifulSoup(html, 'lxml')
            if bs.find('div', {'class': 'mutu-news'}):
                bs1 = bs.find('div', {'class': 'mutu-news'})
                if bs1:
                    for elem in bs1.select('a'):
                        link_url = elem.attrs['href']
                        link_title = elem.get_text()
                        url_lists +=link_url
                        print(n)
                        print(link_url)
                        mydict[link_title] = link_url
                else:
                    pass
            else:
                pass
        else:
            pass
    print(mydict)


if __name__ == '__main__':
    main()