"""
Project Euler Problem 1: https://projecteuler.net/problem=1

3 和 5 的倍数

列出所有小于 10 且是 3 或 5 的倍数的自然数，可得 3、5、6 和 9。
这些倍数之和为 23。

求所有小于 1000 且是 3 或 5 的倍数的数之和。
"""


def solution(n: int = 1000) -> int:
    """
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

    xmulti = []
    zmulti = []
    z = 3
    x = 5
    temp = 1
    while True:
        result = z * temp
        if result < n:
            zmulti.append(result)
            temp += 1
        else:
            temp = 1
            break
    while True:
        result = x * temp
        if result < n:
            xmulti.append(result)
            temp += 1
        else:
            break
    collection = list(set(xmulti + zmulti))
    return sum(collection)


if __name__ == "__main__":
    print(f"{solution() = }")
