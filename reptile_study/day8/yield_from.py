#
# def gen():
#     for c in 'AB':
#         yield c
#     for i in range(1, 3):
#         yield i
#
# # list(gen())
# print(list(gen()))   # ['A', 'B', 1, 2]


#
# def gen():
#     yield from 'AB'
#     yield from range(1,3)
#
# print(list(gen()))  # ['A', 'B', 1, 2]



# Example of flattening a nested sequence using subgenerators

from collections import Iterable

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x) # 这里递归调用，如果x是可迭代对象，继续分解
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]

# Produces 1 2 3 4 5 6 7 8
for x in flatten(items):
    print(x, end='')

items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
    print(x)