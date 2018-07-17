# 动态页面爬取。
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    # driver = webdriver.Chrome()
    # driver.get('https://s.taobao.com/search?q=ipads&s=333')
    # js = "var q=document.documentElement.scrollTop=10000"
    # driver.execute_script(js)
    #
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    #
    # print(type(soup))

    resp = requests.get('https://item.taobao.com/item.htm?id=565844866627&ns=1')
    print(resp.content.decode('utf-8'))

if __name__ == '__main__':
    main()
