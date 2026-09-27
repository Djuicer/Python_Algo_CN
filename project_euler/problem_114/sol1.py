"""
Project Euler Problem 114: https://projecteuler.net/problem=114

在一行长度为七个单位的位置上放置最短长度为三个单位的红色方块，并使任意两个红色方块
（允许长度不同）之间至少隔一个灰色方格。这样的放置方式恰好有十七种。

    |g|g|g|g|g|g|g|    |r,r,r|g|g|g|g|

    |g|r,r,r|g|g|g|    |g|g|r,r,r|g|g|

    |g|g|g|r,r,r|g|    |g|g|g|g|r,r,r|

    |r,r,r|g|r,r,r|    |r,r,r,r|g|g|g|

    |g|r,r,r,r|g|g|    |g|g|r,r,r,r|g|

    |g|g|g|r,r,r,r|    |r,r,r,r,r|g|g|

    |g|r,r,r,r,r|g|    |g|g|r,r,r,r,r|

    |r,r,r,r,r,r|g|    |g|r,r,r,r,r,r|

    |r,r,r,r,r,r,r|

长度为五十个单位的一行有多少种填充方式？

注意：虽然上述示例未体现，但通常允许混合不同方块长度。例如，在长度为八个单位的一行中，
可以使用红色 (3)、灰色 (1) 和红色 (4)。
"""


def solution(length: int = 50) -> int:
    """
    返回给定长度的一行的填充方式数。

    >>> solution(7)
    17
    """

    ways_number = [1] * (length + 1)

    for row_length in range(3, length + 1):
        for block_length in range(3, row_length + 1):
            for block_start in range(row_length - block_length):
                ways_number[row_length] += ways_number[
                    row_length - block_start - block_length - 1
                ]

            ways_number[row_length] += 1

    return ways_number[length]


if __name__ == "__main__":
    print(f"{solution() = }")
