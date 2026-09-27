"""
Project Euler Problem 117: https://projecteuler.net/problem=117

组合使用灰色方砖与以下长方形砖：红色砖（长度两个单位）、绿色砖（长度三个单位）
和蓝色砖（长度四个单位），恰好有十五种方式可以铺满长度为五个单位的一行。

    |grey|grey|grey|grey|grey|       |red,red|grey|grey|grey|

    |grey|red,red|grey|grey|         |grey|grey|red,red|grey|

    |grey|grey|grey|red,red|         |red,red|red,red|grey|

    |red,red|grey|red,red|           |grey|red,red|red,red|

    |green,green,green|grey|grey|    |grey|green,green,green|grey|

    |grey|grey|green,green,green|    |red,red|green,green,green|

    |green,green,green|red,red|      |blue,blue,blue,blue|grey|

    |grey|blue,blue,blue,blue|

长度为五十个单位的一行有多少种铺法？

注意：本题与问题 116（https://projecteuler.net/problem=116）相关。
"""


def solution(length: int = 50) -> int:
    """
    返回铺满给定长度一行的方式数。

    >>> solution(5)
    15
    """

    ways_number = [1] * (length + 1)

    for row_length in range(length + 1):
        for tile_length in range(2, 5):
            for tile_start in range(row_length - tile_length + 1):
                ways_number[row_length] += ways_number[
                    row_length - tile_start - tile_length
                ]

    return ways_number[length]


if __name__ == "__main__":
    print(f"{solution() = }")
