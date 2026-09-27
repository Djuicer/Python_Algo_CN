"""
Problem 81: https://projecteuler.net/problem=81
在下面的 5 x 5 矩阵中，只能向右和向下移动时，从左上角到右下角的最小路径和
以红色粗体标出，等于 2427。

    [131]   673   234    103    18
    [201]  [96]  [342]   965   150
     630   803   [746]  [422]  111
     537   699   497    [121]  956
     805   732   524    [37]  [331]

matrix.txt（https://projecteuler.net/project/resources/p081_matrix.txt）是一个包含
80 x 80 矩阵的 31K 文本文件。求其中只能向右和向下移动时，从左上角到右下角的
最小路径和。
"""

import os


def solution(filename: str = "matrix.txt") -> int:
    """
    返回矩阵中从左上角到右下角的最小路径和。
    >>> solution()
    427337
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as in_file:
        data = in_file.read()

    grid = [[int(cell) for cell in row.split(",")] for row in data.strip().splitlines()]
    dp = [[0 for cell in row] for row in grid]
    n = len(grid[0])

    dp = [[0 for i in range(n)] for j in range(n)]
    dp[0][0] = grid[0][0]
    for i in range(1, n):
        dp[0][i] = grid[0][i] + dp[0][i - 1]
    for i in range(1, n):
        dp[i][0] = grid[i][0] + dp[i - 1][0]

    for i in range(1, n):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])

    return dp[-1][-1]


if __name__ == "__main__":
    print(f"{solution() = }")
