import math


class Graph:
    def __init__(self, n=0) -> None:  # 包含节点 0,1,...,N-1 的图
        self.n = n
        self.w = [
            [math.inf for j in range(n)] for i in range(n)
        ]  # 权重的邻接矩阵
        self.dp = [
            [math.inf for j in range(n)] for i in range(n)
        ]  # dp[i][j] 存储从 i 到 j 的最短距离

    def add_edge(self, u, v, w) -> None:
        """
        添加一条从节点 u 到节点 v、权重为 w 的有向边。

        >>> g = Graph(3)
        >>> g.add_edge(0, 1, 5)
        >>> g.dp[0][1]
        5
        """
        self.dp[u][v] = w

    def floyd_warshall(self) -> None:
        """
        使用 Floyd-Warshall 算法计算所有节点对之间的最短路径。

        >>> g = Graph(3)
        >>> g.add_edge(0, 1, 1)
        >>> g.add_edge(1, 2, 2)
        >>> g.floyd_warshall()
        >>> g.show_min(0, 2)
        3
        >>> g.show_min(2, 0)
        inf
        """
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    self.dp[i][j] = min(self.dp[i][j], self.dp[i][k] + self.dp[k][j])

    def show_min(self, u, v):
        """
        返回从节点 u 到节点 v 的最短距离。

        >>> g = Graph(3)
        >>> g.add_edge(0, 1, 3)
        >>> g.add_edge(1, 2, 4)
        >>> g.floyd_warshall()
        >>> g.show_min(0, 2)
        7
        >>> g.show_min(1, 0)
        inf
        """
        return self.dp[u][v]


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 使用示例
    graph = Graph(5)
    graph.add_edge(0, 2, 9)
    graph.add_edge(0, 4, 10)
    graph.add_edge(1, 3, 5)
    graph.add_edge(2, 3, 7)
    graph.add_edge(3, 0, 10)
    graph.add_edge(3, 1, 2)
    graph.add_edge(3, 2, 1)
    graph.add_edge(3, 4, 6)
    graph.add_edge(4, 1, 3)
    graph.add_edge(4, 2, 4)
    graph.add_edge(4, 3, 9)
    graph.floyd_warshall()
    print(
        graph.show_min(1, 4)
    )  # 应输出从节点 1 到节点 4 的最短距离
    print(
        graph.show_min(0, 3)
    )  # 应输出从节点 0 到节点 3 的最短距离
