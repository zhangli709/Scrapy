import requests
import robobrowser


# 动态页面爬取。无
# 利用robobrowser 第三方工具来登录表单。
def main():
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('https://v.taobao.com')
    for a_tag in b.select['a[href]']:
        print(a_tag.attrs['href'])


if __name__ == '__main__':
    main()