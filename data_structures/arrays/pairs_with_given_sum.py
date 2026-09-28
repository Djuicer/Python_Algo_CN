#!/usr/bin/env python3

"""
给定一个数组 的 整数 并且 整数 req_sum，查找 数 的 对 的 数组
元素 whose 和 是 等于 到 req_sum。

https://practice.geeksforgeeks.org/problems/count-pairs-with-given-sum5022/0
"""

from itertools import combinations


def pairs_with_sum(arr: list, req_sum: int) -> int:
    """
    返回 没有. 的 对 带有 和 "和"
    >>> pairs_with_sum([1, 5, 7, 1], 6)
    2
    >>> pairs_with_sum([1, 1, 1, 1, 1, 1, 1, 1], 2)
    28
    >>> pairs_with_sum([1, 7, 6, 2, 5, 4, 3, 1, 9, 8], 7)
    4
    """
    return len([1 for a, b in combinations(arr, 2) if a + b == req_sum])


if __name__ == "__main__":
    from doctest import testmod

    testmod()
