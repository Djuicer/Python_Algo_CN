#!/usr/bin/env python3

"""
指数查找（Exponential Search）算法的纯 Python 实现

更多信息请参阅维基百科页面：
https://en.wikipedia.org/wiki/Exponential_search

运行 doctest 请使用以下命令：
python3 -m doctest -v exponential_search.py

手动测试请运行：
python3 exponential_search.py
"""

from __future__ import annotations


def binary_search_by_recursion(
    sorted_collection: list[int],
    item: int,
    left: int = 0,
    right: int | None = None,
) -> int:
    """二分查找（Binary Search）算法的纯 Python 递归实现

    注意，集合必须按升序排列，否则结果
    不可预测。

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 待查找的元素值
    :param left: 搜索的起始索引
    :param right: 搜索的结束索引（默认为最后一个索引）
    :return: 找到的元素索引；未找到则返回 -1

    示例：
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 0, 0, 4)
    0
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 15, 0, 4)
    4
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 5, 0, 4)
    1
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 6, 0, 4)
    -1
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], -1)
    -1
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 16)
    -1
    """
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")
    if right is None:
        right = len(sorted_collection) - 1

    # 递归核心：此处的 ``left`` 和 ``right`` 始终是具体索引，因此
    # 搜索区间只能缩小。递归中不使用 ``None`` 哨兵，也不
    # 重新扩大区间，可避免目标值小于 ``sorted_collection[0]``、
    # ``right`` 正常减小到 ``left`` 以下时发生失控递归。
    def _search(left: int, right: int) -> int:
        if right < left:
            return -1

        midpoint = left + (right - left) // 2

        if sorted_collection[midpoint] == item:
            return midpoint
        elif sorted_collection[midpoint] > item:
            return _search(left, midpoint - 1)
        else:
            return _search(midpoint + 1, right)

    return _search(left, right)


def exponential_search(sorted_collection: list[int], item: int) -> int:
    """
    指数查找算法的纯 Python 实现。
    更多信息请参阅：
    https://en.wikipedia.org/wiki/Exponential_search

    注意，集合必须按升序排列，否则结果
    不可预测。

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 待查找的元素值
    :return: 找到的元素索引；未找到则返回 -1

    该算法的时间复杂度为 O(log i)，其中 i 为目标元素的索引。

    示例：
    >>> exponential_search([0, 5, 7, 10, 15], 0)
    0
    >>> exponential_search([0, 5, 7, 10, 15], 15)
    4
    >>> exponential_search([0, 5, 7, 10, 15], 5)
    1
    >>> exponential_search([0, 5, 7, 10, 15], 6)
    -1
    >>> exponential_search([0, 5, 7, 10, 15], -3)
    -1
    >>> exponential_search([0, 5, 7, 10, 15], 20)
    -1
    >>> exponential_search([], 1)  # Empty array edge case
    -1
    """
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")

    if not sorted_collection:
        return -1
    if sorted_collection[0] == item:
        return 0

    bound = 1
    while bound < len(sorted_collection) and sorted_collection[bound] < item:
        bound *= 2

    left = bound // 2
    right = min(bound, len(sorted_collection) - 1)
    return binary_search_by_recursion(sorted_collection, item, left, right)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 手动测试
    user_input = input("Enter numbers separated by commas: ").strip()
    collection = sorted(int(item) for item in user_input.split(","))
    target = int(input("Enter a number to search for: "))
    result = exponential_search(sorted_collection=collection, item=target)
    if result == -1:
        print(f"{target} was not found in {collection}.")
    else:
        print(f"{target} was found at index {result} in {collection}.")
