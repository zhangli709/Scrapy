import json
import re
from urllib.error import URLError

import pymysql
from bs4 import BeautifulSoup
import requests


# def get_page_code(start_url, *, retry_times=3, charsets=('utf-8',)):
#     try:
#         for charset in charsets:
#             try:
#                 html = requests.get(start_url).content.decode(charset)
#                 break
#             except UnicodeDecodeError:
#                 html = None
#     except URLError as e:
#         print('Error', e)
#         if retry_times > 0:
#             return get_page_code(start_url, retry_times=retry_times-1, charsets=charsets)
#         else:
#             return None
#     return html


def main():
    # 待访问列表，此处为单个，可以用while循环遍历
    url_list = ['https://www.zhihu.com/explore']
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/64.0.3282.186 Safari/537.36',
        'Referer': 'https://www.zhihu.com/',
        'Host': 'www.zhihu.com'
    }
    resp = requests.get(url_list[0], headers=header)
    html = resp.content.decode('utf-8')
    conn = pymysql.connect(host='localhost', port=3306,
                           db='crawler', user='root',
                           passwd='123456', charset='utf8')

    link_list = []
    title_list = []
    content_list = []
    bs = BeautifulSoup(html, 'lxml')
    for elem in bs.select('a[class="question_link"]'):
        link_list.append(elem.attrs['href'])
        title_list.append(elem.text)
        resp = requests.get('https://www.zhihu.com'+elem.attrs['href'], headers=header)
        html = resp.content.decode('utf-8')
        bs = BeautifulSoup(html, 'lxml')
        a = bs.select('span[class="RichText ztext CopyrightRichText-richText"] p')
        i_list = ''
        for i in a:
            i_list += i.text
        content_list.append(i_list)
    for i in range(len(link_list)):
        with conn.cursor() as cursor:
            cursor.execute('insert into tb_zhihu(z_url, zquestion,zanswer) values(%s,%s,%s)',
                           (link_list[i], title_list[i],content_list[i]))
        conn.commit()
    conn.close()
    # while len(url_list) > 0 or len(visited_list) > 1000:
    #     # 将 现在的列表中取出一个，放到已经访问过的列表中
    #     current_url = url_list.pop(0)
    #     visited_list.add(current_url)
    #     html = requests.get(current_url, headers=header)
    #     if html:
    #         # 拿到问题，拿到内容答案，正则找到h2的标题，和p里面的内容
    #         link_regex = re.compile()

            # # 链接数据库
            # try:
            #     pass
            # finally:
            #     conn.close()
    print('执行完成')


if __name__ == '__main__':
    main()