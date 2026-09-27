"""
Author  : Mehdi ALAOUI

这是使用纯 Python 实现的给定序列最长递增子序列动态规划（Dynamic Programming）解法。

问题如下：
    给定一个数组，查找并返回其中最长的递增子数组。

示例：
    输入 ``[10, 22, 9, 33, 21, 50, 41, 60, 80]`` 将返回
    ``[10, 22, 33, 41, 60, 80]``。
"""

from __future__ import annotations


def longest_subsequence(array: list[int]) -> list[int]:  # 此函数使用递归
    """
    一些示例

    >>> longest_subsequence([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 41, 60, 80]
    >>> longest_subsequence([4, 8, 7, 5, 1, 12, 2, 3, 9])
    [1, 2, 3, 9]
    >>> longest_subsequence([28, 26, 12, 23, 35, 39])
    [12, 23, 35, 39]
    >>> longest_subsequence([9, 8, 7, 6, 5, 7])
    [5, 7]
    >>> longest_subsequence([1, 1, 1])
    [1, 1, 1]
    >>> longest_subsequence([])
    []
    """
    array_length = len(array)
    # 如果数组仅包含一个元素，则返回该元素（这是递归的终止条件）
    if array_length <= 1:
        return array
        # 否则
    pivot = array[0]
    is_found = False
    i = 1
    longest_subseq: list[int] = []
    while not is_found and i < array_length:
        if array[i] < pivot:
            is_found = True
            temp_array = array[i:]
            temp_array = longest_subsequence(temp_array)
            if len(temp_array) > len(longest_subseq):
                longest_subseq = temp_array
        else:
            i += 1

    temp_array = [element for element in array[1:] if element >= pivot]
    temp_array = [pivot, *longest_subsequence(temp_array)]
    if len(temp_array) > len(longest_subseq):
        return temp_array
    else:
        return longest_subseq


if __name__ == "__main__":
    import doctest

    doctest.testmod()
