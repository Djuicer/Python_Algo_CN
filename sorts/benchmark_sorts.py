#!/usr/bin/env -S uv run --script

"""
在相同的随机数据集上对多种排序算法进行基准测试。

这是用于参考的基准测试，而非严谨的性能评测：在少量共享的
随机整数数据集上计时，输出简短的
对比表，便于读者直观比较本目录中不同
策略的实际开销，无需将计时代码嵌入
各个算法模块（使这些文件保持简洁、导入开销小，
并专注于提供易读的参考实现）。

从仓库根目录运行：

    python -m sorts.benchmark_sorts

各算法从其对应模块导入，因此本文件
不重复实现排序算法。
"""

import random
import sys
from collections.abc import Callable, Sequence
from itertools import pairwise
from timeit import timeit
from typing import Protocol

from sorts.bubble_sort import bubble_sort_iterative
from sorts.cocktail_shaker_sort import cocktail_shaker_sort
from sorts.comb_sort import comb_sort
from sorts.gnome_sort import gnome_sort
from sorts.heap_sort import heap_sort
from sorts.insertion_sort import insertion_sort
from sorts.merge_sort import merge_sort
from sorts.quick_sort import quick_sort
from sorts.selection_sort import selection_sort
from sorts.shell_sort import shell_sort
from sorts.tim_sort import tim_sort

# 名称 -> 可调用对象。每个对象接收列表并返回排序后的列表。
SORTS: dict[str, Callable[[list[int]], Sequence[int]]] = {
    "bubble_sort": bubble_sort_iterative,
    "cocktail_shaker_sort": cocktail_shaker_sort,
    "comb_sort": comb_sort,
    "gnome_sort": gnome_sort,
    "heap_sort": heap_sort,
    "insertion_sort": insertion_sort,
    "merge_sort": merge_sort,
    "quick_sort": quick_sort,
    "selection_sort": selection_sort,
    "shell_sort": shell_sort,
    "tim_sort": tim_sort,
}


def is_sorted(collection: Sequence[int]) -> bool:
    """
    若每个元素都小于或等于下一个元素，则返回 True。

    >>> is_sorted([1, 2, 2, 3])
    True
    >>> is_sorted([1, 3, 2])
    False
    >>> is_sorted([])
    True
    """
    return all(a <= b for a, b in pairwise(collection))


def all_sorts_agree(data: list[int]) -> bool:
    """
    若 ``SORTS`` 中每个算法都能正确排序 ``data``，则返回 True。

    为每个算法提供新的数据副本（部分算法会原地排序），并将
    结果与 Python 内置 ``sorted`` 的结果比较，以验证正确性。

    >>> all_sorts_agree([5, 1, 4.2, 2, 8.5, 0, 2])
    True
    >>> all_sorts_agree([])
    True
    >>> all_sorts_agree([42])
    True
    >>> all_sorts_agree(list(range(5, -6, -1)))
    True
    >>> all_sorts_agree(list("Python"))
    True
    """
    expected = sorted(data)
    return all(list(sort_fn(data.copy())) == expected for sort_fn in SORTS.values())


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def benchmark[T: Comparable](data: list[T], number: int = 1) -> dict[str, float]:
    """
    对 ``SORTS`` 中的每个算法在 ``data`` 副本上的执行进行计时。

    返回算法名到重复执行 ``number`` 次所耗秒数的映射。
    每次计时调用都接收新的副本，避免原地排序算法
    使下一次重复执行收到已经排好序的列表。

    >>> benchmark([])
    Traceback (most recent call last):
        ...
    ValueError: Please provide a non-empty dataset
    >>> benchmark([1], number=0)
    Traceback (most recent call last):
        ...
    ValueError: Number of repetitions must be positive
    """
    if not data:
        raise ValueError("Please provide a non-empty dataset")
    if number <= 0:
        raise ValueError("Number of repetitions must be positive")
    timings: dict[str, float] = {}
    for name, sort_fn in SORTS.items():
        timings[name] = timeit(lambda fn=sort_fn: fn(data.copy()), number=number)
    return timings


def main() -> None:
    # 部分导入的算法（如 tim_sort）使用递归合并，因此
    # 为它们留出足够的递归深度，避免排序最大数据集时达到上限。
    sys.setrecursionlimit(10_000)
    sizes = (100, 1_000, 3_000)
    random.seed(0)
    datasets = {size: [random.randint(0, size) for _ in range(size)] for size in sizes}

    header = "algorithm".ljust(22) + "".join(f"{size:>12}" for size in sizes)
    print(header)
    print("-" * len(header))

    per_size = {size: benchmark(data) for size, data in datasets.items()}
    for name in SORTS:
        row = name.ljust(22)
        row += "".join(f"{per_size[size][name]:>12.4f}" for size in sizes)
        print(row)

    print("\nseconds per sort (lower is better); dataset = uniform random ints")


if __name__ == "__main__":
    main()
