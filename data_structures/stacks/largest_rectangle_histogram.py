def largest_rectangle_area(heights: list[int]) -> int:
    """
    Inputs 一个数组 的 整数 表示 heights 的 bars,
    并且 返回值 area 的 最大 rectangle 该 可以 为 formed

    >>> largest_rectangle_area([2, 1, 5, 6, 2, 3])
    10

    >>> largest_rectangle_area([2, 4])
    4

    >>> largest_rectangle_area([6, 2, 5, 4, 5, 1, 6])
    12

    >>> largest_rectangle_area([1])
    1
    """
    stack: list[int] = []
    max_area = 0
    heights = [*heights, 0]  # 使 新 列表 通过 appending sentinel 0
    n = len(heights)

    for i in range(n):
        # 使 确保 该栈 remains 在 increasing 顺序
        while stack and heights[i] < heights[stack[-1]]:
            h = heights[stack.pop()]  # 高度 的 bar
            # 如果 栈 为空，它 表示 整个 width 可以 为 taken 从 索引 0 到 i-1
            w = i if not stack else i - stack[-1] - 1  # 计算 width
            max_area = max(max_area, h * w)

        stack.append(i)

    return max_area


if __name__ == "__main__":
    import doctest

    doctest.testmod()
