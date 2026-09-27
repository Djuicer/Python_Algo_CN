"""
Problem 44: https://projecteuler.net/problem=44

五边形数由公式 Pn=n(3n-1)/2 生成。前十个五边形数为：
1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...
可以看出 P4 + P7 = 22 + 70 = 92 = P8，但它们的差 70 - 22 = 48 不是五边形数。

找出一对五边形数 Pj 和 Pk，使其和与差都是五边形数，并使 D = |Pk - Pj|
最小；D 的值是多少？
"""


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


def solution(limit: int = 5000) -> int:
    """
    返回两个五边形数 P1 和 P2 的最小差值，其中 P1 + P2 与 P2 - P1 均为五边形数。
    >>> solution(5000)
    5482660
    """
    pentagonal_nums = [(i * (3 * i - 1)) // 2 for i in range(1, limit)]
    for i, pentagonal_i in enumerate(pentagonal_nums):
        for j in range(i, len(pentagonal_nums)):
            pentagonal_j = pentagonal_nums[j]
            a = pentagonal_i + pentagonal_j
            b = pentagonal_j - pentagonal_i
            if is_pentagonal(a) and is_pentagonal(b):
                return b

    return -1


if __name__ == "__main__":
    print(f"{solution() = }")
