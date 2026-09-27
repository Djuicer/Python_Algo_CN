"""
Project Euler Problem 131: https://projecteuler.net/problem=131

对于某些素数 p，存在正整数 n，使表达式 n^3 + n^2p 为完全立方数。

例如，当 p = 19 时，8^3 + 8^2 x 19 = 12^3。

更令人惊讶的是，对于每个具有此性质的素数，n 的值都是唯一的；一百以下只有四个
这样的素数。

一百万以下有多少个素数具有这一非凡性质？
"""

from math import isqrt


def is_prime(number: int) -> bool:
    """
    判断 number 是否为素数。

    >>> is_prime(3)
    True

    >>> is_prime(4)
    False
    """

    return all(number % divisor != 0 for divisor in range(2, isqrt(number) + 1))


def solution(max_prime: int = 10**6) -> int:
    """
    返回 max_prime 以下具有该性质的素数数量。

    >>> solution(100)
    4
    """

    primes_count = 0
    cube_index = 1
    prime_candidate = 7
    while prime_candidate < max_prime:
        primes_count += is_prime(prime_candidate)

        cube_index += 1
        prime_candidate += 6 * cube_index

    return primes_count


if __name__ == "__main__":
    print(f"{solution() = }")
