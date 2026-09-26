"""
奇偶排序（Odd-Even Sort）的实现。

https://en.wikipedia.org/wiki/Odd%E2%80%93even_sort
"""

from collections.abc import MutableSequence
from typing import Any, Protocol


class Comparable(Protocol):
    def __gt__(self, other: Any, /) -> bool: ...


def odd_even_sort[T: Comparable](collection: MutableSequence[T]) -> MutableSequence[T]:
    """
    使用奇偶排序对输入排序。

    该算法采用与冒泡排序相同的思想，
    但分为奇数和偶数两个阶段。
    最初设计用于具有局部互连的
    并行处理器。
    :param collection: 可变有序元素序列
    :return: 按升序排列后的同一个集合
    示例：
    >>> odd_even_sort([5 , 4 ,3 ,2 ,1])
    [1, 2, 3, 4, 5]
    >>> odd_even_sort([])
    []
    >>> odd_even_sort([-10 ,-1 ,10 ,2])
    [-10, -1, 2, 10]
    >>> odd_even_sort([1 ,2 ,3 ,4])
    [1, 2, 3, 4]
    >>> odd_even_sort(["c","a","b"])
    ['a', 'b', 'c']
    >>> odd_even_sort([2.5, -1, 0.0])
    [-1, 0.0, 2.5]
    >>> odd_even_sort([1,"a"])
    Traceback (most recent call last):
       ...
    TypeError: '>' not supported between instances of 'int' and 'str'
    """
    is_sorted = False
    while is_sorted is False:  # 持续循环，直到遍历完所有索引
        is_sorted = True
        for i in range(0, len(collection) - 1, 2):  # 遍历所有偶数索引
            if collection[i] > collection[i + 1]:
                collection[i], collection[i + 1] = collection[i + 1], collection[i]
                # 元素顺序不正确时交换
                is_sorted = False

        for i in range(1, len(collection) - 1, 2):  # 遍历所有奇数索引
            if collection[i] > collection[i + 1]:
                collection[i], collection[i + 1] = collection[i + 1], collection[i]
                # 元素顺序不正确时交换
                is_sorted = False
    return collection


if __name__ == "__main__":
    print("Enter list to be sorted")
    input_list = [int(x) for x in input().split()]
    # 在一行中输入列表元素
    sorted_list = odd_even_sort(input_list)
    print("The sorted list is")
    print(sorted_list)
