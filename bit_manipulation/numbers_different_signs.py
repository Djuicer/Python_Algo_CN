"""
Author  : Alexander Pantyukhin
Date    : November 30, 2022

任务：
给定两个整数。如果它们的符号相反，则返回 True，否则返回 False。

实现说明：使用位运算。
对两个数执行异或运算。
"""


def different_signs(num1: int, num2: int) -> bool:
    """
    如果两个数的符号相反，则返回 True，否则返回 False。

    >>> different_signs(1, -1)
    True
    >>> different_signs(1, 1)
    False
    >>> different_signs(1000000000000000000000000000, -1000000000000000000000000000)
    True
    >>> different_signs(-1000000000000000000000000000, 1000000000000000000000000000)
    True
    >>> different_signs(50, 278)
    False
    >>> different_signs(0, 2)
    False
    >>> different_signs(2, 0)
    False
    """
    return num1 ^ num2 < 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
