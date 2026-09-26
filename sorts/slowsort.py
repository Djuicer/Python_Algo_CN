"""
慢排序（Slowsort）是一种带有幽默性质、没有实用价值的排序算法。
它基于“倍增并投降”（multiply and surrender）的原则，
是对“分而治之”（divide and conquer）的戏仿。
Andrei Broder 和 Jorge Stolfi 于 1986 年在论文
Pessimal Algorithms and Simplexity Analysis 中发表了该算法
（该论文戏仿了最优算法与复杂度分析）。

Source: https://en.wikipedia.org/wiki/Slowsort
"""

from __future__ import annotations

from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def slowsort[T: Comparable](
    sequence: list[T], start: int | None = None, end: int | None = None
) -> None:
    """
    原地排序 sequence[start..end]（包含两端）。
    未提供 start 时默认为 0。
    未提供 end 时默认为 len(sequence) - 1。
    返回 None。
    >>> seq = [1, 6, 2, 5, 3, 4, 4, 5]; slowsort(seq); seq
    [1, 2, 3, 4, 4, 5, 5, 6]
    >>> seq = ["c", "a", "b"]; slowsort(seq); seq
    ['a', 'b', 'c']
    >>> seq = [2.5, -1, 0.0]; slowsort(seq); seq
    [-1, 0.0, 2.5]
    >>> slowsort([1, "a"])
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    >>> seq = []; slowsort(seq); seq
    []
    >>> seq = [2]; slowsort(seq); seq
    [2]
    >>> seq = [1, 2, 3, 4]; slowsort(seq); seq
    [1, 2, 3, 4]
    >>> seq = [4, 3, 2, 1]; slowsort(seq); seq
    [1, 2, 3, 4]
    >>> seq = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]; slowsort(seq, 2, 7); seq
    [9, 8, 2, 3, 4, 5, 6, 7, 1, 0]
    >>> seq = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]; slowsort(seq, end = 4); seq
    [5, 6, 7, 8, 9, 4, 3, 2, 1, 0]
    >>> seq = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]; slowsort(seq, start = 5); seq
    [9, 8, 7, 6, 5, 0, 1, 2, 3, 4]
    """
    if start is None:
        start = 0

    if end is None:
        end = len(sequence) - 1

    if start >= end:
        return

    mid = (start + end) // 2

    slowsort(sequence, start, mid)
    slowsort(sequence, mid + 1, end)

    if sequence[end] < sequence[mid]:
        sequence[end], sequence[mid] = sequence[mid], sequence[end]

    slowsort(sequence, start, end - 1)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
