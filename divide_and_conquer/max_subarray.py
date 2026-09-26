"""
最大子数组问题是在给定的数值数组中，寻找
元素和最大的连续子数组。例如，对于数组
[-2, 1, -3, 4, -1, 2, 1, -5, 4]，元素和最大的连续子数组为
[4, -1, 2, 1]，其和为 6。

该分治算法在 O(n log n) 时间内找到最大子数组。
"""

from __future__ import annotations

import time
from collections.abc import Sequence
from random import randint

from matplotlib import pyplot as plt


def max_subarray(
    arr: Sequence[float], low: int, high: int
) -> tuple[int | None, int | None, float]:
    """
    使用分治法求解最大子数组问题。
    :param arr:     给定的数值数组
    :param low:     起始索引
    :param high:    结束索引
    :return:        最大子数组的起始索引、结束索引，
                    以及最大子数组的元素和

    >>> nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    >>> max_subarray(nums, 0, len(nums) - 1)
    (3, 6, 6)
    >>> nums = [2, 8, 9]
    >>> max_subarray(nums, 0, len(nums) - 1)
    (0, 2, 19)
    >>> nums = [0, 0]
    >>> max_subarray(nums, 0, len(nums) - 1)
    (0, 0, 0)
    >>> nums = [-1.0, 0.0, 1.0]
    >>> max_subarray(nums, 0, len(nums) - 1)
    (2, 2, 1.0)
    >>> nums = [-2, -3, -1, -4, -6]
    >>> max_subarray(nums, 0, len(nums) - 1)
    (2, 2, -1)
    >>> max_subarray([], 0, 0)
    (None, None, 0)
    """
    if not arr:
        return None, None, 0
    if low == high:
        return low, high, arr[low]

    mid = (low + high) // 2
    left_low, left_high, left_sum = max_subarray(arr, low, mid)
    right_low, right_high, right_sum = max_subarray(arr, mid + 1, high)
    cross_left, cross_right, cross_sum = max_cross_sum(arr, low, mid, high)
    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_low, left_high, left_sum
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return right_low, right_high, right_sum
    return cross_left, cross_right, cross_sum


def max_cross_sum(
    arr: Sequence[float], low: int, mid: int, high: int
) -> tuple[int, int, float]:
    left_sum, max_left = float("-inf"), -1
    right_sum, max_right = float("-inf"), -1

    summ: int | float = 0
    for i in range(mid, low - 1, -1):
        summ += arr[i]
        if summ > left_sum:
            left_sum = summ
            max_left = i

    summ = 0
    for i in range(mid + 1, high + 1):
        summ += arr[i]
        if summ > right_sum:
            right_sum = summ
            max_right = i

    return max_left, max_right, (left_sum + right_sum)


def time_max_subarray(input_size: int) -> float:
    arr = [randint(1, input_size) for _ in range(input_size)]
    start = time.time()
    max_subarray(arr, 0, input_size - 1)
    end = time.time()
    return end - start


def plot_runtimes() -> None:
    input_sizes = [10, 100, 1000, 10000, 50000, 100000, 200000, 300000, 400000, 500000]
    runtimes = [time_max_subarray(input_size) for input_size in input_sizes]
    print("No of Inputs\t\tTime Taken")
    for input_size, runtime in zip(input_sizes, runtimes):
        print(input_size, "\t\t", runtime)
    plt.plot(input_sizes, runtimes)
    plt.xlabel("Number of Inputs")
    plt.ylabel("Time taken in seconds")
    plt.show()


if __name__ == "__main__":
    """
    对该算法进行随机模拟。
    """
    from doctest import testmod

    testmod()
