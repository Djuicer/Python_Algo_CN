"""
Author  : Basuki Nath
Date    : 2025-10-04

用于整数的简单奇偶校验工具。

当置位比特的数量为奇数时，奇偶校验值为 1，否则为 0。
"""


def parity(number: int) -> int:
    """
    如果 `number` 的置位比特数量为奇数，则返回 1，否则返回 0。

    >>> parity(0)
    0
    >>> parity(1)
    1
    >>> parity(2)  # 10b -> one set bit
    1
    >>> parity(3)  # 11b -> two set bits
    0
    >>> parity(1023)  # 10 ones -> even
    0
    >>> parity(-1)
    Traceback (most recent call last):
        ...
    ValueError: number must not be negative
    """
    if number < 0:
        raise ValueError("number must not be negative")
    # 使用 Kernighan 算法切换奇偶校验值
    p = 0
    while number:
        p ^= 1
        number &= number - 1
    return p


if __name__ == "__main__":
    import doctest

    doctest.testmod()
