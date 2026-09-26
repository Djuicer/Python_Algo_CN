from math import log2


def binary_count_trailing_zeros(a: int) -> int:
    """
    接收一个整数，返回其二进制表示中末尾零的数量。

    >>> binary_count_trailing_zeros(25)
    0
    >>> binary_count_trailing_zeros(36)
    2
    >>> binary_count_trailing_zeros(16)
    4
    >>> binary_count_trailing_zeros(58)
    1
    >>> binary_count_trailing_zeros(4294967296)
    32
    >>> binary_count_trailing_zeros(0)
    Traceback (most recent call last):
        ...
    ValueError: Trailing zeros for 0 are undefined
    >>> binary_count_trailing_zeros(-10)
    Traceback (most recent call last):
        ...
    ValueError: Input value must be a positive integer
    >>> binary_count_trailing_zeros(0.8)
    Traceback (most recent call last):
        ...
    TypeError: Input value must be an integer
    >>> binary_count_trailing_zeros("0")
    Traceback (most recent call last):
        ...
    TypeError: Input value must be an integer
    """

    # 类型检查
    if not isinstance(a, int):
        raise TypeError("Input value must be an integer")

    # 边界情况：零
    if a == 0:
        raise ValueError("Trailing zeros for 0 are undefined")

    # 不允许负数
    if a < 0:
        raise ValueError("Input value must be a positive integer")

    # 核心逻辑
    return int(log2(a & -a))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
