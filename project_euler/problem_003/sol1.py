"""
Project Euler Problem 3: https://projecteuler.net/problem=3

最大质因数

13195 的质因数为 5、7、13 和 29。

数 600851475143 的最大质因数是多少？

参考资料：
    - https://en.wikipedia.org/wiki/Prime_number#Unique_factorization
"""

import math


def is_prime(number: int) -> bool:
    """以 O(sqrt(n)) 的时间复杂度检查一个数是否为质数。
    如果一个数恰好有两个因数：1 和它本身，则该数为质数。
    返回表示给定数是否为质数的布尔值。

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
        # 负数、0、1、所有偶数及所有 3 的倍数都不是质数
        return False

    # 所有大于 3 的质数都可表示为 6k +/- 1
    for i in range(5, int(math.sqrt(number) + 1), 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True


def solution(n: int = 600851475143) -> int:
    """
    返回给定数 n 的最大质因数。

    >>> solution(13195)
    29
    >>> solution(10)
    5
    >>> solution(17)
    17
    >>> solution(3.4)
    3
    >>> solution(0)
    Traceback (most recent call last):
        ...
    ValueError: Parameter n must be greater than or equal to one.
    >>> solution(-17)
    Traceback (most recent call last):
        ...
    ValueError: Parameter n must be greater than or equal to one.
    >>> solution([])
    Traceback (most recent call last):
        ...
    TypeError: Parameter n must be int or castable to int.
    >>> solution("asd")
    Traceback (most recent call last):
        ...
    TypeError: Parameter n must be int or castable to int.
    """

    try:
        n = int(n)
    except TypeError, ValueError:
        raise TypeError("Parameter n must be int or castable to int.")
    if n <= 0:
        raise ValueError("Parameter n must be greater than or equal to one.")
    max_number = 0
    if is_prime(n):
        return n
    while n % 2 == 0:
        n //= 2
    if is_prime(n):
        return n
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            if is_prime(n // i):
                max_number = n // i
                break
            if is_prime(i):
                max_number = i
    return max_number


if __name__ == "__main__":
    print(f"{solution() = }")
