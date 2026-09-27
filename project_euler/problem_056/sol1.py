"""
Project Euler Problem 56: https://projecteuler.net/problem=56

古戈尔（10^100）是一个巨大的数：1 后面跟着一百个零；
100^100 大得几乎难以想象：1 后面跟着两百个零。
尽管它们很大，但各自的各位数字之和都只有 1。

考虑形如 ab 的自然数，其中 a, b < 100，其最大的各位数字之和是多少？
"""


def solution(a: int = 100, b: int = 100) -> int:
    """
    考虑形如 a**b 的自然数，其中 a, b < 100，求最大的各位数字之和。
    :param a:
    :param b:
    :return:
    >>> solution(10,10)
    45

    >>> solution(100,100)
    972

    >>> solution(100,200)
    1872
    """

    # 将 BASE 的 POWER 次幂转为 STR，再将其中各项转为 INT 并求和，最后返回这些和的最大值
    return max(
        sum(int(x) for x in str(base**power)) for base in range(a) for power in range(b)
    )


# 测试
if __name__ == "__main__":
    import doctest

    doctest.testmod()
