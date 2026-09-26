"""
归并排序（Merge Sort）的 Python 迭代实现
Author: Aman Gupta

运行 doctest 请使用以下命令：
python3 -m doctest -v iterative_merge_sort.py

手动测试请运行：
python3 iterative_merge_sort.py
"""

from __future__ import annotations

from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def merge[T: Comparable](input_list: list[T], low: int, mid: int, high: int) -> list[T]:
    """
    分别对左右两半排序，
    然后将其合并为结果
    """
    result: list[T] = []
    left, right = input_list[low:mid], input_list[mid : high + 1]
    while left and right:
        result.append((left if left[0] <= right[0] else right).pop(0))
    input_list[low : high + 1] = result + left + right
    return input_list


# 遍历无序列表
def iter_merge_sort[T: Comparable](input_list: list[T]) -> list[T]:
    """
    返回输入列表的已排序副本

    >>> iter_merge_sort([5, 9, 8, 7, 1, 2, 7])
    [1, 2, 5, 7, 7, 8, 9]
    >>> iter_merge_sort([1])
    [1]
    >>> iter_merge_sort([2, 1])
    [1, 2]
    >>> iter_merge_sort([2, 1, 3])
    [1, 2, 3]
    >>> iter_merge_sort([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> iter_merge_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> iter_merge_sort(['c', 'b', 'a'])
    ['a', 'b', 'c']
    >>> iter_merge_sort([0.3, 0.2, 0.1])
    [0.1, 0.2, 0.3]
    >>> iter_merge_sort(['dep', 'dang', 'trai'])
    ['dang', 'dep', 'trai']
    >>> iter_merge_sort([6])
    [6]
    >>> iter_merge_sort([])
    []
    >>> iter_merge_sort([-2, -9, -1, -4])
    [-9, -4, -2, -1]
    >>> iter_merge_sort([1.1, 1, 0.0, -1, -1.1])
    [-1.1, -1, 0.0, 1, 1.1]
    >>> iter_merge_sort(['c', 'b', 'a'])
    ['a', 'b', 'c']
    >>> iter_merge_sort(list('cba'))
    ['a', 'b', 'c']
    >>> iter_merge_sort([1, "a"])  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...
    """
    if len(input_list) <= 1:
        return input_list
    input_list = list(input_list)

    # 进行两路归并的迭代
    p = 2
    while p <= len(input_list):
        # 获取单个列表归并排序所需的 low、high 和 middle 值
        for i in range(0, len(input_list), p):
            low = i
            high = i + p - 1
            mid = (low + high + 1) // 2
            input_list = merge(input_list, low, mid, high)
        # 最后两部分的最终合并
        if p * 2 >= len(input_list):
            mid = i
            input_list = merge(input_list, 0, mid, len(input_list) - 1)
            break
        p *= 2

    return input_list


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    if user_input == "":
        unsorted = []
    else:
        unsorted = [int(item.strip()) for item in user_input.split(",")]
    print(iter_merge_sort(unsorted))
