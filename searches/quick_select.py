"""
快速选择（Quickselect）算法的 Python 实现，能够高效地
求出列表排序后某个索引处应有的值，
即使该列表尚未排序
https://en.wikipedia.org/wiki/Quickselect
"""

import random


def _partition(data: list, pivot) -> tuple:
    """
    根据数据与枢轴的大小关系，
    将其划分为较小、相等和较大的三个列表
    :param data: 待排序的数据（列表）
    :param pivot: 用于划分数据的枢轴值
    :return: 较小、相等和较大的三个列表
    """
    less, equal, greater = [], [], []
    for element in data:
        if element < pivot:
            less.append(element)
        elif element > pivot:
            greater.append(element)
        else:
            equal.append(element)
    return less, equal, greater


def quick_select(items: list, index: int):
    """
    >>> quick_select([2, 4, 5, 7, 899, 54, 32], 5)
    54
    >>> quick_select([2, 4, 5, 7, 899, 54, 32], 1)
    4
    >>> quick_select([5, 4, 3, 2], 2)
    4
    >>> quick_select([3, 5, 7, 10, 2, 12], 3)
    7
    """
    # 查找中位数时，index = len(items) // 2
    #   （items 排序后对应的 index 值）

    # 无效输入
    if index >= len(items) or index < 0:
        return None

    pivot = items[random.randint(0, len(items) - 1)]
    count = 0
    smaller, equal, larger = _partition(items, pivot)
    count = len(equal)
    m = len(smaller)

    # index 落在枢轴对应的位置范围内
    if m <= index < m + count:
        return pivot
    # 目标必在 smaller 中
    elif m > index:
        return quick_select(smaller, index)
    # 目标必在 larger 中
    else:
        return quick_select(larger, index - (m + count))


def median(items: list):
    """
    快速选择的常见用途之一是查找中位数，即
    有序数据集中间的元素（或中间两个元素的平均值）。
    它只对数据进行部分排序，无需
    将整个列表完全排序，因此能高效处理无序列表。

    >>> median([3, 2, 2, 9, 9])
    3

    >>> median([2, 2, 9, 9, 9, 3])
    6.0
    """
    mid, rem = divmod(len(items), 2)
    if rem != 0:
        return quick_select(items=items, index=mid)
    else:
        low_mid = quick_select(items=items, index=mid - 1)
        high_mid = quick_select(items=items, index=mid)
        return (low_mid + high_mid) / 2
