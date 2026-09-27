"""
Project Euler Problem 64: https://projecteuler.net/problem=64

所有平方根写成连分数时都是周期性的。例如，考虑 sqrt(23)，可以看出该数列会重复。
为简洁起见，使用记号 sqrt(23)=[4;(1,3,1,8)] 表示块 (1,3,1,8) 无限重复。
当 N<=13 时，恰有四个连分数的周期为奇数。N<=10000 时有多少个连分数的周期为奇数？

参考资料：
- https://en.wikipedia.org/wiki/Continued_fraction
"""

from math import floor, sqrt


def continuous_fraction_period(n: int) -> int:
    """
    返回数字 n 的连分数周期。

    >>> continuous_fraction_period(2)
    1
    >>> continuous_fraction_period(5)
    1
    >>> continuous_fraction_period(7)
    4
    >>> continuous_fraction_period(11)
    2
    >>> continuous_fraction_period(13)
    5
    """
    numerator = 0.0
    denominator = 1.0
    root = int(sqrt(n))
    integer_part = root
    period = 0
    while integer_part != 2 * root:
        numerator = denominator * integer_part - numerator
        denominator = (n - numerator**2) / denominator
        integer_part = int((root + numerator) / denominator)
        period += 1
    return period


def solution(n: int = 10000) -> int:
    """
    返回 <= 10000 且周期为奇数的数字数量。
    此函数对非完全平方数调用 continuous_fraction_period，
    通过 if sr - floor(sr) != 0 语句进行判断。
    如果 continuous_fraction_period 返回奇数周期，则 count_odd_periods 增加 1。

    >>> solution(2)
    1
    >>> solution(5)
    2
    >>> solution(7)
    2
    >>> solution(11)
    3
    >>> solution(13)
    4
    """
    count_odd_periods = 0
    for i in range(2, n + 1):
        sr = sqrt(i)
        if sr - floor(sr) != 0 and continuous_fraction_period(i) % 2 == 1:
            count_odd_periods += 1
    return count_odd_periods


if __name__ == "__main__":
    print(f"{solution(int(input().strip()))}")
