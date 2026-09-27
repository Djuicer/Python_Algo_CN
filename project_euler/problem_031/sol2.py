"""
Problem 31: https://projecteuler.net/problem=31

硬币求和

英国货币由英镑 f 和便士 p 组成，通常流通八种硬币：

1p, 2p, 5p, 10p, 20p, 50p, f1 (100p) 和 f2 (200p)。
可以按以下方式凑出 f2：

1xf1 + 1x50p + 2x20p + 1x5p + 1x2p + 3x1p
使用任意数量的硬币，有多少种不同方式可以凑出 f2？

提示：
    > 1 英镑等于 100 便士（f1 = 100p）
    > 可用硬币（单位：便士）为：1, 2, 5, 10, 20, 50, 100 和 200。
    > 求这些面值组合成 200 便士的不同方式数。

示例：
    凑出 6p 有 5 种方式
      1,1,1,1,1,1
      1,1,1,1,2
      1,1,2,2
      2,2,2
      1,5
    凑出 5p 有 4 种方式
      1,1,1,1,1
      1,1,1,2
      1,2,2
      5
"""


def solution(pence: int = 200) -> int:
    """返回使用任意数量的硬币凑出 X 便士的不同方式数。
    本解法采用自底向上的动态规划（Dynamic Programming）。

    >>> solution(500)
    6295434
    >>> solution(200)
    73682
    >>> solution(50)
    451
    >>> solution(10)
    11
    """
    coins = [1, 2, 5, 10, 20, 50, 100, 200]
    number_of_ways = [0] * (pence + 1)
    number_of_ways[0] = 1  # 基本情况：凑出 0 便士有 1 种方式

    for coin in coins:
        for i in range(coin, pence + 1, 1):
            number_of_ways[i] += number_of_ways[i - coin]
    return number_of_ways[pence]


if __name__ == "__main__":
    assert solution(200) == 73682
