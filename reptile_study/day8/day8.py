# 动态页面爬取。
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    driver = webdriver.Chrome()
    driver.get('https://www.jd.com')
    driver.execute_script('document.documentElement.scrollTop = "100001px"')  # 写js脚本

    while True:
        sleep(50)


    # meta http-equiv="refresh" content="5, https://www.baidu.com   5秒之后重定向，我们抓取后面这个网站。










if __name__ == '__main__':
    main()