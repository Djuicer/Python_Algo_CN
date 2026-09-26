"""Conway's Game Of Life, Author Anurag Kumar(mailto:anuragkumarak95@gmail.com)

依赖：
  - numpy
  - random
  - time
  - matplotlib

Python 版本：
  - 3.5

用法：
  - $python3 game_of_life <canvas_size:int>

生命游戏规则：

 1.
 任何活细胞的活邻居少于两个时，因数量不足而死亡。
 2.
 任何具有两个或三个活邻居的活细胞都会存活到下一代。
 3.
 任何活细胞的活邻居超过三个时，因数量过多而死亡。
 4.
 任何恰好具有三个活邻居的死细胞都会变成活细胞，如同繁殖一般。
"""

import random
import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

usage_doc = "Usage of script: script_name <size_of_canvas:int>"

choice = [0] * 100 + [1] * 10
random.shuffle(choice)


def create_canvas(size: int) -> list[list[bool]]:
    """
    创建给定大小、以 False（死细胞）填充的正方形画布。

    参数：
        size: 正方形画布的边长

    返回：
        大小为 size x size 的二维布尔值列表，所有值均初始化为 False

    >>> canvas = create_canvas(3)
    >>> len(canvas)
    3
    >>> len(canvas[0])
    3
    >>> all(all(not cell for cell in row) for row in canvas)
    True
    >>> create_canvas(1)
    [[False]]
    >>> create_canvas(0)
    []
    """
    canvas = [[False for i in range(size)] for j in range(size)]
    return canvas


def seed(canvas: list[list[bool]]) -> None:
    for i, row in enumerate(canvas):
        for j, _ in enumerate(row):
            canvas[i][j] = bool(random.getrandbits(1))


def run(canvas: list[list[bool]]) -> list[list[bool]]:
    """
    在画布上运行一代康威生命游戏。

    同时对所有细胞应用生命游戏规则，生成下一代。

    参数：
        canvas: 表示细胞当前状态的二维列表

    返回：
        表示下一代状态的二维列表

    >>> blinker = [[False, False, False, False, False],
    ...            [False, False, True, False, False],
    ...            [False, False, True, False, False],
    ...            [False, False, True, False, False],
    ...            [False, False, False, False, False]]
    >>> result = run(blinker)
    >>> result[2]
    [False, True, True, True, False]
    >>> run([[False, False, False], [False, False, False], [False, False, False]])
    [[False, False, False], [False, False, False], [False, False, False]]
    >>> block = [[False, False, False, False],
    ...          [False, True, True, False],
    ...          [False, True, True, False],
    ...          [False, False, False, False]]
    >>> run(block)[1]
    [False, True, True, False]
    """
    current_canvas = np.array(canvas)
    next_gen_canvas = np.array(create_canvas(current_canvas.shape[0]))
    for r, row in enumerate(current_canvas):
        for c, pt in enumerate(row):
            next_gen_canvas[r][c] = __judge_point(
                pt, current_canvas[r - 1 : r + 2, c - 1 : c + 2]
            )

    return next_gen_canvas.tolist()


def __judge_point(pt: bool, neighbours: list[list[bool]]) -> bool:
    """
    应用康威生命游戏规则，确定细胞的下一状态。

    参数：
        pt: 细胞的当前状态（True=存活，False=死亡）
        neighbours: 包含该细胞及其 8 个邻居的 3x3 网格

    返回：
        细胞的下一状态

    规则：
        1. 活邻居少于 2 个的活细胞死亡（数量不足）
        2. 活邻居为 2 至 3 个的活细胞存活
        3. 活邻居多于 3 个的活细胞死亡（数量过多）
        4. 恰好有 3 个活邻居的死细胞变为活细胞

    >>> __judge_point(
    ...     True, [[True, True, False], [False, True, False], [False, False, False]]
    ... )
    True
    >>> __judge_point(
    ...     True, [[True, False, False], [False, True, False], [False, False, False]]
    ... )
    False
    >>> __judge_point(
    ...     True, [[True, True, True], [True, True, False], [False, False, False]]
    ... )
    False
    >>> __judge_point(
    ...     False, [[True, True, False], [True, False, False], [False, False, False]]
    ... )
    True
    >>> __judge_point(
    ...     False, [[True, False, False], [False, False, False], [False, False, False]]
    ... )
    False
    """
    dead = 0
    alive = 0
    # 统计死亡或存活的邻居数量。
    for i in neighbours:
        for status in i:
            if status:
                alive += 1
            else:
                dead += 1

    # 处理目标细胞 pt 的重复计数。
    if pt:
        alive -= 1
    else:
        dead -= 1

    # 在此应用生命游戏规则。
    state = pt
    if pt:
        if alive < 2:
            state = False
        elif alive in {2, 3}:
            state = True
        elif alive > 3:
            state = False
    elif alive == 3:
        state = True

    return state


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception(usage_doc)

    canvas_size = int(sys.argv[1])
    # 本模块的主要运行结构。
    c = create_canvas(canvas_size)
    seed(c)
    fig, ax = plt.subplots()
    fig.show()
    cmap = ListedColormap(["w", "k"])
    try:
        while True:
            c = run(c)
            ax.matshow(c, cmap=cmap)
            fig.canvas.draw()
            ax.cla()
    except KeyboardInterrupt:
        # 不执行任何操作。
        pass
