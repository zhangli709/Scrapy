import requests
import robobrowser


# 利用robobrowser 第三方工具来登录表单。
def main():
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('https://github.com/login')
    f = b.get_form(action='/session')
    f['login'].value = 'zhangli9479@163.com'
    f['password'].value = 'Zl1994-7-9'
    b.submit_form(f)
    # print(b)
    for a_tag in b.select('a[href]'):
        print(a_tag.attrs['href'])


if __name__ == '__main__':
    main()