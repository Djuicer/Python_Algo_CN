"""
Source: https://en.wikipedia.org/wiki/Odd%E2%80%93even_sort

奇偶交换排序（Odd-Even Transposition Sort）的非并行实现。

通常每组中的交换同时进行，若不并行，
算法并不优于冒泡排序。

运行 doctest 请使用以下命令：
python3 -m doctest -v odd_even_transposition_single_threaded.py

手动测试请运行：
python3 odd_even_transposition_single_threaded.py
"""

from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def odd_even_transposition[T: Comparable](collection: list[T]) -> list[T]:
    """
    使用奇偶交换排序算法原地排序列表。

    交替比较并交换偶数索引和奇数索引开头的
    相邻元素对，直到集合完全有序。由于
    每轮比较的元素对互不重叠，各轮可以并行执行；
    本实现按顺序处理这些元素对。

    :param collection: 元素可比较的可变有序集合
    :return: 按升序排列后的同一个集合

    示例：
    >>> odd_even_transposition([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> odd_even_transposition([13, 11, 18, 0, -1]) == sorted([13, 11, 18, 0, -1])
    True
    >>> odd_even_transposition([-.1, 1.1, .1, -2.9]) == sorted([-.1, 1.1, .1, -2.9])
    True
    >>> odd_even_transposition([])
    []
    >>> odd_even_transposition([3, 3, 1, 2, 2, 1])
    [1, 1, 2, 2, 3, 3]
    >>> odd_even_transposition(['c', 'a', 'b']) == sorted(['c', 'a', 'b'])
    True
    >>> odd_even_transposition([3.3, 1.1, 2.2]) == sorted([3.3, 1.1, 2.2])
    True
    >>> values = [4, 2, 7, 1]
    >>> result = odd_even_transposition(values)
    >>> result is values
    True
    >>> values
    [1, 2, 4, 7]
    >>> import random
    >>> collection = random.sample(range(-50, 50), 100)
    >>> odd_even_transposition(collection) == sorted(collection)
    True
    >>> import string
    >>> collection = random.choices(string.ascii_letters + string.digits, k=100)
    >>> odd_even_transposition(collection) == sorted(collection)
    True
    >>> odd_even_transposition([1, "a"])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    arr_size = len(collection)
    for _ in range(arr_size):
        for i in range(_ % 2, arr_size - 1, 2):
            if collection[i + 1] < collection[i]:
                collection[i], collection[i + 1] = collection[i + 1], collection[i]

    return collection


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    arr = list(range(10, 0, -1))
    print(f"Original: {arr}. Sorted: {odd_even_transposition(arr)}")
