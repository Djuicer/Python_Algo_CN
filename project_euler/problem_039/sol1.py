"""
Problem 39: https://projecteuler.net/problem=39

如果 p 是边长均为整数的直角三角形 {a,b,c} 的周长，那么 p = 120 恰好有三个解。
{20,48,52}, {24,45,51}, {30,40,50}

当 p ≤ 1000 时，哪个 p 值对应的解数最多？
"""

from __future__ import annotations

import typing
from collections import Counter


def pythagorean_triple(max_perimeter: int) -> typing.Counter[int]:
    """
    返回一个字典，键为直角三角形的周长，值为对应三元组的数量。
    >>> pythagorean_triple(15)
    Counter({12: 1})
    >>> pythagorean_triple(40)
    Counter({12: 1, 30: 1, 24: 1, 40: 1, 36: 1})
    >>> pythagorean_triple(50)
    Counter({12: 1, 30: 1, 24: 1, 40: 1, 36: 1, 48: 1})
    """
    triplets: typing.Counter[int] = Counter()
    for base in range(1, max_perimeter + 1):
        for perpendicular in range(base, max_perimeter + 1):
            hypotenuse = (base * base + perpendicular * perpendicular) ** 0.5
            if hypotenuse == int(hypotenuse):
                perimeter = int(base + perpendicular + hypotenuse)
                if perimeter > max_perimeter:
                    continue
                triplets[perimeter] += 1
    return triplets


def solution(n: int = 1000) -> int:
    """
    返回解数最多的周长。
    >>> solution(100)
    90
    >>> solution(200)
    180
    >>> solution(1000)
    840
    """
    triplets = pythagorean_triple(n)
    return triplets.most_common(1)[0][0]


if __name__ == "__main__":
    print(f"Perimeter {solution()} has maximum solutions")
