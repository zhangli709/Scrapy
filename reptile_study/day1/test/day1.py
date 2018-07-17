import re
from urllib.error import URLError
from urllib.request import urlopen

import pymysql


def get_page_code(start_url, *, retry_times=3, charsets=('utf-8',)):
    """
    请求一个页面，传入起始链接，最多请求三次，并传入解码规则
    :param start_url:
    :param retry_times:
    :param charset:
    :return:返回一个页面
    """
    try:
        for charset in charsets:
            try:
                html = urlopen(start_url).read().decode(charset)
                break
            except UnicodeDecodeError:
                html = None
    except URLError as ex:
        print('Error', ex)
        if retry_times > 0:
            return get_page_code(start_url, retry_times=retry_times - 1, charsets=charsets)
        else:
            return None
    return html


def main():
    url_list = ['http://sports.sohu.com/nba_a.shtml']
    #  判断，将需要爬取的放到一个列表，将已经爬取过的也放到一个集合，判断，去重
    visited_list = set({})
    while len(url_list) > 0:
        current_url = url_list.pop(0)
        visited_list.add(current_url)
        # 调用方法，获取页面
        html = get_page_code(current_url, charsets=('gbk','utf-8'))
        # 使用惰性匹配，拿到页面里所有的匹配正则的url
        if html:
            link_regex = re.compile(r'<a[^>]+test=a\s[^>]*href=["\'](\S*)["\']', re.IGNORECASE)
            link_list = re.findall(link_regex, html)
            url_list += link_list

            # 链接数据库
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                db='crawler',
                user='root',
                passwd='123456',
                charset='utf8'
            )
            try:
                for link in link_list:
                    # 把之前爬取的url里面的标题存到数据库里。深度搜索。纵向。广度搜索，横向。
                    if link not in visited_list:
                        print(link)
                        html1 = get_page_code(link)
                        title_regex = re.compile(r'<h1>(.*)<span',re.IGNORECASE)
                        match_list = re.findall(title_regex, html1)[0]
                        # 将数据保存到数据库里
                        if len(match_list) > 0:
                            title = match_list
                        with conn.cursor() as cursor:
                            cursor.execute('insert into tb_result (rtitle, rurl) values (%s, %s)', (title, link))
                        conn.commit()
            finally:
                conn.close()
            print('执行完成')


if __name__ == '__main__':
    main()