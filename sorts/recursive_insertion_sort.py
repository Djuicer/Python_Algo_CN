"""
插入排序（Insertion Sort）算法的递归实现
"""

from __future__ import annotations

from collections.abc import MutableSequence
from typing import Any, Protocol, TypeVar


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Comparable)


def rec_insertion_sort[T](collection: MutableSequence[T], n: int) -> None:
    """
    给定可比较元素组成的集合及其长度，
    对集合进行原地升序排序。

    :param collection: 元素可比较的可变集合
    :param n: collection 的长度

    >>> col = [1, 2, 1]
    >>> rec_insertion_sort(col, len(col))
    >>> col
    [1, 1, 2]

    >>> col = [2, 1, 0, -1, -2]
    >>> rec_insertion_sort(col, len(col))
    >>> col
    [-2, -1, 0, 1, 2]

    >>> col = [1]
    >>> rec_insertion_sort(col, len(col))
    >>> col
    [1]

    >>> col = ['d', 'a', 'b', 'e', 'c']
    >>> rec_insertion_sort(col, len(col))
    >>> col
    ['a', 'b', 'c', 'd', 'e']
    """
    # 检查整个集合是否已排序
    if len(collection) <= 1 or n <= 1:
        return

    insert_next(collection, n - 1)
    rec_insertion_sort(collection, n - 1)


def insert_next[T](collection: MutableSequence[T], index: int) -> None:
    """
    将第 '(index-1)th' 个元素插入正确位置

    >>> col = [3, 2, 4, 2]
    >>> insert_next(col, 1)
    >>> col
    [2, 3, 4, 2]

    >>> col = [3, 2, 3]
    >>> insert_next(col, 2)
    >>> col
    [3, 2, 3]

    >>> col = []
    >>> insert_next(col, 1)
    >>> col
    []
    """
    # 检查相邻元素的顺序
    if index >= len(collection) or collection[index - 1] <= collection[index]:
        return

    # 相邻元素未按升序排列，因此交换它们
    collection[index - 1], collection[index] = (
        collection[index],
        collection[index - 1],
    )

    insert_next(collection, index + 1)


if __name__ == "__main__":
    numbers = input("Enter integers separated by spaces: ")
    number_list: list[int] = [int(num) for num in numbers.split()]
    rec_insertion_sort(number_list, len(number_list))
    print(number_list)
