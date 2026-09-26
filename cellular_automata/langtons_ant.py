"""
兰顿蚂蚁（Langton's Ant）

@ https://en.wikipedia.org/wiki/Langton%27s_ant
@ https://upload.wikimedia.org/wikipedia/commons/0/09/LangtonsAntAnimated.gif
"""

from functools import partial

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

WIDTH = 80
HEIGHT = 80


class LangtonsAnt:
    """
    表示 LangtonsAnt 主算法。

    >>> la = LangtonsAnt(2, 2)
    >>> la.board
    [[True, True], [True, True]]
    >>> la.ant_position
    (1, 1)
    """

    def __init__(self, width: int, height: int) -> None:
        # 每个方格取 True 或 False，其中 True 表示白色，False 表示黑色
        self.board = [[True] * width for _ in range(height)]
        self.ant_position: tuple[int, int] = (width // 2, height // 2)

        # 初始方向朝左（与 Wikipedia 图像类似）
        # (0 = 0° | 1 = 90° | 2 = 180 ° | 3 = 270°)
        self.ant_direction: int = 3

    def move_ant(self, axes: plt.Axes | None, display: bool, _frame: int) -> None:
        """
        执行三项任务：
            1. 蚂蚁根据当前所在方格的颜色顺时针或逆时针转向。方格为白色时
            顺时针转向，为黑色时逆时针转向
            2. 蚂蚁沿当前朝向移动一个方格
            3. 翻转蚂蚁之前所在方格的颜色（白色 -> 黑色，黑色 -> 白色）

        如果 display 为 True，还会在坐标轴上显示棋盘。

        >>> la = LangtonsAnt(2, 2)
        >>> la.move_ant(None, True, 0)
        >>> la.board
        [[True, True], [True, False]]
        >>> la.move_ant(None, True, 0)
        >>> la.board
        [[True, False], [True, False]]
        """
        directions = {
            0: (-1, 0),  # 0°
            1: (0, 1),  # 90°
            2: (1, 0),  # 180°
            3: (0, -1),  # 270°
        }
        x, y = self.ant_position

        # 根据方格颜色顺时针或逆时针转向
        if self.board[x][y] is True:
            # 方格为白色，因此顺时针转 90°
            self.ant_direction = (self.ant_direction + 1) % 4
        else:
            # 方格为黑色，因此逆时针转 90°
            self.ant_direction = (self.ant_direction - 1) % 4

        # 移动蚂蚁
        move_x, move_y = directions[self.ant_direction]
        self.ant_position = (x + move_x, y + move_y)

        # 翻转方格颜色
        self.board[x][y] = not self.board[x][y]

        if display and axes:
            # 在坐标轴上显示棋盘
            axes.get_xaxis().set_ticks([])
            axes.get_yaxis().set_ticks([])
            axes.imshow(self.board, cmap="gray", interpolation="nearest")

    def display(self, frames: int = 100_000) -> None:
        """
        在 matplotlib 图中无延迟地显示棋盘，以便直观理解并追踪蚂蚁。

        >>> _ = LangtonsAnt(WIDTH, HEIGHT)
        """
        fig, ax = plt.subplots()
        # 将动画赋给变量，防止其被垃圾回收
        self.animation = FuncAnimation(
            fig, partial(self.move_ant, ax, True), frames=frames, interval=1
        )
        plt.show()


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    LangtonsAnt(WIDTH, HEIGHT).display()
