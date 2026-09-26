"""
基数排序（Radix Sort）算法的纯 Python 实现

Source: https://en.wikipedia.org/wiki/Radix_sort
"""

from __future__ import annotations

RADIX = 10


def radix_sort(list_of_ints: list[int]) -> list[int]:
    """
    示例：
    >>> radix_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> radix_sort(list(range(15))) == sorted(range(15))
    True
    >>> radix_sort(list(range(14,-1,-1))) == sorted(range(15))
    True
    >>> radix_sort([1,100,10,1000]) == sorted([1,100,10,1000])
    True
    >>> radix_sort([-1, 2, 3])
    Traceback (most recent call last):
    ...
    ValueError: All elements in list_of_ints must be non-negative integers
    """
    if not list_of_ints:
        return []

    if any(i < 0 for i in list_of_ints):
        raise ValueError("All elements in list_of_ints must be non-negative integers")

    placement = 1
    max_digit = max(list_of_ints)
    while placement <= max_digit:
        # 声明并初始化空桶
        buckets: list[list] = [[] for _ in range(RADIX)]
        # 将 list_of_ints 分配到各桶
        for i in list_of_ints:
            tmp = int((i / placement) % RADIX)
            buckets[tmp].append(i)
        # 将各桶内容放回 list_of_ints
        a = 0
        for b in range(RADIX):
            for i in buckets[b]:
                list_of_ints[a] = i
                a += 1
        # 处理下一位
        placement *= RADIX
    return list_of_ints


if __name__ == "__main__":
    import doctest

    doctest.testmod()
