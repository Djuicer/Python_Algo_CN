"""
Project Euler Problem 116: https://projecteuler.net/problem=116

一行五块灰色方砖中的若干块，将由彩色长方形砖替换；可选红色（长度二）、
绿色（长度三）或蓝色（长度四）。

如果选择红色砖，恰好有七种方式。

    |red,red|grey|grey|grey|    |grey|red,red|grey|grey|

    |grey|grey|red,red|grey|    |grey|grey|grey|red,red|

    |red,red|red,red|grey|      |red,red|grey|red,red|

    |grey|red,red|red,red|

如果选择绿色砖，有三种方式。

    |green,green,green|grey|grey|    |grey|green,green,green|grey|

    |grey|grey|green,green,green|

如果选择蓝色砖，有两种方式。

    |blue,blue,blue,blue|grey|    |grey|blue,blue,blue,blue|

假设颜色不能混用，替换长度为五个单位的一行灰砖共有 7 + 3 + 2 = 12 种方式。

如果颜色不能混用且必须至少使用一块彩色砖，长度为五十个单位的一行灰砖有多少种
不同的替换方式？

注意：本题与问题 117（https://projecteuler.net/problem=117）相关。
"""


def solution(length: int = 50) -> int:
    """
    返回在颜色不能混用且至少使用一块彩色砖时，替换给定长度一行灰砖的不同方式数。

    >>> solution(5)
    12
    """

    different_colour_ways_number = [[0] * 3 for _ in range(length + 1)]

    for row_length in range(length + 1):
        for tile_length in range(2, 5):
            for tile_start in range(row_length - tile_length + 1):
                different_colour_ways_number[row_length][tile_length - 2] += (
                    different_colour_ways_number[row_length - tile_start - tile_length][
                        tile_length - 2
                    ]
                    + 1
                )

    return sum(different_colour_ways_number[length])


if __name__ == "__main__":
    print(f"{solution() = }")
