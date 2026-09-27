"""
Project Euler Problem 38: https://projecteuler.net/problem=38

取数字 192，分别乘以 1, 2 和 3：

192 x 1 = 192
192 x 2 = 384
192 x 3 = 576

将各个乘积连接起来，得到 1 到 9 的全数字数 192384576。我们称 192384576 为
192 与 (1,2,3) 的连接乘积。

同样，从 9 开始分别乘以 1, 2, 3, 4 和 5，可得到全数字数 918273645，
它是 9 与 (1,2,3,4,5) 的连接乘积。

一个整数与 (1,2, ... , n)（其中 n > 1）的连接乘积所能形成的最大 1 到 9
全数字 9 位数是多少？

解法：
由于 n>1，最大的候选解将由一个 4 位数及其两倍（一个 5 位数）连接而成。
设 a 为该 4 位数。
a  has 4 digits  =>  1000 <=  a  < 10000
2a has 5 digits  => 10000 <= 2a  < 100000
=>  5000 <= a < 10000

将 a 与 2a 连接得 a * 10^5 + 2a，因此给定 a 的候选值为 100002 * a。
按逆序遍历搜索空间 5000 <= a < 10000，计算每个 a 的候选值并检查其是否为
1-9 全数字数。

如果不存在满足该性质的 4 位数，则用类似公式检查 3 位数
（示例 a=192 给出了 a 位数的下界）：
a 有 3 位，依此类推……
=>  100 <= a < 334, candidate = a * 10^6 + 2a * 10^3 + 3a
                              = 1002003 * a
"""

from __future__ import annotations


def is_9_pandigital(n: int) -> bool:
    """
    检查 n 是否为 1 到 9 的全数字 9 位数。
    >>> is_9_pandigital(12345)
    False
    >>> is_9_pandigital(156284973)
    True
    >>> is_9_pandigital(1562849733)
    False
    """
    s = str(n)
    return len(s) == 9 and set(s) == set("123456789")


def solution() -> int | None:
    """
    返回一个整数与 (1,2,...,n)（其中 n > 1）的连接乘积所能形成的最大 1 到 9
    全数字 9 位数。
    """
    for base_num in range(9999, 4999, -1):
        candidate = 100002 * base_num
        if is_9_pandigital(candidate):
            return candidate

    for base_num in range(333, 99, -1):
        candidate = 1002003 * base_num
        if is_9_pandigital(candidate):
            return candidate

    return None


if __name__ == "__main__":
    print(f"{solution() = }")
