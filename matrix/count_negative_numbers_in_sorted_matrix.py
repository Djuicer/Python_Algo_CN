"""
给定一个所有行和列均按降序排列的数值矩阵，返回 grid 中负数的数量。

参考资料：https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix
"""


def generate_large_matrix() -> list[list[int]]:
    """
    >>> generate_large_matrix() # doctest: +ELLIPSIS
    [[1000, ..., -999], [999, ..., -1001], ..., [2, ..., -1998]]
    """
    return [list(range(1000 - i, -1000 - i, -1)) for i in range(1000)]


grid = generate_large_matrix()
test_grids = (
    [[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]],
    [[3, 2], [1, 0]],
    [[7, 7, 6]],
    [[7, 7, 6], [-1, -2, -3]],
    grid,
)


def validate_grid(grid: list[list[int]]) -> None:
    """
    验证 grid 的行和列均按降序排列。
    >>> for grid in test_grids:
    ...     validate_grid(grid)
    """
    assert all(row == sorted(row, reverse=True) for row in grid)
    assert all(list(col) == sorted(col, reverse=True) for col in zip(*grid))


def find_negative_index(array: list[int]) -> int:
    """
    寻找最小的负数索引。

    >>> find_negative_index([0,0,0,0])
    4
    >>> find_negative_index([4,3,2,-1])
    3
    >>> find_negative_index([1,0,-1,-10])
    2
    >>> find_negative_index([0,0,0,-1])
    3
    >>> find_negative_index([11,8,7,-3,-5,-9])
    3
    >>> find_negative_index([-1,-1,-2,-3])
    0
    >>> find_negative_index([5,1,0])
    3
    >>> find_negative_index([-5,-5,-5])
    0
    >>> find_negative_index([0])
    1
    >>> find_negative_index([])
    0
    """
    left = 0
    right = len(array) - 1

    # 处理没有值或所有数均为负数等边界情况
    if not array or array[0] < 0:
        return 0

    while right + 1 > left:
        mid = (left + right) // 2
        num = array[mid]

        # num 必须为负数，且索引必须大于等于 0
        if num < 0 and array[mid - 1] >= 0:
            return mid

        if num >= 0:
            left = mid + 1
        else:
            right = mid - 1
    # 没有负数，因此返回数组末尾索引加 1，即数组长度
    return len(array)


def count_negatives_binary_search(grid: list[list[int]]) -> int:
    """
    使用二分查找寻找正数与负数边界的 O(m logn) 解法。

    >>> [count_negatives_binary_search(grid) for grid in test_grids]
    [8, 0, 0, 3, 1498500]
    """
    total = 0
    bound = len(grid[0])

    for i in range(len(grid)):
        bound = find_negative_index(grid[i][:bound])
        total += bound
    return (len(grid) * len(grid[0])) - total


def count_negatives_brute_force(grid: list[list[int]]) -> int:
    """
    此解法会遍历每一行和每一列，因此复杂度为 O(n^2)。

    >>> [count_negatives_brute_force(grid) for grid in test_grids]
    [8, 0, 0, 3, 1498500]
    """
    return len([number for row in grid for number in row if number < 0])


def count_negatives_brute_force_with_break(grid: list[list[int]]) -> int:
    """
    与上方暴力解法类似，但使用 break 减少迭代次数。

    >>> [count_negatives_brute_force_with_break(grid) for grid in test_grids]
    [8, 0, 0, 3, 1498500]
    """
    total = 0
    for row in grid:
        for i, number in enumerate(row):
            if number < 0:
                total += len(row) - i
                break
    return total


def benchmark() -> None:
    """对各函数进行并列基准测试。"""
    from timeit import timeit

    print("Running benchmarks")
    setup = (
        "from __main__ import count_negatives_binary_search, "
        "count_negatives_brute_force, count_negatives_brute_force_with_break, grid"
    )
    for func in (
        "count_negatives_binary_search",  # 耗时 0.7727 秒
        "count_negatives_brute_force_with_break",  # 耗时 4.6505 秒
        "count_negatives_brute_force",  # 耗时 12.8160 秒
    ):
        time = timeit(f"{func}(grid=grid)", setup=setup, number=500)
        print(f"{func}() took {time:0.4f} seconds")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
