from __future__ import annotations

DIRECTIONS = [
    [-1, 0],  # 左
    [0, -1],  # 下
    [1, 0],  # 右
    [0, 1],  # 上
]


# 搜索路径的函数
def search(
    grid: list[list[int]],
    init: list[int],
    goal: list[int],
    cost: int,
    heuristic: list[list[int]],
) -> tuple[list[list[int]], list[list[int]]]:
    """
    在网格中搜索一条避开障碍物的路径。
    >>> grid = [[0, 1, 0, 0, 0, 0],
    ...         [0, 1, 0, 0, 0, 0],
    ...         [0, 1, 0, 0, 0, 0],
    ...         [0, 1, 0, 0, 1, 0],
    ...         [0, 0, 0, 0, 1, 0]]
    >>> init = [0, 0]
    >>> goal = [len(grid) - 1, len(grid[0]) - 1]
    >>> cost = 1
    >>> heuristic = [[0] * len(grid[0]) for _ in range(len(grid))]
    >>> heuristic = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    >>> for i in range(len(grid)):
    ...     for j in range(len(grid[0])):
    ...         heuristic[i][j] = abs(i - goal[0]) + abs(j - goal[1])
    ...         if grid[i][j] == 1:
    ...             heuristic[i][j] = 99
    >>> path, action = search(grid, init, goal, cost, heuristic)
    >>> path  # doctest: +NORMALIZE_WHITESPACE
    [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [4, 1], [4, 2], [4, 3], [3, 3],
    [2, 3], [2, 4], [2, 5], [3, 5], [4, 5]]
    >>> action  # doctest: +NORMALIZE_WHITESPACE
    [[0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 3, 3],
    [2, 0, 0, 0, 0, 2], [2, 3, 3, 3, 0, 2]]
    """
    closed = [
        [0 for col in range(len(grid[0]))] for row in range(len(grid))
    ]  # 参考网格
    closed[init[0]][init[1]] = 1
    action = [
        [0 for col in range(len(grid[0]))] for row in range(len(grid))
    ]  # 动作网格

    x = init[0]
    y = init[1]
    g = 0
    f = g + heuristic[x][y]  # 从起始单元格到目标单元格的代价
    cell = [[f, g, x, y]]

    found = False  # 搜索完成时设置的标志
    resign = False  # 无法找到可扩展节点时设置的标志

    while not found and not resign:
        if len(cell) == 0:
            raise ValueError("Algorithm is unable to find solution")
        # 选择代价最小的动作，以便向目标靠近
        cell.sort()
        cell.reverse()
        next_cell = cell.pop()
        x = next_cell[2]
        y = next_cell[3]
        g = next_cell[1]

        if x == goal[0] and y == goal[1]:
            found = True
        else:
            for i in range(len(DIRECTIONS)):  # 尝试不同的有效动作
                x2 = x + DIRECTIONS[i][0]
                y2 = y + DIRECTIONS[i][1]
                if (
                    x2 >= 0
                    and x2 < len(grid)
                    and y2 >= 0
                    and y2 < len(grid[0])
                    and closed[x2][y2] == 0
                    and grid[x2][y2] == 0
                ):
                    g2 = g + cost
                    f2 = g2 + heuristic[x2][y2]
                    cell.append([f2, g2, x2, y2])
                    closed[x2][y2] = 1
                    action[x2][y2] = i
    invpath = []
    x = goal[0]
    y = goal[1]
    invpath.append([x, y])  # 从这里得到反向路径
    while x != init[0] or y != init[1]:
        x2 = x - DIRECTIONS[action[x][y]][0]
        y2 = y - DIRECTIONS[action[x][y]][1]
        x = x2
        y = y2
        invpath.append([x, y])

    path = []
    for i in range(len(invpath)):
        path.append(invpath[len(invpath) - 1 - i])
    return path, action


if __name__ == "__main__":
    grid = [
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],  # 0 表示可通行路径，1 表示障碍物
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
    ]

    init = [0, 0]
    # 所有坐标均采用 [y,x] 格式
    goal = [len(grid) - 1, len(grid[0]) - 1]
    cost = 1

    # 促使路径靠近目标的代价图
    heuristic = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            heuristic[i][j] = abs(i - goal[0]) + abs(j - goal[1])
            if grid[i][j] == 1:
                # 在启发式图中加入额外惩罚
                heuristic[i][j] = 99

    path, action = search(grid, init, goal, cost, heuristic)

    print("ACTION MAP")
    for i in range(len(action)):
        print(action[i])

    for i in range(len(path)):
        print(path[i])
