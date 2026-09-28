"""Hopcroft-Karp 算法用于在二分图中查找最大基数匹配。

Reference:
    https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm

Hopcroft-Karp 算法能以 O(|E| * sqrt(|V|)) 的时间复杂度，找出无权
二分图中的最大基数匹配。

主要概念和条件：
1. 二分条件：
   若图 G = (U union V, E) 的顶点可以划分为两个不相交的集合 U（左部）
   和 V（右部），且每条边均连接 U 与 V 中的顶点，则该图是二分图。
   同一部分内部不能存在边，且顶点不能为 None。

2. 匹配条件：
   匹配 M 是边的子集，使得没有两条边共享公共顶点。
   如果一个顶点不与 M 中的任何边相交，则该顶点是“自由”（不匹配）的。

3. 交替路径与增广路径：
   - 交替路径：边在非匹配边（不在 M 中）与匹配边（在 M 中）之间交替的路径。
   - 增广路径：起点和终点是不同自由顶点的交替路径。
   - Berge 引理：当且仅当不存在增广路径时，匹配具有最大基数。

4. Hopcroft-Karp 分层与增广条件：
   Hopcroft-Karp 不会逐一搜索增广路径，而是分阶段运行：
   - BFS 阶段（分层）：同时从 U 中的所有自由顶点开始搜索，以找出最短
     增广路径的长度，并构建交替层次的分层 DAG。若无法到达 V 中的自由
     顶点，算法终止。
   - DFS 阶段（增广）：找出一组数量最多、顶点互不相交且长度为 BFS 所得
     最短长度的增广路径。它只遍历满足以下条件的边：
     distance_map[matched_left] == distance_map[curr_left] + 1。
   - 对称差：翻转每条增广路径上的匹配状态（非匹配变为匹配，匹配变为非匹配）。
   - 迭代 DFS：DFS 阶段使用显式栈迭代实现，避免交替路径直径较大时出现
     RecursionError。

复杂度：
    时间复杂度：O(|E| * sqrt(|V|))
    空间复杂度：O(|V| + |E|)
"""

from __future__ import annotations

import math
from collections import deque

_NIL = object()


class HopcroftKarp[T]:
    """实现 Hopcroft-Karp 最大二分匹配算法的类。

    >>> hk = HopcroftKarp({"u1": ["v1", "v2"], "u2": ["v1"], "u3": ["v2", "v3"]})
    >>> hk.maximum_matching()
    {'u1': 'v2', 'u2': 'v1', 'u3': 'v3'}
    """

    def __init__(self, graph: dict[T, list[T]]) -> None:
        """初始化二分分区并匹配配对字典。

        异常：
            ValueError: If partitions overlap or if any vertex is None.

        >>> hk = HopcroftKarp({"u1": ["v1"]})
        >>> hk.left_vertices
        ['u1']
        >>> hk.right_vertices
        ['v1']
        >>> HopcroftKarp({"A": ["A"]})
        Traceback (most recent call last):
            ...
        ValueError: Partitions must be disjoint: found vertices in both sets: ['A']
        >>> HopcroftKarp({"u1": [None]})
        Traceback (most recent call last):
            ...
        ValueError: Vertices cannot be None
        """
        self.graph = graph
        self.left_vertices = list(graph.keys())
        self.right_vertices = sorted(
            {
                right_vertex
                for neighbors in graph.values()
                for right_vertex in neighbors
            },
            key=repr,
        )

        if any(vertex is None for vertex in self.left_vertices) or any(
            vertex is None for vertex in self.right_vertices
        ):
            msg = "Vertices cannot be None"
            raise ValueError(msg)

        overlap = set(self.left_vertices) & set(self.right_vertices)
        if overlap:
            msg = (
                f"Partitions must be disjoint: found vertices in both sets: "
                f"{sorted(overlap, key=repr)}"
            )
            raise ValueError(msg)

        # pair_left[u] 将 u 的顶点存储在 V 中（或者 _NIL 如果闲置）
        self.pair_left: dict[T, T | object] = dict.fromkeys(self.left_vertices, _NIL)
        # pair_right[v] 将 v 中的 v 的对应顶点存储在 U 中（如果闲置则为 _NIL）
        self.pair_right: dict[T, T | object] = dict.fromkeys(self.right_vertices, _NIL)
        # distance_map 存储 U 中自由顶点的 BFS 级别
        self.distance_map: dict[T | object, float] = {}

    def breadth_first_search(self) -> bool:
        """BFS 阶段：对图进行分层并找到最短增广路径长度。

        返回：
            如果存在至少一条到 V 中自由顶点的增广路径，则为 True，
            否则为 False（终止条件）。

        >>> hk = HopcroftKarp({"u1": ["v1"]})
        >>> hk.breadth_first_search()
        True
        >>> hk.pair_left["u1"] = "v1"
        >>> hk.pair_right["v1"] = "u1"
        >>> hk.breadth_first_search()
        False
        """
        queue: deque[T] = deque()

        # 将左侧分区中的所有空闲顶点排入级别 0 的队列
        for left_vertex in self.left_vertices:
            if self.pair_left[left_vertex] is _NIL:
                self.distance_map[left_vertex] = 0.0
                queue.append(left_vertex)
            else:
                self.distance_map[left_vertex] = math.inf

        # distance_map[_NIL]表示到右下部中自由上部的距离
        self.distance_map[_NIL] = math.inf

        while queue:
            left_vertex = queue.popleft()
            if self.distance_map[left_vertex] < self.distance_map[_NIL]:
                for right_vertex in self.graph[left_vertex]:
                    matched_left = self.pair_right[right_vertex]
                    if self.distance_map.get(matched_left, math.inf) == math.inf:
                        self.distance_map[matched_left] = (
                            self.distance_map[left_vertex] + 1.0
                        )
                        if matched_left is not _NIL:
                            queue.append(matched_left)  # type: ignore[arg-type]

        return self.distance_map[_NIL] != math.inf

    def depth_first_search(self, start_left: T) -> bool:
        """DFS 阶段：沿着最短增广路径迭代查找并增广。

        使用显式堆栈迭代实现以防止 RecursionError
        在具有深度交替路径的图上（直径 > 1000）。

        参数：
            start_left：左侧分区中开始搜索的自由顶点。

        返回：
            如果找到并增强了增广路径，则为 True，否则为 False。

        >>> hk = HopcroftKarp({"u1": ["v1"]})
        >>> _ = hk.breadth_first_search()
        >>> hk.depth_first_search("u1")
        True
        >>> hk.pair_left["u1"]
        'v1'
        >>> hk.depth_first_search("u1")
        False
        """
        stack: list[T] = [start_left]
        neighbor_indices: list[int] = [0]
        path: list[tuple[T, T]] = []

        while stack:
            curr_left = stack[-1]
            curr_index = neighbor_indices[-1]
            neighbors = self.graph[curr_left]

            found_next = False
            for idx in range(curr_index, len(neighbors)):
                right_vertex = neighbors[idx]
                matched_left = self.pair_right[right_vertex]

                # 增强条件：仅沿着最短层路径步进
                if (
                    self.distance_map.get(matched_left, math.inf)
                    == self.distance_map[curr_left] + 1.0
                ):
                    neighbor_indices[-1] = idx + 1
                    path.append((curr_left, right_vertex))

                    if matched_left is _NIL:
                        # 到达自由右顶点：沿路径增强匹配
                        for path_left, path_right in path:
                            self.pair_right[path_right] = path_left
                            self.pair_left[path_left] = path_right
                        return True

                    stack.append(matched_left)  # type: ignore[arg-type]
                    neighbor_indices.append(0)
                    found_next = True
                    break

            if not found_next:
                # 死胡同：阶段台阶 curr_left
                self.distance_map[curr_left] = math.inf
                stack.pop()
                neighbor_indices.pop()
                if path:
                    path.pop()

        return False

    def maximum_matching(self) -> dict[T, T]:
        """计算并返回最大基数匹配。

        >>> hk = HopcroftKarp({"u1": ["v1"], "u2": ["v1"]})
        >>> hk.maximum_matching()
        {'u1': 'v1'}
        """
        while self.breadth_first_search():
            for left_vertex in self.left_vertices:
                if self.pair_left[left_vertex] is _NIL:
                    self.depth_first_search(left_vertex)

        return {
            left_vertex: matched_right  # type: ignore[misc]
            for left_vertex, matched_right in self.pair_left.items()
            if matched_right is not _NIL
        }


def hopcroft_karp[T](graph: dict[T, list[T]]) -> dict[T, T]:
    """使用 Hopcroft-Karp 在二部图中查找最大基数匹配。

    参数：
        图：将左分区 (U) 中的每个顶点映射到的邻接列表
            右分区 (V) 中相邻顶点的列表。两人
            分区必须不相交，并且顶点不能为 None。

    返回：
        表示匹配的字典，将每个匹配的顶点映射到
        左分区到右分区中的匹配伙伴。

    异常：
        ValueError: If any vertex appears in both partitions or if any vertex is None.

    示例：
        >>> # Standard bipartite matching
        >>> graph = {"u1": ["v1", "v2"], "u2": ["v1"], "u3": ["v2", "v3"]}
        >>> hopcroft_karp(graph)
        {'u1': 'v2', 'u2': 'v1', 'u3': 'v3'}

        >>> # Empty graph condition
        >>> hopcroft_karp({})
        {}

        >>> # Isolated vertices (no incident edges)
        >>> hopcroft_karp({"u1": []})
        {}

        >>> # Competing vertices (more left vertices than right vertices)
        >>> hopcroft_karp({"u1": ["v1"], "u2": ["v1"]})
        {'u1': 'v1'}

        >>> # Bipartite cycle (6 vertices)
        >>> cycle_graph = {
        ...     "u1": ["v1", "v2"],
        ...     "u2": ["v2", "v3"],
        ...     "u3": ["v3", "v1"],
        ... }
        >>> hopcroft_karp(cycle_graph)
        {'u1': 'v1', 'u2': 'v2', 'u3': 'v3'}

        >>> # Error condition: Overlapping partitions (not a valid bipartite graph)
        >>> hopcroft_karp({"A": ["A"]})
        Traceback (most recent call last):
            ...
        ValueError: Partitions must be disjoint: found vertices in both sets: ['A']

        >>> # Error condition: None vertex
        >>> hopcroft_karp({"u": [None]})
        Traceback (most recent call last):
            ...
        ValueError: Vertices cannot be None
    """
    return HopcroftKarp(graph).maximum_matching()


def test_hopcroft_karp() -> None:
    """Pytest 测试函数用于验证最大二分匹配功能。

    >>> test_hopcroft_karp()
    """
    assert hopcroft_karp({"u1": ["v1", "v2"], "u2": ["v1"], "u3": ["v2", "v3"]}) == {
        "u1": "v2",
        "u2": "v1",
        "u3": "v3",
    }
    assert hopcroft_karp({}) == {}
    assert hopcroft_karp({"u1": []}) == {}
    assert hopcroft_karp({"u1": ["v1"], "u2": ["v1"]}) == {"u1": "v1"}
    assert hopcroft_karp(
        {"u1": ["v1", "v2"], "u2": ["v2", "v3"], "u3": ["v3", "v1"]}
    ) == {"u1": "v1", "u2": "v2", "u3": "v3"}

    # 深度测试交替路径以保证不会发生RecursionError
    chain_length = 1500
    chain_graph = {f"u{i}": [f"v{i}", f"v{i + 1}"] for i in range(chain_length)}
    assert len(hopcroft_karp(chain_graph)) == chain_length


if __name__ == "__main__":
    import doctest

    doctest.testmod()
