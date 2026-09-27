"""
Project Euler Problem 164: https://projecteuler.net/problem=164

连续三个数字之和的限制

有多少个 20 位数 n（没有前导零），其任意三个连续数字之和都不大于 9？

使用缓存中间结果的暴力递归解法。
"""


def solve(
    digit: int, prev1: int, prev2: int, sum_max: int, first: bool, cache: dict[str, int]
) -> int:
    """
    在前一个数字为 'prev1'、前前一个数字为 'prev2'、总和上限为 'sum_max' 时，
    求剩余 'digit' 位数字的解。传递 'cache' 以存储和复用中间结果。

    >>> solve(digit=1, prev1=0, prev2=0, sum_max=9, first=True, cache={})
    9
    >>> solve(digit=1, prev1=0, prev2=0, sum_max=9, first=False, cache={})
    10
    """
    if digit == 0:
        return 1

    cache_str = f"{digit},{prev1},{prev2}"
    if cache_str in cache:
        return cache[cache_str]

    comb = 0
    for curr in range(sum_max - prev1 - prev2 + 1):
        if first and curr == 0:
            continue

        comb += solve(
            digit=digit - 1,
            prev1=curr,
            prev2=prev1,
            sum_max=sum_max,
            first=False,
            cache=cache,
        )

    cache[cache_str] = comb
    return comb


def solution(n_digits: int = 20) -> int:
    """
    求 n_digits 位数对应的问题解。

    >>> solution(2)
    45
    >>> solution(10)
    21838806
    """
    cache: dict[str, int] = {}
    return solve(digit=n_digits, prev1=0, prev2=0, sum_max=9, first=True, cache=cache)


if __name__ == "__main__":
    print(f"{solution(10) = }")
