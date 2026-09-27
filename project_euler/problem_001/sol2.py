"""
Project Euler Problem 1: https://projecteuler.net/problem=1

3 和 5 的倍数

列出所有小于 10 且是 3 或 5 的倍数的自然数，可得 3、5、6 和 9。
这些倍数之和为 23。

求所有小于 1000 且是 3 或 5 的倍数的数之和。
"""


def solution(n: int = 1000) -> int:
    """
    返回所有小于 n 且是 3 或 5 的倍数的数之和。

    >>> solution(3)
    0
    >>> solution(4)
    3
    >>> solution(10)
    23
    >>> solution(600)
    83700
    """

    total = 0
    terms = (n - 1) // 3
    total += ((terms) * (6 + (terms - 1) * 3)) // 2  # total of an A.P.
    terms = (n - 1) // 5
    total += ((terms) * (10 + (terms - 1) * 5)) // 2
    terms = (n - 1) // 15
    total -= ((terms) * (30 + (terms - 1) * 15)) // 2
    return total


if __name__ == "__main__":
    print(f"{solution() = }")
