import re

import pymysql
import requests
from bs4 import BeautifulSoup


def main():
    head= {'user-agent': 'Baiduspider'}
    proxies = {
        'https': 'https://101.251.232.221:3128'
    }
    html = requests.get('http://sports.sohu.com/nba_a.shtml', headers=head, proxies=proxies)

    # conn = pymysql.connect(
    #     host='localhost',port=3306,
    #     user='root', password='123456',
    #     charset='utf-8',database='test'
    # )

    html1 = html.content
    # html1 = html.content.decode('gbk')
    bs_obj = BeautifulSoup(html1, 'lxml')
    bs_obj = bs_obj.find_all('a')
    bs_obj = bs_obj.find_all('a', {'href': ''})
    bs_obj = bs_obj.find_all('^$')
    bs_obj = bs_obj.find_all('a',{'href': '^$'})
    bs_obj = bs_obj.find_all('a', {'href': re.compile("//./")})
    # bs_obj.attrs['href']
    for a in bs_obj:
        a.attrs['href']
        print(a.get_text())


if __name__ == '__main__':
    main()