"""
Project Euler Problem 174: https://projecteuler.net/problem=174

将方形薄片定义为带有方形“孔洞”的正方形边框，使其具有水平和垂直对称性。

使用八块方砖只能以一种方式形成薄片：一个中心带有 1x1 孔洞的 3x3 正方形。
而使用三十二块方砖可以形成两种不同的薄片。

若 t 表示使用的方砖数，则称 t = 8 属于 L(1) 型，t = 32 属于 L(2) 型。

令 N(n) 表示满足 t ≤ 1000000 且 t 属于 L(n) 型的 t 的数量；例如，
N(15) = 832。

求 1 ≤ n ≤ 10 时的 sum N(n)。
"""

from collections import defaultdict
from math import ceil, sqrt


def solution(t_limit: int = 1000000, n_limit: int = 10) -> int:
    """
    返回 1 <= n <= n_limit 时 N(n) 的总和。

    >>> solution(1000,5)
    222
    >>> solution(1000,10)
    249
    >>> solution(10000,10)
    2383
    """
    count: defaultdict = defaultdict(int)

    for outer_width in range(3, (t_limit // 4) + 2):
        if outer_width * outer_width > t_limit:
            hole_width_lower_bound = max(
                ceil(sqrt(outer_width * outer_width - t_limit)), 1
            )
        else:
            hole_width_lower_bound = 1

        hole_width_lower_bound += (outer_width - hole_width_lower_bound) % 2

        for hole_width in range(hole_width_lower_bound, outer_width - 1, 2):
            count[outer_width * outer_width - hole_width * hole_width] += 1

    return sum(1 for n in count.values() if 1 <= n <= n_limit)


if __name__ == "__main__":
    print(f"{solution() = }")
