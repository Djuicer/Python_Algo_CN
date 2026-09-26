"""
Return the minimum element of an array using the
divide-and-conquer algorithm for selection sort.
Like quicksort, it partitions the input array recursively.
But unlike quicksort,
which recursively processes both sides of the partition,
this algorithm works on only one side of the partition.
The expected running time of this selection sort algorithm is 0(n),
assuming that the elements are distinct.
It returns the ith smallest element of the array A[p: r], where 1 ≤ i ≤ r-p+1.
(From Introduction to Algorithms, Fourth Edition, Cormen, 2022: Chapter 9.2)
"""

from __future__ import annotations

import random


def partition(array: list, starting_index: int, ending_index: int) -> int:
    """
    划分数组。
    Args:
        array: 元素列表
        starting_index: 数组的起始索引
        ending_index: 数组的结束索引

    Returns:
        枢轴的索引

    >>> arr = [-2, 3, -10, 11, 99, 100000, 100, -200]
    >>> partition(arr, 0, len(arr) - 1)
    0
    """
    pivot = array[ending_index]
    i = starting_index - 1
    for j in range(starting_index, ending_index):
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[ending_index] = array[ending_index], array[i + 1]
    return i + 1


def randomized_partition(array: list, starting_index: int, ending_index: int) -> int:
    """
    对数组进行随机划分。
    Args:
        array: 元素列表
        starting_index: 数组的起始索引
        ending_index: 数组的结束索引

    Returns:
        调用 partition 函数的结果

    >>> arr = [-2, 3, -10, 11, 99, 100000, 100, -200]
    >>> arr1 = randomized_partition(arr, 0, len(arr) - 1)
    >>> arr == arr1
    False
    """

    rand_idx = random.randint(starting_index, ending_index)
    array[rand_idx], array[ending_index] = array[ending_index], array[rand_idx]
    return partition(array, starting_index, ending_index)


def selection_sort(
    array: list, starting_index: int, ending_index: int, smallest_element: int
) -> list | None:
    """
    Returns a list of sorted array elements using selection sort.
    相比线性扫描，用选择算法求最小值虽同为 O(n)，却显得复杂；
    这里的价值在于演示分治和划分过程。

    Args:
        array: 元素列表
        starting_index: 数组的起始索引
        ending_index: 数组的结束索引
        smallest_element: 数组 A[p: r] 中第 i 小的元素，
                          其中 1 ≤ i ≤ r-p+1

    Returns:
        sorted array

    >>> from random import shuffle
    >>> arr = [-2, 3, -10, 11, 99, 100000, 100, -200]
    >>> shuffle(arr)
    >>> selection_sort(arr, 0, len(arr) - 1, 1)
    -200

    >>> shuffle(arr)
    >>> selection_sort(arr, 0, len(arr) - 1, 1)
    -200

    >>> arr = [-200]
    >>> selection_sort(arr, 0, len(arr) - 1, 1)
    -200

    >>> arr = [-2]
    >>> selection_sort(arr, 0, len(arr) - 1, 1)
    -2

    >>> arr = []
    >>> selection_sort(arr, 0, len(arr) - 1, 1)
    []
    """

    if not array:
        return array

    if starting_index == ending_index:
        # 当 p == r 时，1 <= i <= r - p + 1 意味着 i == 1
        return array[starting_index]

    q = randomized_partition(array, starting_index, ending_index)

    k = q - starting_index + 1

    if smallest_element == k:
        return array[q]  # 枢轴值即为答案
    if smallest_element < k:
        return selection_sort(array, starting_index, q - 1, smallest_element)
    else:
        return selection_sort(array, q + 1, ending_index, smallest_element - k)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
