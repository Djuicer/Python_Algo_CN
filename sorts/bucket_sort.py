#!/usr/bin/env python3
"""
演示桶排序（Bucket Sort）算法的实现。

Author: OMKAR PATHAK
本程序演示如何实现桶排序算法

维基百科说明：桶排序又称 bin sort，通过将
数组元素分配到若干桶中进行排序。
然后分别对每个桶排序，可使用其他排序
算法，也可递归使用桶排序。它属于
分布排序，与从最高位到最低位进行处理的
基数排序关系密切。
桶排序是鸽巢排序的推广。桶排序可以
使用比较操作实现，因此也可视为
比较排序算法。计算复杂度的估计与
桶的数量有关。

解法的时间复杂度：
最坏情况是所有元素都进入同一个桶。
此时总体性能由桶内排序算法
决定。这里使用 TimSort，因此为 O(n log n)

平均情况为 O(n + (n^2)/k + k)，其中 k 为桶数

若 k = O(n)，则时间复杂度为 O(n)

Source: https://en.wikipedia.org/wiki/Bucket_sort
"""

from __future__ import annotations


def bucket_sort(
    my_list: list[int | float], bucket_count: int = 10
) -> list[int | float]:
    """
    >>> data = [-1, 2, -5, 0]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> data = [9, 8, 7, 6, -12]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> data = [.4, 1.2, .1, .2, -.9]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> bucket_sort([]) == sorted([])
    True
    >>> data = [-1e10, 1e10]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> import random
    >>> collection = random.sample(range(-50, 50), 50)
    >>> bucket_sort(collection) == sorted(collection)
    True
    >>> data = [1, 2, 2, 1, 1, 3]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> data = [5, 5, 5, 5, 5]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> data = [1000, -1000, 500, -500, 0]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> data = [5.5, 2.2, -1.1, 3.3, 0.0]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> bucket_sort(data, 2.5)
    Traceback (most recent call last):
    TypeError: bucket_count must be an integer
    >>> bucket_sort([1]) == [1]
    True
    >>> bucket_sort([1, 2, 3], 2.5)
    Traceback (most recent call last):
        ...
    TypeError: bucket_count must be an integer
    >>> data = [-1.1, -1.5, -3.4, 2.5, 3.6, -3.3]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> data = [9, 2, 7, 1, 5]
    >>> bucket_sort(data) == sorted(data)
    True
    >>> bucket_sort(data, 3.5)
    Traceback (most recent call last):
    ...
    TypeError: bucket_count must be an integer
    """

    if not isinstance(bucket_count, (bool, int)):
        raise TypeError("bucket_count must be an integer")
    if not my_list or bucket_count <= 0:
        return []

    min_value, max_value = min(my_list), max(my_list)
    if min_value == max_value:
        return my_list

    bucket_size = (max_value - min_value) / bucket_count
    buckets: list[list] = [[] for _ in range(bucket_count)]

    for val in my_list:
        index = min(int((val - min_value) / bucket_size), bucket_count - 1)
        buckets[index].append(val)

    return [val for bucket in buckets for val in sorted(bucket)]


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    assert bucket_sort([4, 5, 3, 2, 1]) == [1, 2, 3, 4, 5]
    assert bucket_sort([0, 1, -10, 15, 2, -2]) == [-10, -2, 0, 1, 2, 15]
    assert bucket_sort([1.1, 1.2, -1.2, 0, 2.4]) == [-1.2, 0, 1.1, 1.2, 2.4]
    assert bucket_sort([5, 5, 5, 5, 5]) == [5, 5, 5, 5, 5]
    assert bucket_sort([-5, -1, -6, -2]) == [-6, -5, -2, -1]
