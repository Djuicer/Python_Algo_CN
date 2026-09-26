"""
使用分治法查找单峰列表的峰值。
单峰数组定义如下：数组在索引 p 之前递增，
之后递减。（p >= 1）
一个直接的方法是用 O(n) 时间
查找数组最大值。
(From Kleinberg and Tardos. Algorithm Design.
Addison Wesley 2006: Chapter 5 Solved Exercise 1)
"""

from __future__ import annotations


def peak(lst: list[int]) -> int:
    """
    返回 `lst` 的峰值。
    >>> peak([1, 2, 3, 4, 5, 4, 3, 2, 1])
    5
    >>> peak([1, 10, 9, 8, 7, 6, 5, 4])
    10
    >>> peak([1, 9, 8, 7])
    9
    >>> peak([1, 2, 3, 4, 5, 6, 7, 0])
    7
    >>> peak([1, 2, 3, 4, 3, 2, 1, 0, -1, -2])
    4
    """
    # 中间索引
    m = len(lst) // 2

    # 选择中间的 3 个元素
    three = lst[m - 1 : m + 2]

    # 中间元素为峰值时
    if three[1] > three[0] and three[1] > three[2]:
        return three[1]

    # 若递增，则递归搜索右侧
    elif three[0] < three[2]:
        if len(lst[:m]) == 2:
            m -= 1
        return peak(lst[m:])

    # 递减
    else:
        if len(lst[:m]) == 2:
            m += 1
        return peak(lst[:m])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
