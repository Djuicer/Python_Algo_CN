"""
Project Euler 62
https://projecteuler.net/problem=62

立方数 41063625 (345^3) 的数字可重新排列为另外两个立方数：
56623104 (384^3) 和 66430125 (405^3)。事实上，41063625 是数字排列中恰有三个
也是立方数的最小立方数。

找出数字排列中恰有五个也是立方数的最小立方数。
"""

from collections import defaultdict


def solution(max_base: int = 5) -> int:
    """
    遍历每个可能的立方数，并将其数字按升序排列。排序会保持一种可用于比较排列的
    数字顺序。将每个排序后的数字序列存入字典，键为数字序列，值为立方数底数列表。

    找到 5 个产生相同数字序列的数后，返回其中最小者。由于底数按升序插入，
    最小者位于索引 0。

    >>> solution(2)
    125
    >>> solution(3)
    41063625
    """
    freqs = defaultdict(list)
    num = 0

    while True:
        digits = get_digits(num)
        freqs[digits].append(num)

        if len(freqs[digits]) == max_base:
            base = freqs[digits][0] ** 3
            return base

        num += 1


def get_digits(num: int) -> str:
    """
    计算 num 的立方的排序数字序列。

    >>> get_digits(3)
    '27'
    >>> get_digits(99)
    '027999'
    >>> get_digits(123)
    '0166788'
    """
    return "".join(sorted(str(num**3)))


if __name__ == "__main__":
    print(f"{solution() = }")
