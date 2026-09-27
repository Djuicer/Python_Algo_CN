"""
Problem 14: https://projecteuler.net/problem=14

Collatz 猜想：从任意正整数 n 开始，下一项按如下方式由前一项得到：

如果前一项为偶数，下一项是前一项的一半。
如果前一项为奇数，下一项是前一项的 3 倍加 1。
该猜想认为，无论起始 n 为何，数列最终总会到达 1。

题目说明：
在正整数集合上定义如下迭代数列：

    n → n/2 (n is even)
    n → 3n + 1 (n is odd)

从 13 开始应用上述规则，可生成以下数列：

    13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1

可以看出，这个从 13 开始并以 1 结束的数列包含 10 项。尽管这一结论尚未得到
证明（Collatz 问题），但人们认为所有起始数最终都会到达 1。

在一百万以下，哪个起始数会产生最长的链？
"""

from __future__ import annotations

COLLATZ_SEQUENCE_LENGTHS = {1: 1}


def collatz_sequence_length(n: int) -> int:
    """返回 n 的 Collatz 数列长度。"""
    if n in COLLATZ_SEQUENCE_LENGTHS:
        return COLLATZ_SEQUENCE_LENGTHS[n]
    next_n = n // 2 if n % 2 == 0 else 3 * n + 1
    sequence_length = collatz_sequence_length(next_n) + 1
    COLLATZ_SEQUENCE_LENGTHS[n] = sequence_length
    return sequence_length


def solution(n: int = 1000000) -> int:
    """返回小于 n 且生成最长 Collatz 数列的数。

    >>> solution(1000000)
    837799
    >>> solution(200)
    171
    >>> solution(5000)
    3711
    >>> solution(15000)
    13255
    """

    result = max((collatz_sequence_length(i), i) for i in range(1, n))
    return result[1]


if __name__ == "__main__":
    print(solution(int(input().strip())))
