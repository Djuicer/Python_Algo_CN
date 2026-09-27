"""
Problem 33: https://projecteuler.net/problem=33

分数 49/98 很特别：缺乏经验的人在约分时，可能误以为约去两个 9 就能得到
49/98 = 4/8，而结果碰巧正确。

我们将 30/50 = 3/5 这样的分数视为平凡示例。

这种值小于一、分子和分母均为两位数的非平凡分数恰好有四个。

将这四个分数的乘积约为最简分数，求其分母。
"""

from __future__ import annotations

from fractions import Fraction


def is_digit_cancelling(num: int, den: int) -> bool:
    return (
        num != den and num % 10 == den // 10 and (num // 10) / (den % 10) == num / den
    )


def fraction_list(digit_len: int) -> list[str]:
    """
    >>> fraction_list(2)
    ['16/64', '19/95', '26/65', '49/98']
    >>> fraction_list(3)
    ['16/64', '19/95', '26/65', '49/98']
    >>> fraction_list(4)
    ['16/64', '19/95', '26/65', '49/98']
    >>> fraction_list(0)
    []
    >>> fraction_list(5)
    ['16/64', '19/95', '26/65', '49/98']
    """
    solutions = []
    den = 11
    last_digit = int("1" + "0" * digit_len)
    for num in range(den, last_digit):
        while den <= 99:
            if (
                (num != den)
                and (num % 10 == den // 10)
                and (den % 10 != 0)
                and is_digit_cancelling(num, den)
            ):
                solutions.append(f"{num}/{den}")
            den += 1
        num += 1
        den = 10
    return solutions


def solution(n: int = 2) -> int:
    """
    返回该问题的解。
    """
    result = 1.0
    for fraction in fraction_list(n):
        frac = Fraction(fraction)
        result *= frac.denominator / frac.numerator
    return int(result)


if __name__ == "__main__":
    print(solution())
