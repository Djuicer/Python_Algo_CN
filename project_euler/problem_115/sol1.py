"""
Project Euler Problem 115: https://projecteuler.net/problem=115

注意：这是问题 114 的更难版本
(https://projecteuler.net/problem=114).

在一行长度为 n 个单位的位置上放置最短长度为 m 个单位的红色方块，并使任意两个红色方块
（允许长度不同）之间至少隔一个黑色方格。

令填充计数函数 F(m, n) 表示一行的填充方式数。

例如，F(3, 29) = 673135 且 F(3, 30) = 1089155。

也就是说，当 m = 3 时，n = 30 是使填充计数函数首次超过一百万的最小值。

同理，当 m = 10 时，可以验证 F(10, 56) = 880711 且 F(10, 57) = 1148904，
所以 n = 57 是使填充计数函数首次超过一百万的最小值。

当 m = 50 时，求使填充计数函数首次超过一百万的最小 n 值。
"""

from itertools import count


def solution(min_block_length: int = 50) -> int:
    """
    对给定的最小方块长度，返回使填充计数函数首次超过一百万的最小 n 值。

    >>> solution(3)
    30

    >>> solution(10)
    57
    """

    fill_count_functions = [1] * min_block_length

    for n in count(min_block_length):
        fill_count_functions.append(1)

        for block_length in range(min_block_length, n + 1):
            for block_start in range(n - block_length):
                fill_count_functions[n] += fill_count_functions[
                    n - block_start - block_length - 1
                ]

            fill_count_functions[n] += 1

        if fill_count_functions[n] > 1_000_000:
            break

    return n


if __name__ == "__main__":
    print(f"{solution() = }")
