"""
Problem 16: https://projecteuler.net/problem=16

2^15 = 32768，其各位数字之和为 3 + 2 + 7 + 6 + 8 = 26。

数 2^1000 的各位数字之和是多少？
"""


def solution(power: int = 1000) -> int:
    """返回数 2^power 的各位数字之和。

    >>> solution(1000)
    1366
    >>> solution(50)
    76
    >>> solution(20)
    31
    >>> solution(15)
    26
    """
    n = 2**power
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r


if __name__ == "__main__":
    print(solution(int(str(input()).strip())))
