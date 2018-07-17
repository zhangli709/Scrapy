from functools import wraps


def coroutine(fn):
    # 保留原来的名字。
    @wraps(fn)
    def wrapper(*args, **kwargs):
        gen = fn(*args, **kwargs)
        next(gen)
        return gen

    return wrapper
