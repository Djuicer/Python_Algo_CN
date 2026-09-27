"""
Project Euler Problem 77: https://projecteuler.net/problem=77

将十写成素数之和，恰好有五种不同方式：

7 + 3
5 + 5
5 + 3 + 2
3 + 3 + 2 + 2
2 + 2 + 2 + 2 + 2

第一个能以超过五千种不同方式写成素数之和的数是多少？
"""

from __future__ import annotations

from functools import lru_cache
from math import ceil

NUM_PRIMES = 100

primes = set(range(3, NUM_PRIMES, 2))
primes.add(2)
prime: int

for prime in range(3, ceil(NUM_PRIMES**0.5), 2):
    if prime not in primes:
        continue
    primes.difference_update(set(range(prime * prime, NUM_PRIMES, prime)))


@lru_cache(maxsize=100)
def partition(number_to_partition: int) -> set[int]:
    """
    返回与 n 的不同素数划分对应的整数集合。
    不同素数划分可表示为不同的素数分解，例如
    (7+3) <-> 7*3 = 12, (3+3+2+2) = 3*3*2*2 = 36
    >>> partition(10)
    {32, 36, 21, 25, 30}
    >>> partition(15)
    {192, 160, 105, 44, 112, 243, 180, 150, 216, 26, 125, 126}
    >>> len(partition(20))
    26
    """
    if number_to_partition < 0:
        return set()
    elif number_to_partition == 0:
        return {1}

    ret: set[int] = set()
    prime: int
    sub: int

    for prime in primes:
        if prime > number_to_partition:
            continue
        for sub in partition(number_to_partition - prime):
            ret.add(sub * prime)

    return ret


def solution(number_unique_partitions: int = 5000) -> int | None:
    """
    返回能以超过 m 种不同方式写成素数之和的最小整数。
    >>> solution(4)
    10
    >>> solution(500)
    45
    >>> solution(1000)
    53
    """
    for number_to_partition in range(1, NUM_PRIMES):
        if len(partition(number_to_partition)) > number_unique_partitions:
            return number_to_partition
    return None


if __name__ == "__main__":
    print(f"{solution() = }")
