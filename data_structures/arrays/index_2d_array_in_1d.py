"""
Retrieves 该值 的 0-indexed 1D 索引 从 2D 数组。
其中 是 两个 ways 到 retrieve 值(s)：

1. Index2DArrayIterator(矩阵) -> 迭代器[int]
此 迭代器 允许 you 到 迭代 通过 2D 数组 通过 passing 在 矩阵 并且
calling 下一个(your_iterator). You 可以 也 使用 迭代器 在 循环。
示例：
列表(Index2DArrayIterator(矩阵))
集合(Index2DArrayIterator(矩阵))
元组(Index2DArrayIterator(矩阵))
和(Index2DArrayIterator(矩阵))
-5 在 Index2DArrayIterator(矩阵)

2. index_2d_array_in_1d(数组: 列表[int]，索引: int) -> int
此函数 允许 you 到 提供 2D 数组 并且 0-indexed 1D 整数 索引,
并且 retrieves 整数 值 在 该 索引。

Python doctests 可以 为 运行 使用 此 命令：
python3 -m doctest -v index_2d_array_in_1d.py
"""

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Index2DArrayIterator:
    matrix: list[list[int]]

    def __iter__(self) -> Iterator[int]:
        """
        >>> tuple(Index2DArrayIterator([[5], [-523], [-1], [34], [0]]))
        (5, -523, -1, 34, 0)
        >>> tuple(Index2DArrayIterator([[5, -523, -1], [34, 0]]))
        (5, -523, -1, 34, 0)
        >>> tuple(Index2DArrayIterator([[5, -523, -1, 34, 0]]))
        (5, -523, -1, 34, 0)
        >>> t = Index2DArrayIterator([[5, 2, 25], [23, 14, 5], [324, -1, 0]])
        >>> tuple(t)
        (5, 2, 25, 23, 14, 5, 324, -1, 0)
        >>> list(t)
        [5, 2, 25, 23, 14, 5, 324, -1, 0]
        >>> sorted(t)
        [-1, 0, 2, 5, 5, 14, 23, 25, 324]
        >>> tuple(t)[3]
        23
        >>> sum(t)
        397
        >>> -1 in t
        True
        >>> t = iter(Index2DArrayIterator([[5], [-523], [-1], [34], [0]]))
        >>> next(t)
        5
        >>> next(t)
        -523
        """
        for row in self.matrix:
            yield from row


def index_2d_array_in_1d(array: list[list[int]], index: int) -> int:
    """
    Retrieves 该值 的 一个-dimensional 索引 从 两个-dimensional 数组。

    参数：
        数组: 2D 数组 的 整数 其中 所有 rows 是 相同 大小 并且 所有
               columns 是 相同 大小。
        索引: 1D 索引。

    返回值：
        int: 0-indexed 值 的 1D 索引 在 该数组。

    示例：
    >>> index_2d_array_in_1d([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]], 5)
    5
    >>> index_2d_array_in_1d([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]], -1)
    Traceback (most recent call last):
        ...
    ValueError: index out of range
    >>> index_2d_array_in_1d([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]], 12)
    Traceback (most recent call last):
        ...
    ValueError: index out of range
    >>> index_2d_array_in_1d([[]], 0)
    Traceback (most recent call last):
        ...
    ValueError: no items in array
    """
    rows = len(array)
    cols = len(array[0])

    if rows == 0 or cols == 0:
        raise ValueError("no items in array")

    if index < 0 or index >= rows * cols:
        raise ValueError("index out of range")

    return array[index // cols][index % cols]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
