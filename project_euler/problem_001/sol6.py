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

    a = 3
    result = 0
    while a < n:
        if a % 3 == 0 or a % 5 == 0:
            result += a
        elif a % 15 == 0:
            result -= a
        a += 1
    return result


if __name__ == "__main__":
    print(f"{solution() = }")
