"""
Project Euler Problem 129: https://projecteuler.net/problem=129

完全由数字一组成的数称为重复单位数（repunit）。定义 R(k) 为长度为 k 的重复单位数；
例如，R(6) = 111111。

给定正整数 n 且 GCD(n, 10) = 1，可以证明总存在 k，使 R(k) 可被 n 整除。
令 A(n) 为满足条件的最小 k；例如，A(7) = 6 且 A(41) = 5。

使 A(n) 首次超过十的最小 n 值为 17。

求使 A(n) 首次超过一百万的最小 n 值。
"""


def least_divisible_repunit(divisor: int) -> int:
    """
    返回使长度为 k 的重复单位数可被 divisor 整除的最小 k 值。
    >>> least_divisible_repunit(7)
    6
    >>> least_divisible_repunit(41)
    5
    >>> least_divisible_repunit(1234567)
    34020
    """
    if divisor % 5 == 0 or divisor % 2 == 0:
        return 0
    repunit = 1
    repunit_index = 1
    while repunit:
        repunit = (10 * repunit + 1) % divisor
        repunit_index += 1
    return repunit_index


def solution(limit: int = 1000000) -> int:
    """
    返回使 least_divisible_repunit(n) 首次超过 limit 的最小 n 值。
    >>> solution(10)
    17
    >>> solution(100)
    109
    >>> solution(1000)
    1017
    """
    divisor = limit - 1
    if divisor % 2 == 0:
        divisor += 1
    while least_divisible_repunit(divisor) <= limit:
        divisor += 2
    return divisor


if __name__ == "__main__":
    print(f"{solution() = }")
