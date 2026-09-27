"""
Problem 13: https://projecteuler.net/problem=13

题目说明：
求以下一百个 50 位数之和的前十位数字。
"""

import os


def solution():
    """
    返回文件 num.txt 中数组元素之和的前十位数字。

    >>> solution()
    '5537376230'
    """
    file_path = os.path.join(os.path.dirname(__file__), "num.txt")
    with open(file_path) as file_hand:
        return str(sum(int(line) for line in file_hand))[:10]


if __name__ == "__main__":
    print(solution())
