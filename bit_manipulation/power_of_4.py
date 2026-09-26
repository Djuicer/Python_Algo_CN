"""

任务：
给定一个正整数。如果该数是 4 的幂，则返回 True，否则返回 False。

实现说明：使用位运算。
例如，如果该数是 2 的幂，其二进制表示为：
n     = 0..100..00
n - 1 = 0..011..11

n & (n - 1) 没有重合的置位比特，结果为 0
如果该数是 4 的幂，则它应当也是 2 的幂，且置位比特应位于奇数位置。
"""


def power_of_4(number: int) -> bool:
    """
    如果该数是 4 的幂，则返回 True，否则返回 False。

    >>> power_of_4(0)
    Traceback (most recent call last):
        ...
    ValueError: number must be positive
    >>> power_of_4(1)
    True
    >>> power_of_4(2)
    False
    >>> power_of_4(4)
    True
    >>> power_of_4(6)
    False
    >>> power_of_4(8)
    False
    >>> power_of_4(17)
    False
    >>> power_of_4(64)
    True
    >>> power_of_4(-1)
    Traceback (most recent call last):
        ...
    ValueError: number must be positive
    >>> power_of_4(1.2)
    Traceback (most recent call last):
        ...
    TypeError: number must be an integer

    """
    if not isinstance(number, int):
        raise TypeError("number must be an integer")
    if number <= 0:
        raise ValueError("number must be positive")
    if number & (number - 1) == 0:
        c = 0
        while number:
            c += 1
            number >>= 1
        return c % 2 == 1
    else:
        return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
