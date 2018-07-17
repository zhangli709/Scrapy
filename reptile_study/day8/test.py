import inspect


def simple_coroutine():
    print('-> coroutine started')  # 2 -> coroutine started
    x = yield
    print('-> coroutine received:', x)  # 4 -> coroutine received: 42


my_coro = simple_coroutine()
print(inspect.getgeneratorstate(my_coro))  # 1 GEN_CREATED
# my_coro.send(None)

next(my_coro)
print(inspect.getgeneratorstate(my_coro))  # 3 GEN_SUSPENDED

my_coro.send(42)
print(inspect.getgeneratorstate(my_coro))  #  5 StopIteration
