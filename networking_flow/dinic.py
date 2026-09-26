"""
用于最大流问题的 Dinic 算法。

Dinic 算法反复使用广度优先搜索构建*层次图*（按边数度量的最短增广路径），
然后使用深度优先搜索，在一次遍历中使该层次图上的*阻塞流*饱和。通过这种方式
按长度对增广路径分组，其最坏情况性能远优于普通的 Ford-Fulkerson / Edmonds-Karp
增广路径方法：

* Dinic 算法：                 O(V^2 * E)
* 单位容量网络：               O(E * sqrt(V))

与本目录中 ``ford_fulkerson.py`` 和 ``minimum_cut.py`` 的邻接矩阵实现不同，
本版本将图存储为残量边的邻接表，因此也能处理包含平行边的图，并且在稀疏图上
效率较高。

参考资料：https://en.wikipedia.org/wiki/Dinic%27s_algorithm
"""

from collections import deque


class Dinic:
    """
    计算具有非负整数容量的有向图中的最大流。

    使用 :meth:`add_edge` 添加边，然后调用 :meth:`max_flow`。

    >>> g = Dinic(6)
    >>> capacities = {
    ...     (0, 1): 16, (0, 2): 13, (1, 2): 10, (1, 3): 12,
    ...     (2, 1): 4, (2, 4): 14, (3, 2): 9, (3, 5): 20,
    ...     (4, 3): 7, (4, 5): 4,
    ... }
    >>> for (u, v), cap in capacities.items():
    ...     g.add_edge(u, v, cap)
    >>> g.max_flow(0, 5)
    23

    没有出边的源点（或没有入边的汇点）的最大流为零：

    >>> Dinic(3).max_flow(0, 2)
    0

    支持同一对顶点间的平行边，其容量会累加：

    >>> h = Dinic(2)
    >>> h.add_edge(0, 1, 3)
    >>> h.add_edge(0, 1, 5)
    >>> h.max_flow(0, 1)
    8
    """

    def __init__(self, vertices: int) -> None:
        if vertices <= 0:
            raise ValueError("number of vertices must be positive")
        self.size = vertices
        # graph[vertex] 存储该顶点出边在 self.edges 中的索引
        self.graph: list[list[int]] = [[] for _ in range(vertices)]
        # 每条边存储为 [destination, residual_capacity]
        # 边 i 与其反向边 i ^ 1 始终成对创建
        self.edges: list[list[int]] = []

    def add_edge(self, source: int, destination: int, capacity: int) -> None:
        """
        添加一条容量为给定值的有向边 ``source -> destination``。

        >>> g = Dinic(2)
        >>> g.add_edge(0, 1, 5)
        >>> g.add_edge(0, 1, -1)
        Traceback (most recent call last):
            ...
        ValueError: capacity must be non-negative
        >>> g.add_edge(0, 2, 5)
        Traceback (most recent call last):
            ...
        ValueError: vertex out of range
        """
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        if not (0 <= source < self.size and 0 <= destination < self.size):
            raise ValueError("vertex out of range")
        self.graph[source].append(len(self.edges))
        self.edges.append([destination, capacity])
        self.graph[destination].append(len(self.edges))
        self.edges.append([source, 0])  # 反向边初始为饱和状态

    def _build_level_graph(self, source: int) -> list[int]:
        """执行广度优先搜索；返回各顶点的层级（不可达时为 -1）。"""
        level = [-1] * self.size
        level[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for edge_index in self.graph[vertex]:
                destination, residual = self.edges[edge_index]
                if residual > 0 and level[destination] == -1:
                    level[destination] = level[vertex] + 1
                    queue.append(destination)
        return level

    def _send_flow(
        self,
        vertex: int,
        pushed: int,
        sink: int,
        level: list[int],
        progress: list[int],
    ) -> int:
        """沿层次图推送阻塞流的深度优先搜索。"""
        if vertex == sink:
            return pushed
        while progress[vertex] < len(self.graph[vertex]):
            edge_index = self.graph[vertex][progress[vertex]]
            destination, residual = self.edges[edge_index]
            if residual > 0 and level[destination] == level[vertex] + 1:
                flow = self._send_flow(
                    destination, min(pushed, residual), sink, level, progress
                )
                if flow > 0:
                    self.edges[edge_index][1] -= flow
                    self.edges[edge_index ^ 1][1] += flow
                    return flow
            progress[vertex] += 1
        return 0

    def max_flow(self, source: int, sink: int) -> int:
        """
        返回从 ``source`` 到 ``sink`` 的最大流。

        >>> g = Dinic(4)
        >>> for (u, v), cap in {(0, 1): 3, (0, 2): 2, (1, 2): 5,
        ...                     (1, 3): 2, (2, 3): 3}.items():
        ...     g.add_edge(u, v, cap)
        >>> g.max_flow(0, 3)
        5
        >>> g.max_flow(0, 0)
        Traceback (most recent call last):
            ...
        ValueError: source and sink must be different
        """
        if not (0 <= source < self.size and 0 <= sink < self.size):
            raise ValueError("vertex out of range")
        if source == sink:
            raise ValueError("source and sink must be different")
        infinity = sum(capacity for _, capacity in self.edges) + 1
        flow = 0
        level = self._build_level_graph(source)
        while level[sink] != -1:
            progress = [0] * self.size
            while True:
                pushed = self._send_flow(source, infinity, sink, level, progress)
                if pushed == 0:
                    break
                flow += pushed
            level = self._build_level_graph(source)
        return flow


if __name__ == "__main__":
    from doctest import testmod

    testmod()
