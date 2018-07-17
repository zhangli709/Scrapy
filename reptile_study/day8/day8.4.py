from time import sleep




# 生产
from myutils import coroutine


def countdown_gen(n, consumer):
    # 预先激活，为了让代码来到yield这一句
    # next(consumer)
    while n > 0:
        consumer.send(n)
        n -= 1


# 消费
@coroutine
def countdown_con():
    while True:
        n = yield  # 我要拿到一个,消费一个，并且赋值给n

        print('Countdown:', n)
        sleep(1)


def main():
    consumer = countdown_con()
    countdown_gen(4, consumer)  # 消费者传入生产者里，来消费生产的东西。相互配合，微线程。


if __name__ == '__main__':
    main()
