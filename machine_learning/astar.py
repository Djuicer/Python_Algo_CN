"""
A* 算法结合了一致代价搜索与纯启发式搜索的特点，能够高效地计算最优解。

A* 是一种最佳优先搜索算法，节点的代价为 f(n) = g(n) + h(n)，其中 g(n)
是从初始状态到节点 n 的路径代价，h(n) 是从节点 n 到目标的启发式估计代价。

A* 算法在常规图搜索算法中引入启发式信息，相当于在每一步进行预先规划，
从而作出更优的决策。因此，A* 也被称为“有智慧的算法”。

https://en.wikipedia.org/wiki/A*_search_algorithm
"""

import numpy as np


class Cell:
    """
    Cell 类表示网格世界中的一个单元格，具有以下属性：
    position：由 x、y 坐标组成的元组表示，初始值为 (0,0)。
    parent：到达此单元格之前访问的父单元格对象。
    g, h, f：调用启发式函数时使用的参数。
    """

    def __init__(self) -> None:
        self.position = (0, 0)
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    """
    Overrides equals method because otherwise cell assign will give
    wrong results.
    """

    def __eq__(self, cell):
        return self.position == cell.position

    def showcell(self) -> None:
        print(self.position)


class Gridworld:
    """
    Gridworld 类以 M*M 网格矩阵表示外部世界。
    world_size：按给定的 world_size 创建 NumPy 数组，默认值为 5。
    """

    def __init__(self, world_size=(5, 5)) -> None:
        self.w = np.zeros(world_size)
        self.world_x_limit = world_size[0]
        self.world_y_limit = world_size[1]

    def show(self) -> None:
        print(self.w)

    def get_neighbours(self, cell):
        """
        返回单元格的相邻单元格
        """
        neughbour_cord = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        current_x = cell.position[0]
        current_y = cell.position[1]
        neighbours = []
        for n in neughbour_cord:
            x = current_x + n[0]
            y = current_y + n[1]
            if 0 <= x < self.world_x_limit and 0 <= y < self.world_y_limit:
                c = Cell()
                c.position = (x, y)
                c.parent = cell
                neighbours.append(c)
        return neighbours


def astar(world, start, goal):
    """
    A* 算法的实现。
    world：网格世界对象。
    start：作为起始位置的单元格对象。
    stop：作为目标位置的单元格对象。

    >>> p = Gridworld()
    >>> start = Cell()
    >>> start.position = (0,0)
    >>> goal = Cell()
    >>> goal.position = (4,4)
    >>> astar(p, start, goal)
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    """
    _open = []
    _closed = []
    _open.append(start)

    while _open:
        min_f = np.argmin([n.f for n in _open])
        current = _open[min_f]
        _closed.append(_open.pop(min_f))
        if current == goal:
            break
        for n in world.get_neighbours(current):
            for c in _closed:
                if c == n:
                    continue
            n.g = current.g + 1
            x1, y1 = n.position
            x2, y2 = goal.position
            n.h = (y2 - y1) ** 2 + (x2 - x1) ** 2
            n.f = n.h + n.g

            for c in _open:
                if c == n and c.f < n.f:
                    continue
            _open.append(n)
    path = []
    while current.parent is not None:
        path.append(current.position)
        current = current.parent
    path.append(current.position)
    return path[::-1]


if __name__ == "__main__":
    world = Gridworld()
    # 起始位置和目标位置
    start = Cell()
    start.position = (0, 0)
    goal = Cell()
    goal.position = (4, 4)
    print(f"path from {start.position} to {goal.position}")
    s = astar(world, start, goal)
    # 仅用于可视化。
    for i in s:
        world.w[i] = 1
    print(world.w)
