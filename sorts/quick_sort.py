"""
快速排序（Quick Sort）算法的纯 Python 实现

运行 doctest 请使用以下命令：
python3 -m doctest -v quick_sort.py

手动测试请运行：
python3 quick_sort.py
"""

from __future__ import annotations

from random import randrange
from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def quick_sort[T: Comparable](collection: list[T]) -> list[T]:
    """快速排序算法的纯 Python 实现。

    :param collection: 元素可比较的可变集合
    :return: 按升序排列后的同一个集合

    示例：
    >>> quick_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> quick_sort([])
    []
    >>> quick_sort([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    >>> quick_sort(["z", "a", "m", "b"])
    ['a', 'b', 'm', 'z']
    >>> quick_sort([3.14, -1.0, 2.71])
    [-1.0, 2.71, 3.14]
    >>> quick_sort([0, 5, 3, 2, 2]) == sorted([0, 5, 3, 2, 2])
    True
    >>> quick_sort(["z", "a", "m"]) == sorted(["z", "a", "m"])
    True
    """
    if len(collection) < 2:
        return collection
    pivot_index = randrange(len(collection))
    pivot = collection[pivot_index]
    lesser = [item for item in collection if item < pivot]
    equal = [item for item in collection if item == pivot]
    greater = [item for item in collection if item > pivot]
    return [*quick_sort(lesser), *equal, *quick_sort(greater)]


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(quick_sort(unsorted))
