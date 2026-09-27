"""
Problem 15: https://projecteuler.net/problem=15

从 2x2 网格的左上角出发，并且只能向右和向下移动，到达右下角恰好有 6 条路径。
在 20x20 网格中有多少条这样的路径？
"""


def solution(n: int = 20) -> int:
    """
    使用动态规划（Dynamic Programming）显式统计路径数。

    >>> solution(6)
    924
    >>> solution(2)
    6
    >>> solution(1)
    2
    """

    counts = [[1 for _ in range(n + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            counts[i][j] = counts[i - 1][j] + counts[i][j - 1]

    return counts[n][n]


if __name__ == "__main__":
    print(solution())
