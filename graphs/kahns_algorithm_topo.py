from collections import deque


def topological_sort(graph: dict[int, list[int]]) -> list[int] | None:
    """
    对有向无环图(DAG)进行拓扑排序
    通过广度优先搜索（BFS）使用卡恩算法。

    拓扑排序是图中顶点的线性排序，使得对于
    每个都有向边 u → v，顶点 u 在排序中位于顶点 v 之前。

    参数：
    graph：邻接表，表示键所在的有向图
           顶点，值是相邻顶点的列表。

    返回：
    如果图是DAG，则顶点的拓扑排序顺序。
    如果图包含循环，则返回 None。

    例子：
    >>> graph = {0: [1, 2], 1: [3], 2: [3], 3: [4, 5], 4: [], 5: []}
    >>> topological_sort(graph)
    [0, 1, 2, 3, 4, 5]

    >>> graph_with_cycle = {0: [1], 1: [2], 2: [0]}
    >>> topological_sort(graph_with_cycle)

    >>> sparse_graph = {10: [20], 20: []}
    >>> topological_sort(sparse_graph)
    [10, 20]

    >>> sparse_cycle = {10: [20], 20: [10]}
    >>> topological_sort(sparse_cycle)
    """

    indegree = dict.fromkeys(graph, 0)
    queue: deque[int] = deque()
    topo_order = []
    processed_vertices_count = 0

    # 计算每个顶点的入度
    for values in graph.values():
        for i in values:
            indegree[i] += 1

    # 将所有入度为 0 的顶点添加到队列中
    for vertex, count in indegree.items():
        if count == 0:
            queue.append(vertex)

    # 执行广度优先搜索
    while queue:
        vertex = queue.popleft()
        processed_vertices_count += 1
        topo_order.append(vertex)

        # 遍历邻居
        for neighbor in graph[vertex]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if processed_vertices_count != len(graph):
        return None  # 由于环路，不存在拓扑排序
    return topo_order  # 有效的拓扑排序


if __name__ == "__main__":
    import doctest

    doctest.testmod()
