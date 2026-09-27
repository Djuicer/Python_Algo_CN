"""
Project Euler Problem 70: https://projecteuler.net/problem=70

Euler 欧拉函数 φ(n)（有时称为 phi 函数）用于确定小于或等于 n 且与 n 互素的
正整数数量。例如，1, 2, 4, 5, 7 和 8 均小于九且与九互素，因此 φ(9)=6。

数字 1 被认为与每个正整数都互素，因此 φ(1)=1。

有趣的是，φ(87109)=79180，并且可以看出 87109 是 79180 的一个排列。

找出满足 1 < n < 10^7、φ(n) 是 n 的一个排列且比值 n/φ(n) 最小的 n。

-----

这本质上是暴力求解：计算 10^7 以内的所有欧拉函数值，并找出 n/φ(n) 的最小比值。
为了最小化比值，希望尽量减小 n 并增大 φ(n)，因此可存储当前最小分数的分子和分母，
再用每个欧拉函数值构造新分数进行比较。为避免除以零，这里采用交叉相乘。

参考资料：
计算欧拉函数值
https://en.wikipedia.org/wiki/Euler's_totient_function#Euler's_product_formula
"""

from __future__ import annotations

import numpy as np


def get_totients(max_one: int) -> list[int]:
    """
    使用 Euler 乘积公式的定义，计算从 0 到 max_one（不含）的欧拉函数值列表。

    >>> get_totients(5)
    [0, 1, 1, 2, 2]

    >>> get_totients(10)
    [0, 1, 1, 2, 2, 4, 2, 6, 4, 6]
    """
    totients = np.arange(max_one)

    for i in range(2, max_one):
        if totients[i] == i:
            x = np.arange(i, max_one, i)  # 待选择的索引数组
            totients[x] -= totients[x] // i

    return totients.tolist()


def has_same_digits(num1: int, num2: int) -> bool:
    """
    如果 num1 和 num2 中每个数字出现的频次相同，则返回 True，否则返回 False。

    >>> has_same_digits(123456789, 987654321)
    True

    >>> has_same_digits(123, 23)
    False

    >>> has_same_digits(1234566, 123456)
    False
    """
    return sorted(str(num1)) == sorted(str(num2))


def solution(max_n: int = 10000000) -> int:
    """
    在 1 到 max 中找出使 n/φ(n) 最小的 n。

    >>> solution(100)
    21

    >>> solution(10000)
    4435
    """

    min_numerator = 1  # i
    min_denominator = 0  # φ(i)
    totients = get_totients(max_n + 1)

    for i in range(2, max_n + 1):
        t = totients[i]

        if i * min_denominator < min_numerator * t and has_same_digits(i, t):
            min_numerator = i
            min_denominator = t

    return min_numerator


if __name__ == "__main__":
    print(f"{solution() = }")
