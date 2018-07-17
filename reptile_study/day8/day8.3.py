def Fob():
    """
    斐波拉契数
    :return:
    """
    num1 = 0
    num2 = 1
    while True:
        res = num1
        num1, num2 = num2, num1 + num2
        yield res

def even(res):
    """
    生成偶数
    :param res:
    :return:
    """
    for val in res:
        if val % 2 == 0:
            yield val


def countdown(n):
    """
    倒计数
    :param n:
    :return:
    """
    while n > 0:
        yield n
        n -= 1


def main():
    fob = even(Fob())
    for _ in range(20):
        print(next(fob))


if __name__ == '__main__':
    main()
