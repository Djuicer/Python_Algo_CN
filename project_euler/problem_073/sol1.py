"""
Project Euler Problem 73: https://projecteuler.net/problem=73

考虑分数 n/d，其中 n 和 d 为正整数。如果 n<d 且 HCF(n,d)=1，则称其为最简真分数。

如果按大小升序列出 d ≤ 8 的最简真分数集合，可得：

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3,
5/7, 3/4, 4/5, 5/6, 6/7, 7/8

可以看出，1/3 和 1/2 之间有 3 个分数。

在按大小排序且 d ≤ 12,000 的最简真分数集合中，1/3 和 1/2 之间有多少个分数？
"""

from math import gcd


def solution(max_d: int = 12_000) -> int:
    """
    返回按大小排序且 d ≤ max_d 的最简真分数集合中，位于 1/3 和 1/2 之间的分数数量。

    >>> solution(4)
    0

    >>> solution(5)
    1

    >>> solution(8)
    3
    """

    fractions_number = 0
    for d in range(max_d + 1):
        n_start = d // 3 + 1
        n_step = 1
        if d % 2 == 0:
            n_start += 1 - n_start % 2
            n_step = 2
        for n in range(n_start, (d + 1) // 2, n_step):
            if gcd(n, d) == 1:
                fractions_number += 1
    return fractions_number


if __name__ == "__main__":
    print(f"{solution() = }")
