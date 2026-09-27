"""
最大子数组和问题是在给定的数值数组中，寻找一个和最大的连续子数组。
例如，给定数组 [-2, 1, -3, 4, -1, 2, 1, -5, 4]，和最大的连续子数组是
[4, -1, 2, 1]，因此最大子数组和为 6。

Kadane 算法是一种简单的动态规划算法，以 O(n) 时间和 O(1) 空间解决最大子数组和问题。

Reference: https://en.wikipedia.org/wiki/Maximum_subarray_problem
"""

from collections.abc import Sequence


def max_subarray_sum(
    arr: Sequence[float], allow_empty_subarrays: bool = False
) -> float:
    """
    使用 Kadane 算法解决最大子数组和问题。
    :param arr: 给定的数值数组
    :param allow_empty_subarrays: 如果为 True，则算法会考虑空子数组

    >>> max_subarray_sum([2, 8, 9])
    19
    >>> max_subarray_sum([0, 0])
    0
    >>> max_subarray_sum([-1.0, 0.0, 1.0])
    1.0
    >>> max_subarray_sum([1, 2, 3, 4, -2])
    10
    >>> max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> max_subarray_sum([2, 3, -9, 8, -2])
    8
    >>> max_subarray_sum([-2, -3, -1, -4, -6])
    -1
    >>> max_subarray_sum([-2, -3, -1, -4, -6], allow_empty_subarrays=True)
    0
    >>> max_subarray_sum([])
    0
    """
    if not arr:
        return 0

    max_sum = 0 if allow_empty_subarrays else float("-inf")
    curr_sum = 0.0
    for num in arr:
        curr_sum = max(0 if allow_empty_subarrays else num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)

    return max_sum


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"{max_subarray_sum(nums) = }")
