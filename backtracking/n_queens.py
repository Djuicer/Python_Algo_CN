"""

N 皇后（N-Queens）问题要求在 N * N 棋盘上放置 N 个皇后，
使任意皇后都无法攻击棋盘上的
其他皇后。
也就是说，每个皇后所在的横线、竖线和
对角线上都不能有其他皇后。

"""

from __future__ import annotations

solution = []


def is_safe(board: list[list[int]], row: int, column: int) -> bool:
    """
    根据棋盘当前状态，若可以安全地在指定位置放置皇后，
    则返回布尔值 True。

    参数：
    board (2D matrix): 棋盘
    row, column: 棋盘单元格的坐标

    返回：
    布尔值

    >>> is_safe([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 1, 1)
    True
    >>> is_safe([[0, 1, 0], [0, 0, 0], [0, 0, 0]], 1, 1)
    False
    >>> is_safe([[1, 0, 0], [0, 0, 0], [0, 0, 0]], 1, 1)
    False
    >>> is_safe([[0, 0, 1], [0, 0, 0], [0, 0, 0]], 1, 1)
    False
    >>> is_safe([[1, 0, 0], [0, 0, 0], [0, 0, 0]], 1, 2)
    True
    >>> is_safe([[1, 0, 0], [0, 0, 0], [0, 0, 0]], 2, 1)
    True
    >>> is_safe([[0, 0, 0], [1, 0, 0], [0, 0, 0]], 0, 2)
    True
    >>> is_safe([[0, 0, 0], [1, 0, 0], [0, 0, 0]], 2, 2)
    True
    """

    n = len(board)  # 棋盘大小

    # 检查同列上方、左上对角线和右上对角线上
    # 是否存在皇后
    return (
        all(board[i][j] != 1 for i, j in zip(range(row), [column] * row))
        and all(
            board[i][j] != 1
            for i, j in zip(range(row - 1, -1, -1), range(column - 1, -1, -1))
        )
        and all(
            board[i][j] != 1
            for i, j in zip(range(row - 1, -1, -1), range(column + 1, n))
        )
    )


def solve(board: list[list[int]], row: int) -> bool:
    """
    创建状态空间树并调用安全检查函数，直到
    收到布尔值 False 时终止该分支，回溯到下一个
    可能产生解的分支。
    """
    if row >= len(board):
        """
        若行号超过 N，说明棋盘上的皇后组合有效，
        将该组合加入解列表并输出棋盘。
        """
        solution.append(board)
        printboard(board)
        print()
        return True
    for i in range(len(board)):
        """
        对每一行，遍历各列，检查是否能在相应位置
        放置皇后。
        若该分支中的所有组合均成功，则重新初始化棋盘，
        以搜索下一个可能的组合。
        """
        if is_safe(board, row, i):
            board[row][i] = 1
            solve(board, row + 1)
            board[row][i] = 0
    return False


def printboard(board: list[list[int]]) -> None:
    """
    输出成功放置皇后的棋盘。
    """
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                print("Q", end=" ")  # 此处有皇后
            else:
                print(".", end=" ")  # 空单元格
        print()


# 皇后数量（例如 n=8 表示 8x8 棋盘）
n = 8
board = [[0 for i in range(n)] for j in range(n)]
solve(board, 0)
print("The total number of solutions are:", len(solution))
