import pymysql
from bs4 import BeautifulSoup
import requests
import re


def main():
    # 拿到网页内容
    resp = requests.get('http://sports.sohu.com/nba_a.shtml')
    # 对网页解码
    html = resp.content.decode('gbk')
    # 使用数据转换的第三方库
    bs = BeautifulSoup(html, 'lxml')

    conn = pymysql.connect(
        host='localhost',
        port=3306,
        db='crawler',
        user='root',
        passwd='123456',
        charset='utf8'
    )

    # 查找内容，使用第三方库的查找方法，css选择器
    try:
        for elem in bs.select('a[test=a]'):
            # 获取链接
            link_url = elem.attrs['href']
            # 请求网页
            resp = requests.get(link_url)
            # 获取页面，使用默认utf-8解码，调用第三方库。
            bs_sub = BeautifulSoup(resp.content, 'lxml')
            # 筛选出h1标题中的内容，打印出来。
            # print(re.sub(r'[\r\n]', '', bs_sub.select_one('h1').text))
            title = bs_sub.select_one('h1').text
            with conn.cursor() as cursor:
                cursor.execute('insert into tb_result (rtitle, rurl) values (%s, %s)', (title, link_url))
            conn.commit()

    finally:
        conn.close()
    print('执行完成')


if __name__ == '__main__':
    main()
