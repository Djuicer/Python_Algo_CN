"""
Author  : Alexander Pantyukhin
Date    : November 1, 2022

任务：
给定一个正整数。如果该数是 2 的幂，则返回 True，否则返回 False。

实现说明：使用位运算。
例如，如果该数是 2 的幂，其二进制表示为：
n     = 0..100..00
n - 1 = 0..011..11

n & (n - 1) 没有重合的置位比特，结果为 0
"""


def is_power_of_two(number: int) -> bool:
    """
    如果该数是 2 的幂，则返回 True，否则返回 False。

    >>> is_power_of_two(0)
    True
    >>> is_power_of_two(1)
    True
    >>> is_power_of_two(2)
    True
    >>> is_power_of_two(4)
    True
    >>> is_power_of_two(6)
    False
    >>> is_power_of_two(8)
    True
    >>> is_power_of_two(17)
    False
    >>> is_power_of_two(1024)
    True
    >>> is_power_of_two(1023)
    False
    >>> is_power_of_two(-1)
    Traceback (most recent call last):
        ...
    ValueError: number must not be negative
    >>> is_power_of_two(1.2)
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for &: 'float' and 'float'

    # Test all powers of 2 from 0 to 10,000
    >>> all(is_power_of_two(int(2 ** i)) for i in range(10000))
    True
    """
    if number < 0:
        raise ValueError("number must not be negative")
    return number & (number - 1) == 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
