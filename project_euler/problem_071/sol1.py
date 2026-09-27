"""
有序分数
Problem 71
https://projecteuler.net/problem=71

考虑分数 n/d，其中 n 和 d 为正整数。如果 n<d 且 HCF(n,d)=1，
则称其为最简真分数。

如果按大小升序列出 d ≤ 8 的最简真分数集合，可得：
    1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7,
    1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

可以看出，2/5 是紧邻 3/7 左侧的分数。

将 d ≤ 1,000,000 的最简真分数集合按大小升序排列，找出紧邻 3/7 左侧分数的分子。
"""


def solution(numerator: int = 3, denominator: int = 7, limit: int = 1000000) -> int:
    """
    从最简真分数列表中，返回紧邻给定分数（numerator/denominator）左侧分数的分子。
    >>> solution()
    428570
    >>> solution(3, 7, 8)
    2
    >>> solution(6, 7, 60)
    47
    """
    max_numerator = 0
    max_denominator = 1

    for current_denominator in range(1, limit + 1):
        current_numerator = current_denominator * numerator // denominator
        if current_denominator % denominator == 0:
            current_numerator -= 1
        if current_numerator * max_denominator > current_denominator * max_numerator:
            max_numerator = current_numerator
            max_denominator = current_denominator
    return max_numerator


if __name__ == "__main__":
    print(solution(numerator=3, denominator=7, limit=1000000))
