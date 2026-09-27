"""
Project Euler Problem 35
https://projecteuler.net/problem=35

题目说明：

数 197 称为循环素数，因为其数字的所有循环排列 197, 971 和 719 本身都是素数。
100 以下共有十三个这样的素数：2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73,
79 和 97。一百万以下有多少个循环素数？

为高效解决此问题，先使用埃拉托斯特尼筛法标记一百万以下的所有素数，
再排除其中含有偶数数字的数。随后生成每个数的所有循环排列，并检查它们是否全为素数。
"""

from __future__ import annotations

sieve = [True] * 1000001
i = 2
while i * i <= 1000000:
    if sieve[i]:
        for j in range(i * i, 1000001, i):
            sieve[j] = False
    i += 1


def is_prime(n: int) -> bool:
    """
    对于 2 <= n <= 1000000，如果 n 是素数则返回 True。
    >>> is_prime(87)
    False
    >>> is_prime(23)
    True
    >>> is_prime(25363)
    False
    """
    return sieve[n]


def contains_an_even_digit(n: int) -> bool:
    """
    如果 n 包含偶数数字，则返回 True。
    >>> contains_an_even_digit(0)
    True
    >>> contains_an_even_digit(975317933)
    False
    >>> contains_an_even_digit(-245679)
    True
    """
    return any(digit in "02468" for digit in str(n))


def find_circular_primes(limit: int = 1000000) -> list[int]:
    """
    返回 limit 以下的循环素数。
    >>> len(find_circular_primes(100))
    13
    >>> len(find_circular_primes(1000000))
    55
    """
    result = [2]  # result 已包含数字 2
    for num in range(3, limit + 1, 2):
        if is_prime(num) and not contains_an_even_digit(num):
            str_num = str(num)
            list_nums = [int(str_num[j:] + str_num[:j]) for j in range(len(str_num))]
            if all(is_prime(i) for i in list_nums):
                result.append(num)
    return result


def solution() -> int:
    """
    >>> solution()
    55
    """
    return len(find_circular_primes())


if __name__ == "__main__":
    print(f"{len(find_circular_primes()) = }")
