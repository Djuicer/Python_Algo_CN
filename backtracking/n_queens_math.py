r"""
问题：

N 皇后（N-Queens）问题要求在 N * N 棋盘上放置 N 个皇后，
使任意皇后都无法攻击其他皇后。也就是说，每个皇后
所在的横线、竖线和对角线上都不能有其他皇后。

解法：

使用简单的数学知识求解。皇后可以沿所有
允许的方向移动，概括为：竖直、水平、左对角线和
 右对角线。

可以直观地表示为：

左对角线 = \
右对角线 = /

在棋盘上，竖直移动可以对应行的变化，水平移动可以对应
列的变化。

在程序中可以使用数组，每个索引表示行，
每个值表示列。例如：

    . Q . .     此棋盘每列都有一个皇后，且皇后之间
    . . . Q     不能互相攻击。
    Q . . .     对应的数组为：[1, 3, 0, 2]
    . . Q .

若使用数组，并验证其中各值互不相同，
就能保证皇后至少不会在水平和
竖直方向上互相攻击。

至此已完成一半，接下来将棋盘视为
笛卡尔坐标平面。回顾基础数学知识，
可以用到以下公式：

    直线斜率：

           y2 - y1
     m = ----------
          x2 - x1

此公式可以求出斜率。对于 45º（右对角线）和 135º
（左对角线），计算结果分别为 m = 1 和 m = -1。

参见：
https://www.enotes.com/homework-help/write-equation-line-that-hits-origin-45-degree-1474860

另有以下公式：

斜截式：

y = mx + b

b 表示直线与 Y 轴的交点纵坐标（更多信息见：
https://www.mathsisfun.com/y_intercept.html），将公式改写为求 b，
得到：

y - mx = b

已知 45º 和 135º 对应的 m 值，公式可写为
如下形式：

45º: y - (1)x = b
45º: y - x = b

135º: y - (-1)x = b
135º: y + x = b

y = row
x = column

应用这两个公式，可以检查某个位置的皇后是否受到
另一个皇后的攻击，反之亦然。

"""

from __future__ import annotations


def depth_first_search(
    possible_board: list[int],
    diagonal_right_collisions: list[int],
    diagonal_left_collisions: list[int],
    boards: list[list[str]],
    n: int,
) -> None:
    """
    >>> boards = []
    >>> depth_first_search([], [], [], boards, 4)
    >>> for board in boards:
    ...     print(board)
    ['. Q . . ', '. . . Q ', 'Q . . . ', '. . Q . ']
    ['. . Q . ', 'Q . . . ', '. . . Q ', '. Q . . ']
    """

    # 获取当前棋盘（possible_board）中下一个待放置皇后的行
    row = len(possible_board)

    # 若 row 等于棋盘大小，则当前棋盘（possible_board）的每一行
    # 都已有一个皇后
    if row == n:
        # 将 possible_board 从 [1, 3, 0, 2] 这样的形式转换为
        # this: ['. Q . . ', '. . . Q ', 'Q . . . ', '. . Q . ']
        boards.append([". " * i + "Q " + ". " * (n - 1 - i) for i in possible_board])
        return

    # 遍历该行的每一列，以找出该行所有可能的放置结果
    for col in range(n):
        # 应用前述知识。首先检查当前棋盘
        # （possible_board）中是否存在相同值；如果存在，
        # 就表示竖直方向上发生冲突。然后应用之前介绍的
        # 两个公式：
        #
        # 45º: y - x = b or 45: row - col = b
        # 135º: y + x = b or row + col = b.
        #
        # 检查这两个公式的结果是否分别不存在于
        # 对应变量中。（diagonal_right_collisions, diagonal_left_collisions）
        #
        # 若任意一项为 True，说明存在冲突，因此继续处理
        # for 循环中的下一个值。
        if (
            col in possible_board
            or row - col in diagonal_right_collisions
            or row + col in diagonal_left_collisions
        ):
            continue

        # 若为 False，则更新输入并再次调用 dfs 函数
        depth_first_search(
            [*possible_board, col],
            [*diagonal_right_collisions, row - col],
            [*diagonal_left_collisions, row + col],
            boards,
            n,
        )


def n_queens_solution(n: int) -> None:
    boards: list[list[str]] = []
    depth_first_search([], [], [], boards, n)

    # 输出所有棋盘
    for board in boards:
        for column in board:
            print(column)
        print("")

    print(len(boards), "solutions were found.")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    n_queens_solution(4)
