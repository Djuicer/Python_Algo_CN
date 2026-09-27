"""
Project Euler Problem 137: https://projecteuler.net/problem=137

斐波那契黄金块

该多项式数列可改写为有限形式：

A_F(x) = x / (1 - x - x^2)

接下来需要求出使 A_F(x) 为正整数的有理数 x。事实证明，第 n 个黄金块由
F(2n) * F(2n + 1) 给出，其中 F(k) 是第 k 个斐波那契数。

Reference: https://oeis.org/A081018

"""


def solution(n: int = 15) -> int:
    """
    计算第 2n 和 2n+1 个斐波那契数，并返回其乘积。

    >>> solution(3)
    104
    >>> solution(10)
    74049690
    """

    k = 2 * n

    fib1 = fib2 = 1
    for _ in range(k - 1):
        fib1, fib2 = fib2, fib1 + fib2

    return fib1 * fib2


if __name__ == "__main__":
    print(f"{solution() = }")
