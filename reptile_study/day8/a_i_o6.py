import asyncio

import asn1crypto
import requests


@asyncio.coroutine
async def download(url):
    print('[Fetch:', url)
    # yield from asyncio.sleep(0.000001)
    await asyncio.sleep(0.00001)
    resp = requests.get(url)  # 异步操作，拿到响应
    print(url, '-->', resp.status_code)
    print(url, '-->', resp.headers)



def main():
    loop = asyncio.get_event_loop()
    urls = [
        'https://www.baidu.com',
        'http://www.sohu.com',
        'http://www.sina.com',
        'https://www.taobao.com',
        'http://www.qq.com'
    ]
    tasks = [download(url) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))  # 传进来的函数，必须是协程。

if __name__ == '__main__':
    main()