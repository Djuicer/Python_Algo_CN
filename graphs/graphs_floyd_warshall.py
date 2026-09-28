# floyd_warshall.py
"""
问题是找到一个中所有边对之间的最短距离
可以具有负边权重的加权有向图。
"""


def _print_dist(dist, v) -> None:
    print("\nThe shortest path matrix using Floyd Warshall algorithm\n")
    for i in range(v):
        for j in range(v):
            end_char = "" if j == v - 1 else "  "
            if dist[i][j] != float("inf"):
                print(int(dist[i][j]), end=end_char)
            else:
                print("INF", end=end_char)
        print()


def floyd_warshall(graph, v):
    """
    :param graph: 根据权重[edge[i, j]]计算的二维数组
    ：类型图：列表[列表[浮点]]
    :param v: 顶点数
    ：类型 v：int
    :return: 所有边对之间的最短距离
    distance[u][v] 将包含从顶点 u 到 v 的最短距离。

    1. For all edges from v to n, distance[i][j] = weight(edge(i, j)).
    3. The algorithm then performs distance[i][j] = min(distance[i][j], distance[i][k] +
        distance[k][j]) 对于每个可能的顶点对 i, j 。
    4. The above is repeated for each vertex k in the graph.
    5. Whenever distance[i][j] is given a new minimum value, next vertex[i][j] is
        更新到下一个顶点[i][k]。


    >>> graph = [
    ...     [0, 3, float('inf')],
    ...     [2, 0, float('inf')],
    ...     [float('inf'), 7, 0]
    ... ]

    >>> expected = [
    ...     [0, 3, float('inf')],
    ...     [2, 0, float('inf')],
    ...     [9, 7, 0]
    ... ]
    >>> dist, _ = floyd_warshall(graph, 3)
    <BLANKLINE>
    The shortest path matrix using Floyd Warshall algorithm
    <BLANKLINE>
    0  3  INF
    2  0  INF
    9  7  0
    >>> dist == expected
    True
    """

    dist = [[float("inf") for _ in range(v)] for _ in range(v)]

    for i in range(v):
        for j in range(v):
            dist[i][j] = graph[i][j]

            # 检查顶点 k 与所有其他顶点 (i, j)
    for k in range(v):
        # 循环遍历图数组的行
        for i in range(v):
            # 循环遍历图数组的列
            for j in range(v):
                if (
                    dist[i][k] != float("inf")
                    and dist[k][j] != float("inf")
                    and dist[i][k] + dist[k][j] < dist[i][j]
                ):
                    dist[i][j] = dist[i][k] + dist[k][j]

    _print_dist(dist, v)
    return dist, v


if __name__ == "__main__":
    v = int(input("Enter number of vertices: "))
    e = int(input("Enter number of edges: "))

    graph = [[float("inf") for i in range(v)] for j in range(v)]

    for i in range(v):
        graph[i][i] = 0.0

        # src 和 dst 必须安装数组大小 graph[e][v] 内的索引
        # 不遵循此操作将导致错误
    for i in range(e):
        print("\nEdge ", i + 1)
        src = int(input("Enter source:"))
        dst = int(input("Enter destination:"))
        weight = float(input("Enter weight:"))
        graph[src][dst] = weight

    floyd_warshall(graph, v)

    # 输入示例
    # 输入顶点数：3
    # 输入边数：2

    # # 从顶点和边输入生成图
    # [[inf, inf, inf], [inf, inf, inf], [inf, inf, inf]]
    # [[0.0, inf, inf], [inf, 0.0, inf], [inf, inf, 0.0]]

    # 指定边 #1 的源、目的地和权重
    # 边1
    # 输入来源：1
    # 输入目的地：2
    # 输入重量：2

    # 指定边 #2 的源、目的地和权重
    # 边2
    # 输入来源：2
    # 输入目的地：1
    # 输入重量：1

    # # 顶点、边和src、dst、权重输入的预期！！
    # 0		INF	INF
    # 中核因子 0 2
    # 中核因子 1 0
