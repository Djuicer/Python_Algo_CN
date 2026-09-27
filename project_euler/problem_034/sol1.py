"""
Problem 34: https://projecteuler.net/problem=34

145 是一个特殊的数，因为 1! + 4! + 5! = 1 + 24 + 120 = 145。
求所有等于其各位数字阶乘之和的数的总和。
注意：由于 1! = 1 和 2! = 2 不是和，因此不计入。
"""

from math import factorial

DIGIT_FACTORIAL = {str(d): factorial(d) for d in range(10)}


def sum_of_digit_factorial(n: int) -> int:
    """
    返回 n 的各位数字阶乘之和。
    >>> sum_of_digit_factorial(15)
    121
    >>> sum_of_digit_factorial(0)
    1
    """
    return sum(DIGIT_FACTORIAL[d] for d in str(n))


def solution() -> int:
    """
    返回所有等于其各位数字阶乘之和的数的总和。
    >>> solution()
    40730
    """
    limit = 7 * factorial(9) + 1
    return sum(i for i in range(3, limit) if sum_of_digit_factorial(i) == i)


if __name__ == "__main__":
    print(f"{solution() = }")
