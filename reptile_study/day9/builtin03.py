import math


def calc(my_list, fn):
    result = my_list[0]
    for i in my_list[1:]:
        result = fn(result, i)
    return result


def main():
    my_list = [1, 2, 3, 4, 5]
    print(calc(my_list, lambda x, y: x * y))
    thy_list = [23, 43, 54, 44, 66, 35, 87]
    print(sum(map(math.sqrt, filter(lambda x: x % 2 == 0, thy_list))))


if __name__ == '__main__':
    main()
