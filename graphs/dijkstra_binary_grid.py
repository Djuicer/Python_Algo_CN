"""
该脚本在二进制网络上实现 Dijkstra 算法。
网格由0和1组成，其中1代表
一个可步行的节点，0代表一个障碍物。
该算法找到从起始节点到目标节点的最短路径。
可以允许或不允许对角线移动。
"""

from heapq import heappop, heappush

import numpy as np


def dijkstra(
    grid: np.ndarray,
    source: tuple[int, int],
    destination: tuple[int, int],
    allow_diagonal: bool,
) -> tuple[float | int, list[tuple[int, int]]]:
    """
    在二进制网格上实现 Dijkstra 算法。

    参数：
        grid (np.ndarray)：表示网格的2D numpy 阵列。
        1 represents a walkable node and 0 represents an obstacle.
        source (Tuple[int, int])：表示起始节点的元组。
        目的地 (Tuple[int, int])：表示目的地的元组
        目的节点。
        allow_diagonal (bool): 一个布尔值，确定是否
        允许对角线移动。

    返回：
        元组[联合[float, int],列表[元组[int, int]]]：
        起始节点到目的节点的最短距离
        以及作为节点列表的最短路径。

    >>> dijkstra(np.array([[1, 1, 1], [0, 1, 0], [0, 1, 1]]), (0, 0), (2, 2), False)
    (4.0, [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)])

    >>> dijkstra(np.array([[1, 1, 1], [0, 1, 0], [0, 1, 1]]), (0, 0), (2, 2), True)
    (2.0, [(0, 0), (1, 1), (2, 2)])

    >>> dijkstra(np.array([[1, 1, 1], [0, 0, 1], [0, 1, 1]]), (0, 0), (2, 2), False)
    (4.0, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)])
    """
    rows, cols = grid.shape
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    if allow_diagonal:
        dx += [-1, -1, 1, 1]
        dy += [-1, 1, -1, 1]

    queue, visited = [(0, source)], set()
    matrix = np.full((rows, cols), np.inf)
    matrix[source] = 0
    predecessors = np.empty((rows, cols), dtype=object)
    predecessors[source] = None

    while queue:
        (dist, (x, y)) = heappop(queue)
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) == destination:
            path = []
            while (x, y) != source:
                path.append((x, y))
                x, y = predecessors[x, y]
            path.append(source)  # 手动添加源
            path.reverse()
            return float(matrix[destination]), path

        for i in range(len(dx)):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < rows and 0 <= ny < cols:
                next_node = grid[nx][ny]
                if next_node == 1 and matrix[nx, ny] > dist + 1:
                    heappush(queue, (dist + 1, (nx, ny)))
                    matrix[nx, ny] = dist + 1
                    predecessors[nx, ny] = (x, y)

    return np.inf, []


if __name__ == "__main__":
    import doctest

    doctest.testmod()
