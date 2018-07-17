import asyncio

import aiohttp


# 不仅能操作网页，还能操作客户端

async def download(url):
    print('[Fetch:', url)
    # yield from asyncio.sleep
    async with aiohttp.ClientSession() as session:  # with 自动关闭，释放内存
        async with session.get(url) as resp:
            print(url, '-->', resp.status)
            print(url, '-->', resp.headers)
            # print('\n\n', await resp.text())  # 只能方生成器


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
