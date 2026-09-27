from maths.greatest_common_divisor import greatest_common_divisor

"""
Project Euler Problem 5: https://projecteuler.net/problem=5

最小倍数

2520 是能被 1 到 10 中每个数整除且没有余数的最小数。

能被 1 到 20 中所有数整除的最小正数是多少？

参考资料：
    - https://en.wiktionary.org/wiki/evenly_divisible
    - https://en.wikipedia.org/wiki/Euclidean_algorithm
    - https://en.wikipedia.org/wiki/Least_common_multiple
"""


def lcm(x: int, y: int) -> int:
    """
    最小公倍数。

    使用性质 lcm(a, b) * greatest_common_divisor(a, b) = a*b

    >>> lcm(3, 15)
    15
    >>> lcm(1, 27)
    27
    >>> lcm(13, 27)
    351
    >>> lcm(64, 48)
    192
    """

    return (x * y) // greatest_common_divisor(x, y)


def solution(n: int = 20) -> int:
    """
    返回能被 1 到 n 中所有数整除（无余数）的最小正数。

    >>> solution(10)
    2520
    >>> solution(15)
    360360
    >>> solution(22)
    232792560
    """

    g = 1
    for i in range(1, n + 1):
        g = lcm(g, i)
    return g


if __name__ == "__main__":
    print(f"{solution() = }")
