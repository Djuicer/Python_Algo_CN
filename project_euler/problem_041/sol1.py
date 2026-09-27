"""
全数字素数
Problem 41: https://projecteuler.net/problem=41

如果一个 n 位数恰好使用了 1 到 n 的每个数字一次，就称其为全数字数。
例如，2143 是一个 4 位全数字数，同时也是素数。最大的 n 位全数字素数是多少？

除 1、4、7 位全数字数外，其他位数的全数字数都能被 3 整除。
因此只检查 7 位全数字数，以得到可能的最大全数字素数。
"""

from __future__ import annotations

import math
from itertools import permutations


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


def solution(n: int = 7) -> int:
    """
    返回长度为 n 的最大全数字素数。如果不存在，则返回 0。
    >>> solution(2)
    0
    >>> solution(4)
    4231
    >>> solution(7)
    7652413
    """
    pandigital_str = "".join(str(i) for i in range(1, n + 1))
    perm_list = [int("".join(i)) for i in permutations(pandigital_str, n)]
    pandigitals = [num for num in perm_list if is_prime(num)]
    return max(pandigitals) if pandigitals else 0


if __name__ == "__main__":
    print(f"{solution() = }")
