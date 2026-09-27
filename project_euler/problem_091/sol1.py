"""
Project Euler Problem 91: https://projecteuler.net/problem=91

点 P (x1, y1) 和 Q (x2, y2) 位于整数坐标上，并与原点 O(0,0) 相连形成 ΔOPQ。
￼
当每个坐标都在 0 到 2（含）之间时，恰好可以形成十四个含直角的三角形；即
0 ≤ x1, y1, x2, y2 ≤ 2.
￼
给定 0 ≤ x1, y1, x2, y2 ≤ 50，可以形成多少个直角三角形？
"""

from itertools import combinations, product


def is_right(x1: int, y1: int, x2: int, y2: int) -> bool:
    """
    检查由 P(x1,y1)、Q(x2,y2) 和 O(0,0) 描述的三角形是否为直角三角形。
    注意：此处不检查 P 与 Q 是否相等，该情况由 solution 函数中的
    itertools.combinations 处理。

    >>> is_right(0, 1, 2, 0)
    True
    >>> is_right(1, 0, 2, 2)
    False
    """
    if x1 == y1 == 0 or x2 == y2 == 0:
        return False
    a_square = x1 * x1 + y1 * y1
    b_square = x2 * x2 + y2 * y2
    c_square = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
    return (
        a_square + b_square == c_square
        or a_square + c_square == b_square
        or b_square + c_square == a_square
    )


def solution(limit: int = 50) -> int:
    """
    返回由两点 P、Q 形成的直角三角形 OPQ 数量，其中两点的 x、y 坐标均在
    0 到 limit（含）之间。

    >>> solution(2)
    14
    >>> solution(10)
    448
    """
    return sum(
        1
        for pt1, pt2 in combinations(product(range(limit + 1), repeat=2), 2)
        if is_right(*pt1, *pt2)
    )


if __name__ == "__main__":
    print(f"{solution() = }")
