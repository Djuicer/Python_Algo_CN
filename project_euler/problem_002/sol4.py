"""
Project Euler Problem 2: https://projecteuler.net/problem=2

偶数斐波那契数

斐波那契数列中的每个新项都由前两项相加得到。从 1 和 2 开始，前 10 项为：

1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

考虑斐波那契数列中值不超过四百万的项，求其中偶数项之和。

参考资料：
    - https://en.wikipedia.org/wiki/Fibonacci_number
"""

import math
from decimal import Decimal, getcontext


def solution(n: int = 4000000) -> int:
    """
    返回斐波那契数列中所有小于或等于 n 的偶数项之和。

    >>> solution(10)
    10
    >>> solution(15)
    10
    >>> solution(2)
    2
    >>> solution(1)
    0
    >>> solution(34)
    44
    >>> solution(3.4)
    2
    >>> solution(0)
    Traceback (most recent call last):
        ...
    ValueError: Parameter n must be greater than or equal to one.
    >>> solution(-17)
    Traceback (most recent call last):
        ...
    ValueError: Parameter n must be greater than or equal to one.
    >>> solution([])
    Traceback (most recent call last):
        ...
    TypeError: Parameter n must be int or castable to int.
    >>> solution("asd")
    Traceback (most recent call last):
        ...
    TypeError: Parameter n must be int or castable to int.
    """

    try:
        n = int(n)
    except TypeError, ValueError:
        raise TypeError("Parameter n must be int or castable to int.")
    if n <= 0:
        raise ValueError("Parameter n must be greater than or equal to one.")
    getcontext().prec = 100
    phi = (Decimal(5) ** Decimal("0.5") + 1) / Decimal(2)

    index = (math.floor(math.log(n * (phi + 2), phi) - 1) // 3) * 3 + 2
    num = Decimal(round(phi ** Decimal(index + 1))) / (phi + 2)
    total = num // 2
    return int(total)


if __name__ == "__main__":
    print(f"{solution() = }")
