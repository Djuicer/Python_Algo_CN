"""广度优先搜索最短路径的实现。
doctest:
python -m doctest -v breadth_first_search_shortest_path_2.py
手动测试：
python breadth_first_search_shortest_path_2.py
"""

from collections import deque

demo_graph = {
    "A": ["B", "C", "E"],
    "B": ["A", "D", "E"],
    "C": ["A", "F", "G"],
    "D": ["B"],
    "E": ["A", "B", "D"],
    "F": ["C"],
    "G": ["C"],
}


def bfs_shortest_path(graph: dict, start, goal) -> list[str]:
    """求 `start` 和 `goal` 节点之间的最短路径。
    参数：
        graph (dict)：节点/相邻节点键/值对的列表。
        start：起始节点。
        目标：目标节点。
    返回：
        `start` 和 `goal` 节点之间作为节点链的最短节点。
        如果未找到路径，则返回空列表。
    例子：
        >>> bfs_shortest_path(demo_graph, "G", "D")
        ['G', 'C', 'A', 'B', 'D']
        >>> bfs_shortest_path(demo_graph, "G", "G")
        ['G']
        >>> bfs_shortest_path(demo_graph, "G", "Unknown")
        []
    """
    # 跟踪探索的节点
    explored = set()
    # 跟踪所有要检查的路径
    queue = deque([[start]])

    # 如果起点是目标则返回路径
    if start == goal:
        return [start]

    # 不断循环，直到检查完所有可能的路径
    while queue:
        # 从队列中弹出第一个路径
        path = queue.popleft()
        # 获取路径中的最后一个节点
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            # 遍历所有邻居节点，构建一条新路径
            # 将其推入队列
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # 如果邻居是目标则返回路径
                if neighbour == goal:
                    return new_path

            # 将节点标记为已探索
            explored.add(node)

    # 如果两个节点之间没有路径
    return []


def bfs_shortest_path_distance(graph: dict, start, target) -> int:
    """求 `start` 和 `target` 节点之间的最短路径距离。
    参数：
        图：相邻节点键/值对的节点/列表。
        start：开始搜索的节点。
        target：要搜索的节点。
    返回：
        `start` 和 `target` 节点之间的最短路径中的边数。
        -1 if no path exists.
    例子：
        >>> bfs_shortest_path_distance(demo_graph, "G", "D")
        4
        >>> bfs_shortest_path_distance(demo_graph, "A", "A")
        0
        >>> bfs_shortest_path_distance(demo_graph, "A", "Unknown")
        -1
    """
    if not graph or start not in graph or target not in graph:
        return -1
    if start == target:
        return 0
    queue = deque([start])
    visited = set(start)
    # 密切关注与`start` 节点的距离。
    dist = {start: 0, target: -1}
    while queue:
        node = queue.popleft()
        if node == target:
            dist[target] = (
                dist[node] if dist[target] == -1 else min(dist[target], dist[node])
            )
        for adjacent in graph[node]:
            if adjacent not in visited:
                visited.add(adjacent)
                queue.append(adjacent)
                dist[adjacent] = dist[node] + 1
    return dist[target]


if __name__ == "__main__":
    print(bfs_shortest_path(demo_graph, "G", "D"))  # 返回 ['G', 'C', 'A', 'B', 'D']
    print(bfs_shortest_path_distance(demo_graph, "G", "D"))  # 返回 4
