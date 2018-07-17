import inspect


def simple_coro2(a):
    print('-> coroutine started: a=', a)
    b = yield a
    print('-> coroutine received: b =', b)
    c = yield b + a
    print('-> coroutine Received: c = ', c)


my_coro2 = simple_coro2(14)  #
print(inspect.getgeneratorstate(my_coro2))  # 1 GEN_CREATED

next(my_coro2)  # 2 '-> coroutine started: a= 14
print(inspect.getgeneratorstate(my_coro2))  # 3 GEN_SUSPENDED

my_coro2.send(28)  # 4   -> coroutine received: b = 28
print(inspect.getgeneratorstate(my_coro2))  # 5 GEN_SUSPENDED
my_coro2.send(99)  # 6 -> coroutine Received: c =  99

# 7 StopIteration