"""
Author  : Basuki Nath
Date    : 2025-10-04

用于计算大于或等于 n 的最小 2 的幂的工具。
"""


def next_power_of_two(n: int) -> int:
    """
    对于正整数 n，返回满足 >= n 的最小 2 的幂。

    >>> next_power_of_two(1)
    1
    >>> next_power_of_two(2)
    2
    >>> next_power_of_two(3)
    4
    >>> next_power_of_two(5)
    8
    >>> next_power_of_two(1025)
    2048
    >>> next_power_of_two(0)
    Traceback (most recent call last):
        ...
    ValueError: n must be positive
    >>> next_power_of_two(-3)
    Traceback (most recent call last):
        ...
    ValueError: n must be positive
    """
    if n <= 0:
        raise ValueError("n must be positive")
    # 如果已经是 2 的幂，则直接返回
    if n & (n - 1) == 0:
        return n
    # 否则，将右侧各位填充为 1
    v = n - 1
    v |= v >> 1
    v |= v >> 2
    v |= v >> 4
    v |= v >> 8
    v |= v >> 16
    # 对于非常大的整数，利用 Python 的任意精度继续移位
    shift = 32
    while (1 << shift) <= v:
        v |= v >> shift
        shift <<= 1
    return v + 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
