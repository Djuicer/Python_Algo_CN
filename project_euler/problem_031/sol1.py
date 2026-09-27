"""
硬币求和
Problem 31: https://projecteuler.net/problem=31

英国货币由英镑 f 和便士 p 组成，通常流通八种硬币：

1p, 2p, 5p, 10p, 20p, 50p, f1 (100p) and f2 (200p).
可以按以下方式凑出 f2：

1xf1 + 1x50p + 2x20p + 1x5p + 1x2p + 3x1p
使用任意数量的硬币，有多少种不同方式可以凑出 f2？
"""


def one_pence() -> int:
    return 1


def two_pence(x: int) -> int:
    return 0 if x < 0 else two_pence(x - 2) + one_pence()


def five_pence(x: int) -> int:
    return 0 if x < 0 else five_pence(x - 5) + two_pence(x)


def ten_pence(x: int) -> int:
    return 0 if x < 0 else ten_pence(x - 10) + five_pence(x)


def twenty_pence(x: int) -> int:
    return 0 if x < 0 else twenty_pence(x - 20) + ten_pence(x)


def fifty_pence(x: int) -> int:
    return 0 if x < 0 else fifty_pence(x - 50) + twenty_pence(x)


def one_pound(x: int) -> int:
    return 0 if x < 0 else one_pound(x - 100) + fifty_pence(x)


def two_pound(x: int) -> int:
    return 0 if x < 0 else two_pound(x - 200) + one_pound(x)


def solution(n: int = 200) -> int:
    """返回使用任意数量的硬币凑出 n 便士的不同方式数。

    >>> solution(500)
    6295434
    >>> solution(200)
    73682
    >>> solution(50)
    451
    >>> solution(10)
    11
    """
    return two_pound(n)


if __name__ == "__main__":
    print(solution(int(input().strip())))
