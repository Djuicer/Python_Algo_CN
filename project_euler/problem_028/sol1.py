"""
Problem 28
Url: https://projecteuler.net/problem=28
题目说明：
从数字 1 开始向右并按顺时针方向移动，可形成如下 5 x 5 螺旋：

    21 22 23 24 25
    20  7  8  9 10
    19  6  1  2 11
    18  5  4  3 12
    17 16 15 14 13

可以验证，对角线上的数字之和为 101。

以相同方式形成的 1001 x 1001 螺旋中，对角线上的数字之和是多少？
"""

from math import ceil


def solution(n: int = 1001) -> int:
    """返回以相同方式形成的 n x n 螺旋中对角线上的数字之和。

    >>> solution(1001)
    669171001
    >>> solution(500)
    82959497
    >>> solution(100)
    651897
    >>> solution(50)
    79697
    >>> solution(10)
    537
    """
    total = 1

    for i in range(1, ceil(n / 2.0)):
        odd = 2 * i + 1
        even = 2 * i
        total = total + 4 * odd**2 - 6 * even

    return total


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print(solution())
    else:
        try:
            n = int(sys.argv[1])
            print(solution(n))
        except ValueError:
            print("Invalid entry - please enter a number")
