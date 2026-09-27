"""
Problem 119: https://projecteuler.net/problem=119

名称：数字幂和

数字 512 很有趣，因为它等于其各位数字之和的某次幂：5 + 1 + 2 = 8，且 8^3 = 512。
具有该性质的另一个数是 614656 = 28^4。定义 an 为该数列第 n 项，并规定一个数必须
至少包含两位才有数字和。已知 a2 = 512 且 a10 = 614656，求 a30。
"""

import math


def digit_sum(n: int) -> int:
    """
    返回该数的各位数字之和。
    >>> digit_sum(123)
    6
    >>> digit_sum(456)
    15
    >>> digit_sum(78910)
    25
    """
    return sum(int(digit) for digit in str(n))


def solution(n: int = 30) -> int:
    """
    返回第 30 个数字幂和的值。
    >>> solution(2)
    512
    >>> solution(5)
    5832
    >>> solution(10)
    614656
    """
    digit_to_powers = []
    for digit in range(2, 100):
        for power in range(2, 100):
            number = int(math.pow(digit, power))
            if digit == digit_sum(number):
                digit_to_powers.append(number)

    digit_to_powers.sort()
    return digit_to_powers[n - 1]


if __name__ == "__main__":
    print(solution())
