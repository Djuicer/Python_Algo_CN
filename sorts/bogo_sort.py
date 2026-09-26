"""
猴子排序（Bogosort）算法的纯 Python 实现，
也称 permutation sort、stupid sort、slowsort、shotgun sort 或 monkey sort。
随机生成排列，直到碰巧得到正确顺序。

More info on: https://en.wikipedia.org/wiki/Bogosort

运行 doctest 请使用以下命令：
python -m doctest -v bogo_sort.py
或
python3 -m doctest -v bogo_sort.py
手动测试请运行：
python bogo_sort.py
"""

import random
from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def bogo_sort[T: Comparable](collection: list[T]) -> list[T]:
    """猴子排序算法的纯 Python 实现
    :param collection: 可变有序集合，其中包含类型可不同但
    可相互比较的元素
    :return: 按升序排列后的同一个集合
    示例：
    >>> bogo_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> bogo_sort([])
    []
    >>> bogo_sort([-2, -5, -45])
    [-45, -5, -2]
    >>> bogo_sort(["c", "a", "b"])
    ['a', 'b', 'c']
    >>> bogo_sort([2.5, -1.0, 0.0])
    [-1.0, 0.0, 2.5]
    >>> bogo_sort([1, "a"])
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """

    def is_sorted[T: Comparable](collection: list[T]) -> bool:
        for i in range(len(collection) - 1):
            if collection[i + 1] < collection[i]:
                return False
        return True

    while not is_sorted(collection):
        random.shuffle(collection)
    return collection


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(bogo_sort(unsorted))
