"""
Sparse table 是 数据 结构 该 允许 answering 范围 queries 在
static 数 列表，i.e. 元素 do 不 更改 throughout 所有 queries。

实现 下方 将 solve problem 的 范围 最小值 查询：
Finding 最小值 值 的 子集 [L..R] 的 static 数 列表。

Overall 时间复杂度: O(nlogn)
Overall 空间复杂度: O(nlogn)

Wikipedia link: https://en.wikipedia.org/wiki/Range_minimum_query
"""

from math import log2


def build_sparse_table(number_list: list[int]) -> list[list[int]]:
    """
    Precompute 范围 最小值 queries 带有 power 的 两个 长度 并且 存储 precomputed
    值 在 table。

    >>> build_sparse_table([8, 1, 0, 3, 4, 9, 3])
    [[8, 1, 0, 3, 4, 9, 3], [1, 0, 0, 3, 4, 3, 0], [0, 0, 0, 3, 0, 0, 0]]
    >>> build_sparse_table([3, 1, 9])
    [[3, 1, 9], [1, 1, 0]]
    >>> build_sparse_table([])
    Traceback (most recent call last):
    ...
    ValueError: empty number list not allowed
    """
    if not number_list:
        raise ValueError("empty number list not allowed")

    length = len(number_list)
    # 初始化 sparse_table -- sparse_table[j][i] 表示 最小值 值 的
    # 子集 的 长度 (2 ** j) 的 number_list，起始 从 索引 i。

    # 最小 power 的 2 子集 长度 该 fully covers number_list
    row = int(log2(length)) + 1
    sparse_table = [[0 for i in range(length)] for j in range(row)]

    # 最小值 的 子集 的 长度 1 是 该 值 自身
    for i, value in enumerate(number_list):
        sparse_table[0][i] = value
    j = 1

    # 计算 最小值 值 用于 所有 区间 带有 大小 (2 ** j)
    while (1 << j) <= length:
        i = 0
        # 当 子集 起始 从 i 仍然 具有 在 least (2 ** j) 元素
        while (i + (1 << j) - 1) < length:
            # 拆分 范围 [i，i + 2 ** j] 并且 查找 最小值 的 2 halves
            sparse_table[j][i] = min(
                sparse_table[j - 1][i + (1 << (j - 1))], sparse_table[j - 1][i]
            )
            i += 1
        j += 1
    return sparse_table


def query(sparse_table: list[list[int]], left_bound: int, right_bound: int) -> int:
    """
    >>> query(build_sparse_table([8, 1, 0, 3, 4, 9, 3]), 0, 4)
    0
    >>> query(build_sparse_table([8, 1, 0, 3, 4, 9, 3]), 4, 6)
    3
    >>> query(build_sparse_table([3, 1, 9]), 2, 2)
    9
    >>> query(build_sparse_table([3, 1, 9]), 0, 1)
    1
    >>> query(build_sparse_table([8, 1, 0, 3, 4, 9, 3]), 0, 11)
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> query(build_sparse_table([]), 0, 0)
    Traceback (most recent call last):
    ...
    ValueError: empty number list not allowed
    """
    if left_bound < 0 or right_bound >= len(sparse_table[0]):
        raise IndexError("list index out of range")

    # 最高 子集 长度 的 power 的 2 该 是 之内 范围 [left_bound，right_bound]
    j = int(log2(right_bound - left_bound + 1))

    # 最小值 的 2 重叠 更小 subsets：
    # [left_bound，left_bound + 2 ** j - 1] 并且 [right_bound - 2 ** j + 1，right_bound]
    return min(sparse_table[j][right_bound - (1 << j) + 1], sparse_table[j][left_bound])


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    print(f"{query(build_sparse_table([3, 1, 9]), 2, 2) = }")
