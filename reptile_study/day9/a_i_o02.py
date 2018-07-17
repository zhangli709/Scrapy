import threading
from time import sleep

import asyncio

# 生产
from day8.myutils import coroutine


@asyncio.coroutine
async def countdown(name, num):
    # 打印线程的消息， 只有一个MainThreading
    print(threading.current_thread())
    while True:
        print(f'Countdown[{name}:{num}]')
        # 异步执行 - 非阻塞式
        await asyncio.sleep(1)
        # 同步执行 - 阻塞式
        sleep(1)
        num -= 1


def main():
    loop = asyncio.get_event_loop()
    # 异步I/ O - 虽然只有一个线程，但是两个任务之间相互不阻塞
    tasks = [
        countdown('A', 10),
        countdown('B', 5)
    ]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    main()
