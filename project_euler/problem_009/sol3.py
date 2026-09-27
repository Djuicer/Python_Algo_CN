"""
Project Euler Problem 9: https://projecteuler.net/problem=9

特殊勾股数

勾股数是满足 a < b < c 的三个自然数 a、b、c，且：

    a^2 + b^2 = c^2

例如，3^2 + 4^2 = 9 + 16 = 25 = 5^2。

恰有一组勾股数满足 a + b + c = 1000。求乘积 a*b*c。

参考资料：
    - https://en.wikipedia.org/wiki/Pythagorean_triple
"""


def solution() -> int:
    """
    返回满足以下条件的勾股数 a、b、c 的乘积：
      1. a**2 + b**2 = c**2
      2. a + b + c = 1000

    >>> solution()
    31875000
    """

    return next(
        iter(
            [
                a * b * (1000 - a - b)
                for a in range(1, 999)
                for b in range(a, 999)
                if (a * a + b * b == (1000 - a - b) ** 2)
            ]
        )
    )


if __name__ == "__main__":
    print(f"{solution() = }")
