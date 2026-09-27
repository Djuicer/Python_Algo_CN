"""
Project Euler Problem 234: https://projecteuler.net/problem=234

对于任意整数 n，考虑以下三个函数

f1,n(x,y,z) = x^(n+1) + y^(n+1) - z^(n+1)
f2,n(x,y,z) = (xy + yz + zx)*(x^(n-1) + y^(n-1) - z^(n-1))
f3,n(x,y,z) = xyz*(xn-2 + yn-2 - zn-2)

以及它们的组合

fn(x,y,z) = f1,n(x,y,z) + f2,n(x,y,z) - f3,n(x,y,z)

若 x、y 和 z 均为形如 a / b 的有理数，满足 0 < a < b ≤ k，且至少存在一个
整数 n 使 fn(x,y,z) = 0，则称 (x,y,z) 为 k 阶黄金三元组。

令 s(x,y,z) = x + y + z。
令 t = u / v 为所有 35 阶黄金三元组 (x,y,z) 对应的不同 s(x,y,z) 之和。
所有 s(x,y,z) 和 t 均须为最简形式。

求 u + v。


解法：

展开括号容易证明
fn(x, y, z) = (x + y + z) * (x^n + y^n - z^n).

由于 x,y,z 均为正数，当且仅当 x^n + y^n = z^n 时，条件 fn(x, y, z) = 0 成立。

根据 Fermat 最后定理，这意味着 n 的绝对值不能超过 2，即 n 属于 {-2, -1, 0, 1, 2}。
可以排除 n = 0，因为此时方程化为 1 + 1 = 1，不存在解。

因此只需遍历 x 和 y 的所有可能分子与分母，计算对应的 z，并检查相应分子和分母
是否为整数且满足 0 < z_num < z_den <= 0。使用集合 "uniquq_s" 确保没有重复项，
并使用 fractions.Fraction 类确保得到正确的分子和分母。

Reference:
https://en.wikipedia.org/wiki/Fermat%27s_Last_Theorem
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd, sqrt


def is_sq(number: int) -> bool:
    """
    检查 number 是否为完全平方数。

    >>> is_sq(1)
    True
    >>> is_sq(1000001)
    False
    >>> is_sq(1000000)
    True
    """
    sq: int = int(number**0.5)
    return number == sq * sq


def add_three(
    x_num: int, x_den: int, y_num: int, y_den: int, z_num: int, z_den: int
) -> tuple[int, int]:
    """
    给定三个分数的分子和分母，返回其和的最简分子与分母。
    >>> add_three(1, 3, 1, 3, 1, 3)
    (1, 1)
    >>> add_three(2, 5, 4, 11, 12, 3)
    (262, 55)
    """
    top: int = x_num * y_den * z_den + y_num * x_den * z_den + z_num * x_den * y_den
    bottom: int = x_den * y_den * z_den
    hcf: int = gcd(top, bottom)
    top //= hcf
    bottom //= hcf
    return top, bottom


def solution(order: int = 35) -> int:
    """
    对给定阶数的所有黄金三元组 (x,y,z)，求全部 s(x,y,z) 之和的分子与分母之和。

    >>> solution(5)
    296
    >>> solution(10)
    12519
    >>> solution(20)
    19408891927
    """
    unique_s: set = set()
    hcf: int
    total: Fraction = Fraction(0)
    fraction_sum: tuple[int, int]

    for x_num in range(1, order + 1):
        for x_den in range(x_num + 1, order + 1):
            for y_num in range(1, order + 1):
                for y_den in range(y_num + 1, order + 1):
                    # n=1
                    z_num = x_num * y_den + x_den * y_num
                    z_den = x_den * y_den
                    hcf = gcd(z_num, z_den)
                    z_num //= hcf
                    z_den //= hcf
                    if 0 < z_num < z_den <= order:
                        fraction_sum = add_three(
                            x_num, x_den, y_num, y_den, z_num, z_den
                        )
                        unique_s.add(fraction_sum)

                    # n=2
                    z_num = (
                        x_num * x_num * y_den * y_den + x_den * x_den * y_num * y_num
                    )
                    z_den = x_den * x_den * y_den * y_den
                    if is_sq(z_num) and is_sq(z_den):
                        z_num = int(sqrt(z_num))
                        z_den = int(sqrt(z_den))
                        hcf = gcd(z_num, z_den)
                        z_num //= hcf
                        z_den //= hcf
                        if 0 < z_num < z_den <= order:
                            fraction_sum = add_three(
                                x_num, x_den, y_num, y_den, z_num, z_den
                            )
                            unique_s.add(fraction_sum)

                    # n=-1
                    z_num = x_num * y_num
                    z_den = x_den * y_num + x_num * y_den
                    hcf = gcd(z_num, z_den)
                    z_num //= hcf
                    z_den //= hcf
                    if 0 < z_num < z_den <= order:
                        fraction_sum = add_three(
                            x_num, x_den, y_num, y_den, z_num, z_den
                        )
                        unique_s.add(fraction_sum)

                    # n=2
                    z_num = x_num * x_num * y_num * y_num
                    z_den = (
                        x_den * x_den * y_num * y_num + x_num * x_num * y_den * y_den
                    )
                    if is_sq(z_num) and is_sq(z_den):
                        z_num = int(sqrt(z_num))
                        z_den = int(sqrt(z_den))
                        hcf = gcd(z_num, z_den)
                        z_num //= hcf
                        z_den //= hcf
                        if 0 < z_num < z_den <= order:
                            fraction_sum = add_three(
                                x_num, x_den, y_num, y_den, z_num, z_den
                            )
                            unique_s.add(fraction_sum)

    for num, den in unique_s:
        total += Fraction(num, den)

    return total.denominator + total.numerator


if __name__ == "__main__":
    print(f"{solution() = }")
