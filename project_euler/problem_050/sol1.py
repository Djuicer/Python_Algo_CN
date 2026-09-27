"""
Project Euler Problem 50: https://projecteuler.net/problem=50

连续素数和

素数 41 可以写成六个连续素数之和：
41 = 2 + 3 + 5 + 7 + 11 + 13

在一百以下可得到素数的连续素数和中，这是项数最多的一个。

在一千以下，可得到素数且项数最多的连续素数和包含 21 项，其值为 953。

一百万以下哪个素数可以写成最多个连续素数之和？
"""

from __future__ import annotations


def prime_sieve(limit: int) -> list[int]:
    """
    埃拉托斯特尼筛法（Sieve of Eratosthenes）。
    返回小于数字 'limit' 的所有素数。
    https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

    >>> prime_sieve(3)
    [2]

    >>> prime_sieve(50)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    """
    is_prime = [True] * limit
    is_prime[0] = False
    is_prime[1] = False
    is_prime[2] = True

    for i in range(3, int(limit**0.5 + 1), 2):
        index = i * 2
        while index < limit:
            is_prime[index] = False
            index = index + i

    primes = [2]

    for i in range(3, limit, 2):
        if is_prime[i]:
            primes.append(i)

    return primes


def solution(ceiling: int = 1_000_000) -> int:
    """
    返回小于上限且可写成最多个连续素数之和的最大素数。

    >>> solution(500)
    499

    >>> solution(1_000)
    953

    >>> solution(10_000)
    9521
    """
    primes = prime_sieve(ceiling)
    length = 0
    largest = 0

    for i in range(len(primes)):
        for j in range(i + length, len(primes)):
            sol = sum(primes[i:j])
            if sol >= ceiling:
                break

            if sol in primes:
                length = j - i
                largest = sol

    return largest


if __name__ == "__main__":
    print(f"{solution() = }")
