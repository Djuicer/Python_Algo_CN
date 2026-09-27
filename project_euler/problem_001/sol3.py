"""
Project Euler Problem 1: https://projecteuler.net/problem=1

3 和 5 的倍数

列出所有小于 10 且是 3 或 5 的倍数的自然数，可得 3、5、6 和 9。
这些倍数之和为 23。

求所有小于 1000 且是 3 或 5 的倍数的数之和。
"""


def solution(n: int = 1000) -> int:
    """
    本解法基于数列相邻项遵循的模式：0+3,+2,+1,+3,+1,+2,+3。
    返回所有小于 n 且是 3 或 5 的倍数的数之和。

    >>> solution(3)
    0
    >>> solution(4)
    3
    >>> solution(10)
    23
    >>> solution(600)
    83700
    """

    total = 0
    num = 0
    while 1:
        num += 3
        if num >= n:
            break
        total += num
        num += 2
        if num >= n:
            break
        total += num
        num += 1
        if num >= n:
            break
        total += num
        num += 3
        if num >= n:
            break
        total += num
        num += 1
        if num >= n:
            break
        total += num
        num += 2
        if num >= n:
            break
        total += num
        num += 3
        if num >= n:
            break
        total += num
    return total


if __name__ == "__main__":
    print(f"{solution() = }")
