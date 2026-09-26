"""
给定一个网格，从左上角位置 [0, 0] 出发，求到达右下角位置的路径数量。

从此处开始 ->   0  0  0  0
                 1  1  0  0
                 0  0  0  1
                 0  1  0  0  <- 在此处结束
可以通过多少条“不同的”路径到达终点？
使用下方的递归深度优先搜索算法，可以求出不同路径的数量（count）。

'*' 表示一条路径。
上例中有两条不同的路径：
1.                2.
    *  *  *  0      *  *  *  *
    1  1  *  0      1  1  *  *
    0  0  *  1      0  0  *  1
    0  1  *  *      0  1  *  *
"""


def depth_first_search(grid: list[list[int]], row: int, col: int, visit: set) -> int:
    """
    递归回溯深度优先搜索算法。

    从矩阵左上角出发，统计可到达矩阵右下角的路径数量。
    1 表示障碍（不可访问）
    0 表示有效空间（可访问）

    0  0  0  0
    1  1  0  0
    0  0  0  1
    0  1  0  0
    >>> grid = [[0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0]]
    >>> depth_first_search(grid, 0, 0, set())
    2

    0  0  0  0  0
    0  1  1  1  0
    0  1  1  1  0
    0  0  0  0  0
    >>> grid = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]]
    >>> depth_first_search(grid, 0, 0, set())
    2
    """
    row_length, col_length = len(grid), len(grid[0])
    if (
        min(row, col) < 0
        or row == row_length
        or col == col_length
        or (row, col) in visit
        or grid[row][col] == 1
    ):
        return 0
    if row == row_length - 1 and col == col_length - 1:
        return 1

    visit.add((row, col))

    count = 0
    count += depth_first_search(grid, row + 1, col, visit)
    count += depth_first_search(grid, row - 1, col, visit)
    count += depth_first_search(grid, row, col + 1, visit)
    count += depth_first_search(grid, row, col - 1, visit)

    visit.remove((row, col))
    return count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
