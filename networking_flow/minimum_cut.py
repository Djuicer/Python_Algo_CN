"""
使用 Ford-Fulkerson 算法求流网络的最小割。

最大流最小割定理指出，从源点到汇点的最大流值等于最小 s-t 割中各边的容量
总和；最小 s-t 割是移除后能断开汇点与源点的最小代价边集。本模块通过运行
Ford-Fulkerson 构建残量图来寻找这些割边，然后报告原图中从源点仍可达顶点
指向不可达顶点的所有边。

参考资料：https://en.wikipedia.org/wiki/Minimum_cut
另请参阅：https://en.wikipedia.org/wiki/Max-flow_min-cut_theorem
"""

test_graph = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0],
]


def bfs(graph: list[list[int]], source: int, sink: int, parent: list[int]) -> bool:
    """
    若在残量 ``graph`` 中从 ``source`` 可以到达 ``sink``，则返回 True，
    并在 ``parent`` 中记录遍历树。

    >>> bfs(test_graph, 0, 5, [-1] * 6)
    True
    >>> bfs([[0, 0], [0, 0]], 0, 1, [-1, -1])
    False
    """
    visited = [False] * len(graph)
    queue = [source]
    visited[source] = True

    while queue:
        node = queue.pop(0)
        for neighbor in range(len(graph[node])):
            if visited[neighbor] is False and graph[node][neighbor] > 0:
                queue.append(neighbor)
                visited[neighbor] = True
                parent[neighbor] = node

    return visited[sink]


def mincut(graph: list[list[int]], source: int, sink: int) -> list[tuple[int, int]]:
    """
    以 ``(from, to)`` 元组形式返回最小 s-t 割的边。

    输入 ``graph`` 是容量邻接矩阵，并保持不变（算法在内部副本上运行）。

    >>> mincut(test_graph, source=0, sink=5)
    [(1, 3), (4, 3), (4, 5)]

    割边的容量之和等于最大流（此处为 23）：

    >>> sum(test_graph[u][v] for u, v in mincut(test_graph, 0, 5))
    23

    单条饱和边自身即构成最小割：

    >>> mincut([[0, 7], [0, 0]], source=0, sink=1)
    [(0, 1)]
    """
    residual = [row[:] for row in graph]  # 在副本上操作，保持输入不变
    parent = [-1] * (len(residual))
    res = []
    while bfs(residual, source, sink, parent):
        path_flow = max(max(row) for row in residual)
        s = sink

        while s != source:
            # 寻找增广路径上的最小剩余容量
            path_flow = min(path_flow, residual[parent[s]][s])
            s = parent[s]

        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = parent[v]

    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] > 0 and residual[i][j] == 0:
                res.append((i, j))

    return res


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    print(mincut(test_graph, source=0, sink=5))
