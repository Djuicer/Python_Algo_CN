"""
Project Euler Problem 72: https://projecteuler.net/problem=72

考虑分数 n/d，其中 n 和 d 为正整数。如果 n<d 且 HCF(n,d)=1，则称其为最简真分数。

如果按大小升序列出 d ≤ 8 的最简真分数集合，可得：

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2,
4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

可以看出，该集合包含 21 个元素。

d ≤ 1,000,000 的最简真分数集合包含多少个元素？
"""


def solution(limit: int = 1000000) -> int:
    """
    返回分母小于 limit 的最简真分数数量。
    >>> solution(8)
    21
    >>> solution(1000)
    304191
    """
    primes = set(range(3, limit, 2))
    primes.add(2)
    for p in range(3, limit, 2):
        if p not in primes:
            continue
        primes.difference_update(set(range(p * p, limit, p)))

    phi = [float(n) for n in range(limit + 1)]

    for p in primes:
        for n in range(p, limit + 1, p):
            phi[n] *= 1 - 1 / p

    return int(sum(phi[2:]))


if __name__ == "__main__":
    print(f"{solution() = }")
