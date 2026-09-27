"""
可截断素数
Problem 37: https://projecteuler.net/problem=37

数 3797 具有一个有趣的性质。它本身是素数，从左到右连续移除数字时，
每一步仍为素数：3797, 797, 97 和 7。从右到左也同样如此：3797, 379, 37 和 3。

求仅有的十一个可从左到右和从右到左截断的素数之和。

注意：2, 3, 5 和 7 不视为可截断素数。
"""

from __future__ import annotations

import math


def is_prime(number: int) -> bool:
    """以 O(sqrt(n)) 的时间复杂度检查一个数是否为素数。

    如果一个数恰好有两个因数（1 和它本身），则它是素数。

    >>> is_prime(0)
    False
    >>> is_prime(1)
    False
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(27)
    False
    >>> is_prime(87)
    False
    >>> is_prime(563)
    True
    >>> is_prime(2999)
    True
    >>> is_prime(67483)
    False
    """

    if 1 < number < 4:
        # 2 和 3 是质数
        return True
    elif number < 2 or number % 2 == 0 or number % 3 == 0:
        # 负数、0、1、所有偶数以及 3 的倍数都不是质数
        return False

    # 所有质数都形如 6k +/- 1
    for i in range(5, int(math.sqrt(number) + 1), 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True


def list_truncated_nums(n: int) -> list[int]:
    """
    返回 n 从左侧和右侧截断所得的所有数字列表。
    >>> list_truncated_nums(927628)
    [927628, 27628, 92762, 7628, 9276, 628, 927, 28, 92, 8, 9]
    >>> list_truncated_nums(467)
    [467, 67, 46, 7, 4]
    >>> list_truncated_nums(58)
    [58, 8, 5]
    """
    str_num = str(n)
    list_nums = [n]
    for i in range(1, len(str_num)):
        list_nums.append(int(str_num[i:]))
        list_nums.append(int(str_num[:-i]))
    return list_nums


def validate(n: int) -> bool:
    """
    为优化方法，排除大于 1000 且前三位或后三位不是素数的数字。
    >>> validate(74679)
    False
    >>> validate(235693)
    False
    >>> validate(3797)
    True
    """
    return not (
        len(str(n)) > 3
        and (not is_prime(int(str(n)[-3:])) or not is_prime(int(str(n)[:3])))
    )


def compute_truncated_primes(count: int = 11) -> list[int]:
    """
    返回可截断素数列表。
    >>> compute_truncated_primes(11)
    [23, 37, 53, 73, 313, 317, 373, 797, 3137, 3797, 739397]
    """
    list_truncated_primes: list[int] = []
    num = 13
    while len(list_truncated_primes) != count:
        if validate(num):
            list_nums = list_truncated_nums(num)
            if all(is_prime(i) for i in list_nums):
                list_truncated_primes.append(num)
        num += 2
    return list_truncated_primes


def solution() -> int:
    """
    返回可截断素数之和。
    """
    return sum(compute_truncated_primes(11))


if __name__ == "__main__":
    print(f"{sum(compute_truncated_primes(11)) = }")
