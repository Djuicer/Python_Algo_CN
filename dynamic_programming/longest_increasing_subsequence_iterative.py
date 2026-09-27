"""
Author  : Sanjay Muthu <https://github.com/XenoBytesX>

这是使用纯 Python 实现的给定序列最长递增子序列动态规划（Dynamic Programming）解法。

问题如下：
    给定一个数组，查找并返回其中最长的递增子数组。

示例：
    输入 ``[10, 22, 9, 33, 21, 50, 41, 60, 80]`` 将返回
    ``[10, 22, 33, 50, 60, 80]``。
"""

from __future__ import annotations

import copy


def longest_subsequence(array: list[int]) -> list[int]:
    """
    一些示例

    >>> longest_subsequence([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 50, 60, 80]
    >>> longest_subsequence([4, 8, 7, 5, 1, 12, 2, 3, 9])
    [1, 2, 3, 9]
    >>> longest_subsequence([9, 8, 7, 6, 5, 7])
    [7, 7]
    >>> longest_subsequence([28, 26, 12, 23, 35, 39])
    [12, 23, 35, 39]
    >>> longest_subsequence([1, 1, 1])
    [1, 1, 1]
    >>> longest_subsequence([])
    []
    """
    n = len(array)
    # 以 array[i] 结尾的最长递增子序列
    longest_increasing_subsequence = []
    for i in range(n):
        longest_increasing_subsequence.append([array[i]])

    for i in range(1, n):
        for prev in range(i):
            # 如果 array[prev] 小于或等于 array[i]，则
            # longest_increasing_subsequence[prev] + array[i]
            # 是有效的递增子序列

            # 仅当长度更长时，才将 longest_increasing_subsequence[i] 设为
            # longest_increasing_subsequence[prev] + array[i]

            if array[prev] <= array[i] and len(
                longest_increasing_subsequence[prev]
            ) + 1 > len(longest_increasing_subsequence[i]):
                longest_increasing_subsequence[i] = copy.copy(
                    longest_increasing_subsequence[prev]
                )
                longest_increasing_subsequence[i].append(array[i])

    result: list[int] = []
    for i in range(n):
        if len(longest_increasing_subsequence[i]) > len(result):
            result = longest_increasing_subsequence[i]

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
