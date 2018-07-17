# 动态页面爬取。
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    driver = webdriver.Chrome()
    driver.get('https://v.taobao.com/v/content/live?spm=a21xh.11312891.servList.1.1ae97001cn78J4&catetype=701')
    elem = driver.find_element_by_css_selector('input[placeholder="输入关键词搜索"]')
    elem.send_keys('美女')
    elem.send_keys(Keys.ENTER)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for img_tag in soup.body.select('img[src]'):
        print(img_tag.attrs['src'])


if __name__ == '__main__':
    main()
