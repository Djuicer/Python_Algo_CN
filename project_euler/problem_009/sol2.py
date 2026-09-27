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


def solution(n: int = 1000) -> int:
    """
    返回满足以下条件的勾股数 a、b、c 的乘积：
      1. a < b < c
      2. a**2 + b**2 = c**2
      3. a + b + c = n

    >>> solution(36)
    1620
    >>> solution(126)
    66780
    """

    product = -1
    candidate = 0
    for a in range(1, n // 3):
        # 联立方程 a**2+b**2=c**2 和 a+b+c=N，消去 c
        b = (n * n - 2 * a * n) // (2 * n - 2 * a)
        c = n - a - b
        if c * c == (a * a + b * b):
            candidate = a * b * c
            product = max(product, candidate)
    return product


if __name__ == "__main__":
    print(f"{solution() = }")
