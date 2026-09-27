"""
Problem 46: https://projecteuler.net/problem=46

Christian Goldbach 曾提出，每个奇合数都可以写成一个素数与一个平方数两倍之和。

9 = 7 + 2 x 12
15 = 7 + 2 x 22
21 = 3 + 2 x 32
25 = 7 + 2 x 32
27 = 19 + 2 x 22
33 = 31 + 2 x 12

事实证明，这个猜想是错误的。

不能写成一个素数与一个平方数两倍之和的最小奇合数是多少？
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


odd_composites = [num for num in range(3, 100001, 2) if not is_prime(num)]


def compute_nums(n: int) -> list[int]:
    """
    返回前 n 个不符合该猜想的奇合数列表。
    >>> compute_nums(1)
    [5777]
    >>> compute_nums(2)
    [5777, 5993]
    >>> compute_nums(0)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0
    >>> compute_nums("a")
    Traceback (most recent call last):
        ...
    ValueError: n must be an integer
    >>> compute_nums(1.1)
    Traceback (most recent call last):
        ...
    ValueError: n must be an integer

    """
    if not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n <= 0:
        raise ValueError("n must be >= 0")

    list_nums = []
    for num in range(len(odd_composites)):
        i = 0
        while 2 * i * i <= odd_composites[num]:
            rem = odd_composites[num] - 2 * i * i
            if is_prime(rem):
                break
            i += 1
        else:
            list_nums.append(odd_composites[num])
            if len(list_nums) == n:
                return list_nums

    return []


def solution() -> int:
    """返回该问题的解。"""
    return compute_nums(1)[0]


if __name__ == "__main__":
    print(f"{solution() = }")
