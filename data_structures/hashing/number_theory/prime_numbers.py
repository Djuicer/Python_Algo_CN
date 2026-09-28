#!/usr/bin/env python3
"""
module 到 操作 带有 prime 数
"""

import math


def is_prime(number: int) -> bool:
    """Checks 到 see 如果一个 数 是 prime 在 O(sqrt(n))。

    数 是 prime 如果 它 具有 exactly 两个 factors: 1 并且 自身。

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

    # 前置条件
    assert isinstance(number, int) and (number >= 0), (
        "'number' must been an int and positive"
    )

    if 1 < number < 4:
        # 2 并且 3 是 primes
        return True
    elif number < 2 or not number % 2:
        # Negatives，0，1 并且 所有 偶数 数 是 不 primes
        return False

    odd_numbers = range(3, int(math.sqrt(number) + 1), 2)
    return not any(not number % i for i in odd_numbers)


def next_prime(value, factor=1, **kwargs):
    value = factor * value
    first_value_val = value

    while not is_prime(value):
        value += 1 if not ("desc" in kwargs and kwargs["desc"] is True) else -1

    if value == first_value_val:
        return next_prime(value + 1, **kwargs)
    return value
