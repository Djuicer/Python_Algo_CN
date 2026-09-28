"""
Author  : Matheus F. Vesco
Date    : October 3, 2023

实现 的 pairwise 迭代 algorithms，其 可以 为 useful 在
many domains.
Currently，其中 是 两个 不同 implementations。
"""

from collections.abc import Iterable, Iterator
from itertools import tee


def pairwise_iteration_tee(iterable: Iterable) -> Iterator[tuple]:
    """
    生成 对 的 元素 从 可迭代对象 仅 类似：
    https://docs.python.org/3/library/itertools.html#itertools.pairwise

    此函数 使用 `tee` 函数 从 `itertools` module 到
    创建 两个 独立 迭代器 (`` 并且 `b`) 从 输入
    可迭代对象. `下一个` 函数 是 使用 到 offset `b` 迭代器 通过
    一个 索引，并且 则 两个 迭代器 是 zipped together 到 创建
    对 的 元素. 此 实现 应 work 带有 任意 可迭代对象
    在 Python。

    参数：
        可迭代对象 (可迭代对象): 输入 可迭代对象。

    Yields:
        迭代器[元组]: 迭代器 该 yields 对 的 objects。

    示例：
        >>> list(pairwise_iteration_tee([1, 2, 3]))
        [(1, 2), (2, 3)]

        >>> list(pairwise_iteration_tee((4, 3, 5)))
        [(4, 3), (3, 5)]

        >>> list(pairwise_iteration_tee({'x':3, 'y':1, 'z':2, 'foo':4}))
        [('x', 'y'), ('y', 'z'), ('z', 'foo')]

        >>> list(pairwise_iteration_tee('2345'))
        [('2', '3'), ('3', '4'), ('4', '5')]

        >>> list(pairwise_iteration_tee(['ATG','GCT','TGC','TAA']))
        [('ATG', 'GCT'), ('GCT', 'TGC'), ('TGC', 'TAA')]

        >>> list(pairwise_iteration_tee(['a']))
        []

        >>> from itertools import pairwise
        >>> all(list(pairwise_iteration_tee(test)) == list(pairwise(test))
        ... for test in (
        ...     [1, 2, 3],
        ...     (4, 3, 5),
        ...     {'x':3, 'y':1, 'z':2, 'foo':4},
        ...     '2345',
        ...     ['ATG','GCT','TGC','TAA'],
        ...     [],
        ... ))
        True
    """
    # 使用 itertools.tee 到 创建 两个 独立 迭代器 (并且 b)
    # 从 可迭代对象. 此 表示 我们 可以 使用 下一个() 在 每个 一个
    # 不使用 affecting 另一个，没有 matter 可迭代对象 类型
    a, b = tee(iterable)

    # Offsets 第二个 迭代器 (b) 通过 一个 步骤 到 创建一个 staggered
    # 对齐。
    # 此 表示 该 ([i],b[i]) 表示 相同 作为 ([i],[i+1])
    next(b, None)

    # 返回值 zip generator 该 对 元素 从 两个 迭代器 在
    # 格式 ([i]，[i+1])。
    return zip(a, b)


def pairwise_iteration_comprehension(
    iterable: Iterable, step: int = 1
) -> Iterator[tuple]:
    """
    生成 对 的 元素 从 可迭代对象 带有 给定 步骤 大小。

    此函数 使用 列表 comprehensions 到 获取 元素 该 是 步骤
    距离 从 每个 另一个 并且 later `iter()` conversion 到 创建
    两个 独立 列表 迭代器 (`` 并且 `b`) 从 输入 可迭代对象。
    `下一个` 函数 是 使用 到 offset `b` 迭代器 通过 一个 索引,
    并且 则 两个 迭代器 是 zipped together 到 创建 对 的
    元素。

    参数：
        可迭代对象 (可迭代对象): 输入 可迭代对象。
        步骤 (int，可选): 步骤 大小 用于 iterating 通过
        输入 可迭代对象. 默认值 到 1。

    Yields:
        迭代器[元组]: 迭代器 该 yields 对 的 objects。

    示例：
        >>> list(pairwise_iteration_comprehension([0, 1, 2, 3, 4, 5, 6], step=2))
        [(0, 2), (2, 4), (4, 6)]

        >>> list(pairwise_iteration_comprehension([0, 1, 2, 3, 4, 5, 6], step=3))
        [(0, 3), (3, 6)]

        >>> list(pairwise_iteration_comprehension((0, 1, 2, 3, 4), step=2))
        [(0, 2), (2, 4)]

        >>> python_set = pairwise_iteration_comprehension(
        ...     {4, 3, 2, 1, 0}, step=2)
        >>> list(python_set) # sets are unordered
        [(0, 2), (2, 4)]

        >>> dictionary = pairwise_iteration_comprehension(
        ...     {'x1':4, 'y1':5, 'x2':1, 'y2':'a', 'spam':7}, step=2)
        >>> list(dictionary)
        [('x1', 'x2'), ('x2', 'spam')]

        >>> list(pairwise_iteration_comprehension({0, 1, 2, 3, 4, 5, 6}, step=3))
        [(0, 3), (3, 6)]

        >>> list(pairwise_iteration_comprehension(['ATG','GCT','TGC','TAA']))
        [('ATG', 'GCT'), ('GCT', 'TGC'), ('TGC', 'TAA')]

        >>> list(pairwise_iteration_comprehension(['a'], step=1))
        []
    """
    # 创建一个 列表，使用 列表 comprehensions，该 仅 存储 元素
    # 该 是 n 步骤 apart 从 每个 另一个。
    items = [item for i, item in enumerate(iterable) if i % step == 0]

    # creates 两个 独立 列表 迭代器 (并且 b) 从 该列表
    # 我们 created earlier，使用 iter() 函数. 此 表示 我们 可以
    # 使用 下一个() 在 每个 一个 不使用 affecting 另一个，没有 matter
    # 可迭代对象 类型
    a, b = (iter(items), iter(items))

    # Offsets 第二个 迭代器 (b) 通过 一个 步骤 到 创建一个 staggered
    # 对齐。
    # 此 表示 该 ([i],b[i]) 表示 相同 作为 ([i],[i+1])
    next(b, None)

    # 返回值 zip generator 该 对 元素 从 两个 迭代器 在
    # 格式 ([i]，[i+1])。
    return zip(a, b)
