"""
使用分治法在线性时间内查找第 k 小的元素。
也可以简单地在 O(nlogn) 时间内完成：先对列表排序，
再以常数时间访问第 k 个元素。

这是一个能在 O(n) 时间内求解的分治算法。

关于该算法的更多信息：
https://web.stanford.edu/class/archive/cs/cs161/cs161.1138/lectures/08/Small08.pdf
"""

from __future__ import annotations

from random import choice


def random_pivot(lst):
    """
    为列表随机选择一个枢轴。
    这里也可以使用更复杂的算法，例如中位数的中位数
    （Median of Medians）算法。
    """
    return choice(lst)


def kth_number(lst: list[int], k: int) -> int:
    """
    返回 lst 中第 k 小的数。
    >>> kth_number([2, 1, 3, 4, 5], 3)
    3
    >>> kth_number([2, 1, 3, 4, 5], 1)
    1
    >>> kth_number([2, 1, 3, 4, 5], 5)
    5
    >>> kth_number([3, 2, 5, 6, 7, 8], 2)
    3
    >>> kth_number([25, 21, 98, 100, 76, 22, 43, 60, 89, 87], 4)
    43
    """
    # 选择枢轴，并根据枢轴将元素划分到列表中。
    pivot = random_pivot(lst)

    # 根据枢轴划分
    # 线性时间
    small = [e for e in lst if e < pivot]
    big = [e for e in lst if e > pivot]

    # 运气好时，枢轴可能恰好就是目标元素。
    # 可以直观地看出：
    # small（小于 k 的元素）
    # + pivot（第 k 个元素）
    # + big（大于 k 的元素）
    if len(small) == k - 1:
        return pivot
    # 枢轴位于大于 k 的元素中
    elif len(small) < k - 1:
        return kth_number(big, k - len(small) - 1)
    # 枢轴位于小于 k 的元素中
    else:
        return kth_number(small, k)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
