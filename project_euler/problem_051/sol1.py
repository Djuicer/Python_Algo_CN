"""
https://projecteuler.net/problem=51
素数数字替换
Problem 51

替换两位数 *3 的第 1 位数字后，九个可能值中的六个：13, 23, 43, 53, 73 和 83
都是素数。

用同一个数字替换 56**3 的第 3 和第 4 位后，这个 5 位数是首个在生成的十个数中
有七个素数的示例，得到素数族：56003, 56113, 56333, 56443, 56663, 56773 和 56993。
因此，作为该素数族的第一个成员，56003 是具有此性质的最小素数。

找出最小的素数：将其部分数字（不必相邻）替换为同一个数字后，它属于一个包含
八个素数的素数族。
"""

from __future__ import annotations

from collections import Counter


def prime_sieve(n: int) -> list[int]:
    """
    埃拉托斯特尼筛法（Sieve of Eratosthenes）。
    返回小于某个数的所有素数。
    https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

    >>> prime_sieve(3)
    [2]

    >>> prime_sieve(50)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    """
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False
    is_prime[2] = True

    for i in range(3, int(n**0.5 + 1), 2):
        index = i * 2
        while index < n:
            is_prime[index] = False
            index = index + i

    primes = [2]

    for i in range(3, n, 2):
        if is_prime[i]:
            primes.append(i)

    return primes


def digit_replacements(number: int) -> list[list[int]]:
    """
    返回一个至少含有一个重复数字的数通过数字替换所得的所有可能数族。

    >>> digit_replacements(544)
    [[500, 511, 522, 533, 544, 555, 566, 577, 588, 599]]

    >>> digit_replacements(3112)
    [[3002, 3112, 3222, 3332, 3442, 3552, 3662, 3772, 3882, 3992]]
    """
    number_str = str(number)
    replacements = []
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    for duplicate in Counter(number_str) - Counter(set(number_str)):
        family = [int(number_str.replace(duplicate, digit)) for digit in digits]
        replacements.append(family)

    return replacements


def solution(family_length: int = 8) -> int:
    """
    返回该问题的解。

    >>> solution(2)
    229399

    >>> solution(3)
    221311
    """
    numbers_checked = set()

    # 筛除可替换数字少于 3 个的质数
    primes = {
        x for x in set(prime_sieve(1_000_000)) if len(str(x)) - len(set(str(x))) >= 3
    }

    for prime in primes:
        if prime in numbers_checked:
            continue

        replacements = digit_replacements(prime)

        for family in replacements:
            numbers_checked.update(family)
            primes_in_family = primes.intersection(family)

            if len(primes_in_family) != family_length:
                continue

            return min(primes_in_family)

    return -1


if __name__ == "__main__":
    print(solution())
