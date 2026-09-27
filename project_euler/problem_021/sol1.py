"""
亲和数
问题 21

定义 d(n) 为 n 的真约数（小于 n 且能整除 n 的数）之和。
如果 d(a) = b 且 d(b) = a，其中 a ≠ b，那么 a 和 b 构成一对亲和数，
a 与 b 各自都称为亲和数。

例如，220 的真约数为 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 和 110；
因此 d(220) = 284。284 的真约数为 1, 2, 4, 71 和 142；所以 d(284) = 220。

求 10000 以下所有亲和数之和。
"""

from math import sqrt


def sum_of_divisors(n: int) -> int:
    total = 0
    for i in range(1, int(sqrt(n) + 1)):
        if n % i == 0 and i != sqrt(n):
            total += i + n // i
        elif i == sqrt(n):
            total += i
    return total - n


def solution(n: int = 10000) -> int:
    """返回 n 以下所有亲和数之和。

    >>> solution(10000)
    31626
    >>> solution(5000)
    8442
    >>> solution(1000)
    504
    >>> solution(100)
    0
    >>> solution(50)
    0
    """
    total = sum(
        i
        for i in range(1, n)
        if sum_of_divisors(sum_of_divisors(i)) == i and sum_of_divisors(i) != i
    )
    return total


if __name__ == "__main__":
    print(solution(int(str(input()).strip())))
