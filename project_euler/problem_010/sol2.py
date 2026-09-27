"""
Project Euler Problem 10: https://projecteuler.net/problem=10

质数求和

小于 10 的质数之和为 2 + 3 + 5 + 7 = 17。

求所有小于两百万的质数之和。

参考资料：
    - https://en.wikipedia.org/wiki/Prime_number
"""

import math
from collections.abc import Iterator
from itertools import takewhile


def is_prime(number: int) -> bool:
    """以 O(sqrt(n)) 的时间复杂度检查一个数是否为质数。
    如果一个数恰好有两个因数：1 和它本身，则该数为质数。
    返回表示给定数 num 是否为质数的布尔值。

    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(27)
    False
    >>> is_prime(2999)
    True
    >>> is_prime(0)
    False
    >>> is_prime(1)
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


def prime_generator() -> Iterator[int]:
    """
    生成质数列表
    """

    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1


def solution(n: int = 2000000) -> int:
    """
    返回所有小于 n 的质数之和。

    >>> solution(1000)
    76127
    >>> solution(5000)
    1548136
    >>> solution(10000)
    5736396
    >>> solution(7)
    10
    """

    return sum(takewhile(lambda x: x < n, prime_generator()))


if __name__ == "__main__":
    print(f"{solution() = }")
