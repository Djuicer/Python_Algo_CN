"""
用于最大流问题的 Ford-Fulkerson 算法
* https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm

说明：
    (1) 从初始流量 0 开始
    (2) 选择从源点到汇点的增广路径，并将该路径加入流
"""

graph = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0],
]


def breadth_first_search(graph: list, source: int, sink: int, parents: list) -> bool:
    """
    若存在尚未遍历的节点，则返回 True。

    参数：
        graph: 图的邻接矩阵
        source: 源点
        sink: 汇点
        parents: 父节点列表

    返回：
        若存在从 source 到 sink 的路径，则返回 True

    >>> breadth_first_search(graph, 0, 5, [-1, -1, -1, -1, -1, -1])
    True
    """
    num_nodes = len(graph)
    visited = [False] * num_nodes
    queue = []  # 使用 list 代替 deque

    queue.append(source)
    visited[source] = True

    while queue:
        # 使用 pop(0) 模拟 deque 的 popleft()
        current_node = queue.pop(0)

        # 若已到达汇点，则可提前停止
        if current_node == sink:
            return True

        # 检查所有相邻节点
        for neighbor, capacity in enumerate(graph[current_node]):
            if not visited[neighbor] and capacity > 0:
                visited[neighbor] = True
                parents[neighbor] = current_node
                queue.append(neighbor)

    return visited[sink]


def ford_fulkerson(graph: list, source: int, sink: int) -> int:
    """
    返回给定图中从源点到汇点的最大流。

    注意：本函数会修改给定的图。

    参数：
        graph: 图的邻接矩阵
        source: 源点
        sink: 汇点

    返回：
        最大流

    >>> test_graph = [
    ...     [0, 16, 13, 0, 0, 0],
    ...     [0, 0, 10, 12, 0, 0],
    ...     [0, 4, 0, 0, 14, 0],
    ...     [0, 0, 9, 0, 0, 20],
    ...     [0, 0, 0, 7, 0, 4],
    ...     [0, 0, 0, 0, 0, 0],
    ... ]
    >>> ford_fulkerson(test_graph, 0, 5)
    23
    """
    # 创建图的副本，以免修改原图
    residual_graph = [row[:] for row in graph]
    num_nodes = len(residual_graph)
    parents = [-1] * num_nodes
    max_flow = 0

    # 只要存在从源点到汇点的路径，就持续增广流
    while breadth_first_search(residual_graph, source, sink, parents):
        # 寻找路径上的最小剩余容量
        path_flow = float("inf")
        current_node = sink

        # 寻找路径中的最小容量
        while current_node != source:
            parent_node = parents[current_node]
            path_flow = min(path_flow, residual_graph[parent_node][current_node])
            current_node = parent_node

        # 将路径流量加入总流量
        max_flow += path_flow

        # 更新边及其反向边的剩余容量
        current_node = sink
        while current_node != source:
            parent_node = parents[current_node]
            residual_graph[parent_node][current_node] -= path_flow
            residual_graph[current_node][parent_node] += path_flow
            current_node = parent_node

    return max_flow


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    print(f"{ford_fulkerson(graph, source=0, sink=5) = }")
