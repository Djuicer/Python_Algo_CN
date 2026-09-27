"""
Problem 45: https://projecteuler.net/problem=45

三角数、五边形数和六边形数分别由以下公式生成：
Triangle	 	T(n) = (n * (n + 1)) / 2	 	1, 3, 6, 10, 15, ...
Pentagonal	 	P(n) = (n * (3 * n - 1)) / 2	 	1, 5, 12, 22, 35, ...
Hexagonal	 	H(n) = n * (2 * n - 1)	 	1, 6, 15, 28, 45, ...
可以验证 T(285) = P(165) = H(143) = 40755。

求下一个同时为五边形数和六边形数的三角数。
所有三角数都是六边形数。
T(2n-1) = n * (2 * n - 1) = H(n)
因此只需检查同时也是五边形数的六边形数。
"""


def hexagonal_num(n: int) -> int:
    """
    返回第 n 个六边形数。
    >>> hexagonal_num(143)
    40755
    >>> hexagonal_num(21)
    861
    >>> hexagonal_num(10)
    190
    """
    return n * (2 * n - 1)


def is_pentagonal(n: int) -> bool:
    """
    如果 n 是五边形数则返回 True，否则返回 False。
    >>> is_pentagonal(330)
    True
    >>> is_pentagonal(7683)
    False
    >>> is_pentagonal(2380)
    True
    """
    root = (1 + 24 * n) ** 0.5
    return ((1 + root) / 6) % 1 == 0


def solution(start: int = 144) -> int:
    """
    返回下一个同时为三角数、五边形数和六边形数的数。
    >>> solution(144)
    1533776805
    """
    n = start
    num = hexagonal_num(n)
    while not is_pentagonal(num):
        n += 1
        num = hexagonal_num(n)
    return num


if __name__ == "__main__":
    print(f"{solution()} = ")
