"""
用于最大流问题的推送-重标记（Push-Relabel，Goldberg-Tarjan）算法。

推送-重标记方法与本目录中的增广路径算法采用截然不同的思路
（``ford_fulkerson.py`` 每次沿一条路径逐步建立有效流）。它使用*预流*，其中
某个顶点接收的流量可以暂时多于其发送的流量。每个活跃顶点要么将其超额流量
*推送*给低一层的相邻顶点，要么被*重标记*到更高层级，使推送成为可能。当除
源点和汇点外的所有顶点均无超额流量时，预流便成为最大流。

本实现采用最高标号选择规则（始终释放标号最大的活跃顶点），时间复杂度为
O(V^2 * sqrt(E))，在稠密图上优于增广路径方法。

参考资料：https://en.wikipedia.org/wiki/Push%E2%80%93relabel_maximum_flow_algorithm
"""

from __future__ import annotations


class PushRelabel:
    """
    计算具有非负整数容量的有向图中的最大流。

    使用 :meth:`add_edge` 添加边，然后调用 :meth:`max_flow`。

    >>> g = PushRelabel(6)
    >>> capacities = {
    ...     (0, 1): 16, (0, 2): 13, (1, 2): 10, (1, 3): 12,
    ...     (2, 1): 4, (2, 4): 14, (3, 2): 9, (3, 5): 20,
    ...     (4, 3): 7, (4, 5): 4,
    ... }
    >>> for (u, v), cap in capacities.items():
    ...     g.add_edge(u, v, cap)
    >>> g.max_flow(0, 5)
    23

    其结果与经典的四顶点示例一致：

    >>> h = PushRelabel(4)
    >>> for (u, v), cap in {(0, 1): 3, (0, 2): 2, (1, 2): 5,
    ...                     (1, 3): 2, (2, 3): 3}.items():
    ...     h.add_edge(u, v, cap)
    >>> h.max_flow(0, 3)
    5

    平行边的容量会累加，汇点不可达时流量为零：

    >>> p = PushRelabel(2)
    >>> p.add_edge(0, 1, 3)
    >>> p.add_edge(0, 1, 5)
    >>> p.max_flow(0, 1)
    8
    >>> PushRelabel(3).max_flow(0, 2)
    0
    """

    def __init__(self, vertices: int) -> None:
        if vertices <= 0:
            raise ValueError("number of vertices must be positive")
        self.size = vertices
        self.graph: list[list[int]] = [[] for _ in range(vertices)]
        # 每条边存储为 [destination, residual_capacity]
        self.edges: list[list[int]] = []

    def add_edge(self, source: int, destination: int, capacity: int) -> None:
        """
        添加一条容量为给定值的有向边 ``source -> destination``。

        >>> g = PushRelabel(2)
        >>> g.add_edge(0, 1, -1)
        Traceback (most recent call last):
            ...
        ValueError: capacity must be non-negative
        >>> g.add_edge(2, 0, 1)
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

    def max_flow(self, source: int, sink: int) -> int:
        """
        返回从 ``source`` 到 ``sink`` 的最大流。

        >>> PushRelabel(2).max_flow(0, 0)
        Traceback (most recent call last):
            ...
        ValueError: source and sink must be different
        """
        if not (0 <= source < self.size and 0 <= sink < self.size):
            raise ValueError("vertex out of range")
        if source == sink:
            raise ValueError("source and sink must be different")

        height = [0] * self.size
        excess = [0] * self.size
        height[source] = self.size

        # 使源点的每条出边饱和，以创建初始预流
        for edge_index in self.graph[source]:
            destination, residual = self.edges[edge_index]
            if residual > 0:
                self.edges[edge_index][1] -= residual
                self.edges[edge_index ^ 1][1] += residual
                excess[destination] += residual
                excess[source] -= residual

        active = [
            v for v in range(self.size) if v not in (source, sink) and excess[v] > 0
        ]

        while active:
            u = max(active, key=lambda v: height[v])
            if not self._discharge(u, height):
        # 重标记：将 u 提升至比其最低可用相邻顶点高一级
                min_height = min(
                    height[self.edges[i][0]]
                    for i in self.graph[u]
                    if self.edges[i][1] > 0
                )
                height[u] = min_height + 1
            self._apply_pushes(u, height, excess)
            active = [
                v for v in range(self.size) if v not in (source, sink) and excess[v] > 0
            ]

        return excess[sink]

    def _discharge(self, u: int, height: list[int]) -> bool:
        """若 ``u`` 至少有一条可容许出边，则返回 ``True``。"""
        return any(
            self.edges[i][1] > 0 and height[self.edges[i][0]] == height[u] - 1
            for i in self.graph[u]
        )

    def _apply_pushes(self, u: int, height: list[int], excess: list[int]) -> None:
        """沿可容许边尽可能多地推送 ``u`` 的超额流量。"""
        for edge_index in self.graph[u]:
            if excess[u] == 0:
                break
            destination, residual = self.edges[edge_index]
            if residual > 0 and height[u] == height[destination] + 1:
                delta = min(excess[u], residual)
                self.edges[edge_index][1] -= delta
                self.edges[edge_index ^ 1][1] += delta
                excess[u] -= delta
                excess[destination] += delta


if __name__ == "__main__":
    from doctest import testmod

    testmod()
