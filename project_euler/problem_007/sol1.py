"""
Project Euler Problem 7: https://projecteuler.net/problem=7

第 10001 个质数

列出前六个质数：2、3、5、7、11 和 13，可知第 6 个质数是 13。

第 10001 个质数是多少？

参考资料：
    - https://en.wikipedia.org/wiki/Prime_number
"""

from math import sqrt


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
    for i in range(5, int(sqrt(number) + 1), 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True


def solution(nth: int = 10001) -> int:
    """
    返回第 n 个质数。

    >>> solution(6)
    13
    >>> solution(1)
    2
    >>> solution(3)
    5
    >>> solution(20)
    71
    >>> solution(50)
    229
    >>> solution(100)
    541
    """

    count = 0
    number = 1
    while count != nth and number < 3:
        number += 1
        if is_prime(number):
            count += 1
    while count != nth:
        number += 2
        if is_prime(number):
            count += 1
    return number


if __name__ == "__main__":
    print(f"{solution() = }")
