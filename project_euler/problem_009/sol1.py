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
      1. a < b < c
      2. a**2 + b**2 = c**2
      3. a + b + c = 1000

    >>> solution()
    31875000
    """

    for a in range(300):
        for b in range(a + 1, 400):
            for c in range(b + 1, 500):
                if (a + b + c) == 1000 and (a**2) + (b**2) == (c**2):
                    return a * b * c

    return -1


def solution_fast() -> int:
    """
    返回满足以下条件的勾股数 a、b、c 的乘积：
      1. a < b < c
      2. a**2 + b**2 = c**2
      3. a + b + c = 1000

    >>> solution_fast()
    31875000
    """

    for a in range(300):
        for b in range(400):
            c = 1000 - a - b
            if a < b < c and (a**2) + (b**2) == (c**2):
                return a * b * c

    return -1


def benchmark() -> None:
    """
    对两个不同版本的函数进行基准测试。
    """
    import timeit

    print(
        timeit.timeit("solution()", setup="from __main__ import solution", number=1000)
    )
    print(
        timeit.timeit(
            "solution_fast()", setup="from __main__ import solution_fast", number=1000
        )
    )


if __name__ == "__main__":
    print(f"{solution() = }")
