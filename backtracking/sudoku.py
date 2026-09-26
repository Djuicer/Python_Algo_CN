"""
给定一个部分填入数字的 9x9 二维数组，目标是在 9x9
方格中填入 1 到 9，使每一行、每一列以及
九个 3x3 子宫格都包含全部数字。

可使用回溯法求解，与 N 皇后问题类似。
检查某个单元格能否安全放置数字，并递归调用
函数处理下一列，检查是否返回 True。若返回 True，
说明已解出谜题；否则回溯，在该单元格中放置另一个数字，
重复此过程。
"""

from __future__ import annotations

Matrix = list[list[int]]

# 为网格赋初始值
initial_grid: Matrix = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0],
    [5, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0],
]

# 无解的网格
no_solution: Matrix = [
    [5, 0, 6, 5, 0, 8, 4, 0, 3],
    [5, 2, 0, 0, 0, 0, 0, 0, 2],
    [1, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0],
]


def is_safe(grid: Matrix, row: int, column: int, n: int) -> bool:
    """
    检查网格中对应的行、
    列以及 3x3 子宫格是否包含数字 'n'。
    若不安全（发现重复数字），则返回 False，
    否则返回 True，表示安全
    """
    for i in range(9):
        if n in {grid[row][i], grid[i][column]}:
            return False

    for i in range(3):
        for j in range(3):
            if grid[(row - row % 3) + i][(column - column % 3) + j] == n:
                return False

    return True


def find_empty_location(grid: Matrix) -> tuple[int, int] | None:
    """
    寻找空位置，以便在对应的行列
    位置填入数字。
    """
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None


def sudoku(grid: Matrix) -> Matrix | None:
    """
    接收部分填好的网格，尝试为所有
    未赋值的位置填入数字，使其满足数独的要求
    （行、列和宫格内均无重复数字）

    >>> sudoku(initial_grid)  # doctest: +NORMALIZE_WHITESPACE
    [[3, 1, 6, 5, 7, 8, 4, 9, 2],
     [5, 2, 9, 1, 3, 4, 7, 6, 8],
     [4, 8, 7, 6, 2, 9, 5, 3, 1],
     [2, 6, 3, 4, 1, 5, 9, 8, 7],
     [9, 7, 4, 8, 6, 3, 1, 2, 5],
     [8, 5, 1, 7, 9, 2, 6, 4, 3],
     [1, 3, 8, 9, 4, 7, 2, 5, 6],
     [6, 9, 2, 3, 5, 1, 8, 7, 4],
     [7, 4, 5, 2, 8, 6, 3, 1, 9]]
     >>> sudoku(no_solution) is None
     True
    """
    if location := find_empty_location(grid):
        row, column = location
    else:
        # 若位置为 ``None``，说明网格已解出。
        return grid

    for digit in range(1, 10):
        if is_safe(grid, row, column, digit):
            grid[row][column] = digit

            if sudoku(grid) is not None:
                return grid

            grid[row][column] = 0

    return None


def print_solution(grid: Matrix) -> None:
    """
    以 9x9 网格形式
    输出解
    """
    for row in grid:
        for cell in row:
            print(cell, end=" ")
        print()


if __name__ == "__main__":
    # 复制 grid，以便与未修改的 grid 比较
    for example_grid in (initial_grid, no_solution):
        print("\nExample grid:\n" + "=" * 20)
        print_solution(example_grid)
        print("\nExample grid solution:")
        solution = sudoku(example_grid)
        if solution is not None:
            print_solution(solution)
        else:
            print("Cannot find a solution.")
