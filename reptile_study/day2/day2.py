from urllib.parse import urljoin
import re
import requests
from bs4 import BeautifulSoup


def main():
    # 设置请求头
    head = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'}
    # 设置代理
    proxies = {
        # 'http': 'http://119.28.142.148:8888',
        'https': 'https://101.251.232.221:3128'
    }
    base_url = 'https://www.zhihu.com/'
    # 拼接链接
    seed_url = urljoin(base_url, 'explore')
    resp = requests.get('https://www.zhihu.com/explore', headers=head, proxies=proxies)
    # print(resp.text)
    soup = BeautifulSoup(resp.text, 'lxml')

    # 筛选需要的东西,
    href_regex = re.compile(r'^/question')
    # 去重
    link_set = set()
    for a_tag in soup.find_all('a', {'href': href_regex}):
        # 拿属性
        href = a_tag.attrs['href']
        # 错误判断
        if 'href' in a_tag.attrs:
            full_url = urljoin(base_url, href)
            link_set.add(full_url)

    print(len(link_set))
    print(link_set)


if __name__ == '__main__':
    main()