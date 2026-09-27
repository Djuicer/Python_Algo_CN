"""
Project Euler Problem 113: https://projecteuler.net/problem=113

从左到右观察，如果任一数字都不大于其左侧数字，则称为递增数；例如 134468。

类似地，如果任一数字都不大于其右侧数字，则称为递减数；例如 66420。

既非递增也非递减的正整数称为“弹跳数”；例如 155349。

随着 n 增大，n 以下弹跳数的比例也随之增加；一百万以下只有 12951 个非弹跳数，
10^10 以下只有 277032 个非弹跳数。

古戈尔（10^100）以下有多少个数不是弹跳数？
"""


def choose(n: int, r: int) -> int:
    """
    使用乘法公式计算二项式系数 c(n,r)。
    >>> choose(4,2)
    6
    >>> choose(5,3)
    10
    >>> choose(20,6)
    38760
    """
    ret = 1.0
    for i in range(1, r + 1):
        ret *= (n + 1 - i) / i
    return round(ret)


def non_bouncy_exact(n: int) -> int:
    """
    计算最多 n 位的非弹跳数数量。
    >>> non_bouncy_exact(1)
    9
    >>> non_bouncy_exact(6)
    7998
    >>> non_bouncy_exact(10)
    136126
    """
    return choose(8 + n, n) + choose(9 + n, n) - 10


def non_bouncy_upto(n: int) -> int:
    """
    计算最多 n 位的非弹跳数数量。
    >>> non_bouncy_upto(1)
    9
    >>> non_bouncy_upto(6)
    12951
    >>> non_bouncy_upto(10)
    277032
    """
    return sum(non_bouncy_exact(i) for i in range(1, n + 1))


def solution(num_digits: int = 100) -> int:
    """
    计算小于一个古戈尔的非弹跳数数量。
    >>> solution(6)
    12951
    >>> solution(10)
    277032
    """
    return non_bouncy_upto(num_digits)


if __name__ == "__main__":
    print(f"{solution() = }")
