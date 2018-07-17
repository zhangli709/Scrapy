# 消费型的生成器
from random import randint
from time import sleep


def create_delivery_man(name, capacity=1):
    buffer = []
    while True:
        size = 0
        while size < capacity:

            # 消费掉你给我的东西
            pkg_name = yield  # 等待你给我一个包裹
            if pkg_name:
                size += 1
                buffer.append(pkg_name)
                print('%s正在接收包裹%s' % (name, pkg_name))
            else:
                break
        print('%s正在派送%d件包裹' % (name, len(buffer)))
        sleep(randint(2, 3))  # 模拟派送过程
        buffer.clear()


def create_package_center(consumer, max_packages):
    consumer.send(None)  # 1. 预激活，让代码执行到yield这一行
    num = 0
    while num <= max_packages:
        print('快递中心准备派送%d号包裹' % num)
        consumer.send('包裹-%s' % num)
        num += 1
        if num % 10 == 0:
            sleep(randint(4,5))


def main():
    dm = create_delivery_man('曹宇', 7)
    create_package_center(dm, 25)


if __name__ == '__main__':
    main()
