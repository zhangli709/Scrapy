import requests
from bs4 import BeautifulSoup


def main():
    """
    常规方法跳过表单，获取页面
    :return:
    """
    resp = requests.get('https://github.com/login')
    if resp.status_code != 200:
        print('页面拿不到')
        # return
    cookies = resp.cookies.get_dict()
    soup = BeautifulSoup(resp.text, 'lxml')  # lxml 解析器， 效果好一点
    utf8_value = soup.select_one('form input[name=utf8]').attrs['value']
    authenticity_token = soup.select_one('form input[name=authenticity_token]').attrs['value']
    data = {
        'utf8': utf8_value,
        'authenticity_token': authenticity_token,
        'login': 'zhangli9479@163.com',
        'password': 'Zl1994-7-9'
    }
    # 上传文件
    # files = {
    #     'files1': open(),
    #     'files2': open()
    # }
    resp2 = requests.post('https://github.com/login', data=data, cookies=cookies)
    print(resp2.content.decode('utf-8'))


if __name__ == '__main__':
    main()
