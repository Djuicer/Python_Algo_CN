"""
查找 平衡 索引 的 一个数组。

引用：
https://www.geeksforgeeks.org/equilibrium-index-of-an-array

Python doctest 可以 为 运行 带有：

python -m doctest -v equilibrium_index_in_array.py

给定一个数组 arr 的 大小 n，返回 平衡 索引
如果 一个 存在; 否则 返回 -1。

平衡 索引 是 一个索引 其中 和 的 所有
元素 到 左 equals 和 的 所有元素
到 右。
"""


def equilibrium_index(arr: list[int]) -> int:
    """
    查找 第一个 平衡 索引 的 一个数组。
    参数：
        arr: 输入 数组 的 整数。
    返回值：
        第一个 平衡 索引，或 -1 如果 none 存在。
    示例：
        >>> equilibrium_index([])
        -1
        >>> equilibrium_index([5])
        0
        >>> equilibrium_index([-7, 1, 5, 2, -4, 3, 0])
        3
        >>> equilibrium_index([2, 4, 6, 8, 10, 3])
        -1
        >>> equilibrium_index([1, 2, 3, 4, 5])
        -1
        >>> equilibrium_index([1, 1, 1, 1, 1])
        2
        >>> equilibrium_index([0, 0, 0])
        0
        >>> equilibrium_index([-1, -1, -1])
        1
        >>> equilibrium_index([1, -1, 0])
        2

    时间复杂度：
        O(n)，其中 n 是 长度 的 该数组。

    空间复杂度：
        O(1)，使用 仅 constant extra 空间。
    """
    total_sum = sum(arr)
    left_sum = 0
    for i, value in enumerate(arr):
        total_sum -= value
        if left_sum == total_sum:
            return i
        left_sum += value
    return -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
