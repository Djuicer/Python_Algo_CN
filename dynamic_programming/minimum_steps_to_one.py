"""
YouTube Explanation: https://www.youtube.com/watch?v=f2xi3c1S95M

给定整数 n，返回从 n 变为 1 所需的最少步骤数。

可用步骤：
    * 减去 1
    * 如果 n 能被 2 整除，则除以 2
    * 如果 n 能被 3 整除，则除以 3


示例 1：n = 10
10 -> 9 -> 3 -> 1
结果：3 步

示例 2：n = 15
15 -> 5 -> 4 -> 2 -> 1
结果：4 步

示例 3：n = 6
6 -> 2 -> 1
结果：2 步
"""

from __future__ import annotations

__author__ = "Alexander Joslin"


def min_steps_to_one(number: int) -> int:
    """
    使用表格法（Tabulation）实现变为 1 的最少步骤数。
    >>> min_steps_to_one(10)
    3
    >>> min_steps_to_one(15)
    4
    >>> min_steps_to_one(6)
    2

    :param number:
    :return int:
    """

    if number <= 0:
        msg = f"n must be greater than 0. Got n = {number}"
        raise ValueError(msg)

    table = [number + 1] * (number + 1)

    # 起始位置
    table[1] = 0
    for i in range(1, number):
        table[i + 1] = min(table[i + 1], table[i] + 1)
        # 检查是否越界
        if i * 2 <= number:
            table[i * 2] = min(table[i * 2], table[i] + 1)
        # 检查是否越界
        if i * 3 <= number:
            table[i * 3] = min(table[i * 3], table[i] + 1)
    return table[number]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
