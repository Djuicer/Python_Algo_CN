"""
Author  : Naman Sharma
Date    : October 2, 2023

任务：
求小于或等于给定数的最大 2 的幂。

实现说明：使用位运算。
从 1 开始，左移置位比特，并检查 (res << 1) <= number 是否成立。
每次向左移一位都表示 2 的一个幂。

示例：
number: 15
res:    1   0b1
        2   0b10
        4   0b100
        8   0b1000
        16  0b10000（退出）
"""


def largest_pow_of_two_le_num(number: int) -> int:
    """
    返回小于或等于给定数的最大 2 的幂。

    >>> largest_pow_of_two_le_num(0)
    0
    >>> largest_pow_of_two_le_num(1)
    1
    >>> largest_pow_of_two_le_num(-1)
    0
    >>> largest_pow_of_two_le_num(3)
    2
    >>> largest_pow_of_two_le_num(15)
    8
    >>> largest_pow_of_two_le_num(99)
    64
    >>> largest_pow_of_two_le_num(178)
    128
    >>> largest_pow_of_two_le_num(999999)
    524288
    >>> largest_pow_of_two_le_num(99.9)
    Traceback (most recent call last):
        ...
    TypeError: Input value must be a 'int' type
    """
    if isinstance(number, float):
        raise TypeError("Input value must be a 'int' type")
    if number <= 0:
        return 0
    res = 1
    while (res << 1) <= number:
        res <<= 1
    return res


if __name__ == "__main__":
    import doctest

    doctest.testmod()
