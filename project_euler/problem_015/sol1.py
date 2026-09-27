"""
Problem 15: https://projecteuler.net/problem=15

从 2x2 网格的左上角出发，并且只能向右和向下移动，到达右下角恰好有 6 条路径。
在 20x20 网格中有多少条这样的路径？
"""

from math import factorial


def solution(n: int = 20) -> int:
    """
    返回在 n x n 网格中从左上角出发、只能向右和向下移动到右下角的路径数。
    >>> solution(25)
    126410606437752
    >>> solution(23)
    8233430727600
    >>> solution(20)
    137846528820
    >>> solution(15)
    155117520
    >>> solution(1)
    2
    """
    n = 2 * n  # 从第 3 行开始，奇数行的中间项是 n = 1,
    # 2, 3,... 时的解
    k = n // 2

    return int(factorial(n) / (factorial(k) * factorial(n - k)))


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print(solution(20))
    else:
        try:
            n = int(sys.argv[1])
            print(solution(n))
        except ValueError:
            print("Invalid entry - please enter a number.")
