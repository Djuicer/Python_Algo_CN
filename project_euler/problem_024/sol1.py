"""
排列是对象的一种有序安排。例如，3124 是数字 1, 2, 3 和 4 的一种可能排列。
如果按数字或字母顺序列出全部排列，就称为字典序。0, 1 和 2 的字典序排列为：

    012   021   102   120   201   210

数字 0, 1, 2, 3, 4, 5, 6, 7, 8 和 9 的第百万个字典序排列是什么？
"""

from itertools import permutations


def solution():
    """返回数字 0, 1, 2, 3, 4, 5, 6, 7, 8 和 9 的第百万个字典序排列。

    >>> solution()
    '2783915460'
    """
    result = list(map("".join, permutations("0123456789")))
    return result[999999]


if __name__ == "__main__":
    print(solution())
