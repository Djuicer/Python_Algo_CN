"""
给定一个表示高程图的非负整数数组，其中每个柱子的宽度为 1，
此程序计算可以收集多少雨水。

示例 - height = (0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1)
输出：6
此问题可以使用“动态规划（DYNAMIC PROGRAMMING）”的概念求解。

计算数组中每个柱子左右两侧柱子的最大高度，然后逐个遍历结构中的每个索引。
可存储的水量等于两侧柱子最大高度的较小值减去当前位置柱子的高度。
"""


def trapped_rainwater(heights: tuple[int, ...]) -> int:
    """
    trapped_rainwater 函数根据给定的柱高数组计算可收集的雨水总量。
    它使用动态规划方法，确定每个柱子两侧柱子的最大高度，
    然后计算每个柱子上方收集的雨水。函数返回收集的雨水总量。

    >>> trapped_rainwater((0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1))
    6
    >>> trapped_rainwater((7, 1, 5, 3, 6, 4))
    9
    >>> trapped_rainwater((7, 1, 5, 3, 6, -1))
    Traceback (most recent call last):
        ...
    ValueError: No height can be negative
    """
    if not heights:
        return 0
    if any(h < 0 for h in heights):
        raise ValueError("No height can be negative")
    length = len(heights)

    left_max = [0] * length
    left_max[0] = heights[0]
    for i, height in enumerate(heights[1:], start=1):
        left_max[i] = max(height, left_max[i - 1])

    right_max = [0] * length
    right_max[-1] = heights[-1]
    for i in range(length - 2, -1, -1):
        right_max[i] = max(heights[i], right_max[i + 1])

    return sum(
        min(left, right) - height
        for left, right, height in zip(left_max, right_max, heights)
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(f"{trapped_rainwater((0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1)) = }")
    print(f"{trapped_rainwater((7, 1, 5, 3, 6, 4)) = }")
