from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


class DisjointSetTreeNode[T]:
    # 不相交集节点来存储父节点和等级
    def __init__(self, data: T) -> None:
        self.data = data
        self.parent = self
        self.rank = 0


class DisjointSetTree[T]:
    # 不相交集数据结构
    def __init__(self) -> None:
        # 从节点名称映射到节点对象
        self.map: dict[T, DisjointSetTreeNode[T]] = {}

    def make_set(self, data: T) -> None:
        # 创建一个新集合，其中 x 作为其成员
        self.map[data] = DisjointSetTreeNode(data)

    def find_set(self, data: T) -> DisjointSetTreeNode[T]:
        # 找到x所属的集合（使用路径压缩）
        elem_ref = self.map[data]
        if elem_ref != elem_ref.parent:
            elem_ref.parent = self.find_set(elem_ref.parent.data)
        return elem_ref.parent

    def link(
        self, node1: DisjointSetTreeNode[T], node2: DisjointSetTreeNode[T]
    ) -> None:
        # 联合操作的辅助函数
        if node1.rank > node2.rank:
            node2.parent = node1
        else:
            node1.parent = node2
            if node1.rank == node2.rank:
                node2.rank += 1

    def union(self, data1: T, data2: T) -> None:
        # 合并 2 个不相交的集合
        self.link(self.find_set(data1), self.find_set(data2))


class GraphUndirectedWeighted[T]:
    def __init__(self) -> None:
        # 连接：从节点到相邻节点的映射（带权重）
        self.connections: dict[T, dict[T, int]] = {}

    def add_node(self, node: T) -> None:
        # 仅当图中不存在时才添加节点
        if node not in self.connections:
            self.connections[node] = {}

    def add_edge(self, node1: T, node2: T, weight: int) -> None:
        # 添加具有给定权重的边
        self.add_node(node1)
        self.add_node(node2)
        self.connections[node1][node2] = weight
        self.connections[node2][node1] = weight

    def kruskal(self) -> GraphUndirectedWeighted[T]:
        # 用于生成图的最小生成树（MST）的Kruskal算法
        """
        Details: https://en.wikipedia.org/wiki/Kruskal%27s_algorithm

        例子：
        >>> g1 = GraphUndirectedWeighted[int]()
        >>> g1.add_edge(1, 2, 1)
        >>> g1.add_edge(2, 3, 2)
        >>> g1.add_edge(3, 4, 1)
        >>> g1.add_edge(3, 5, 100) # Removed in MST
        >>> g1.add_edge(4, 5, 5)
        >>> assert 5 in g1.connections[3]
        >>> mst = g1.kruskal()
        >>> assert 5 not in mst.connections[3]

        >>> g2 = GraphUndirectedWeighted[str]()
        >>> g2.add_edge('A', 'B', 1)
        >>> g2.add_edge('B', 'C', 2)
        >>> g2.add_edge('C', 'D', 1)
        >>> g2.add_edge('C', 'E', 100) # Removed in MST
        >>> g2.add_edge('D', 'E', 5)
        >>> assert 'E' in g2.connections["C"]
        >>> mst = g2.kruskal()
        >>> assert 'E' not in mst.connections['C']
        """

        # 按权重升序获取边
        edges = []
        seen = set()
        for start in self.connections:
            for end in self.connections[start]:
                if (start, end) not in seen:
                    seen.add((end, start))
                    edges.append((start, end, self.connections[start][end]))
        edges.sort(key=lambda x: x[2])

        # 创建不相交集
        disjoint_set = DisjointSetTree[T]()
        for node in self.connections:
            disjoint_set.make_set(node)

        # MST生成
        num_edges = 0
        index = 0
        graph = GraphUndirectedWeighted[T]()
        while num_edges < len(self.connections) - 1:
            u, v, w = edges[index]
            index += 1
            parent_u = disjoint_set.find_set(u)
            parent_v = disjoint_set.find_set(v)
            if parent_u != parent_v:
                num_edges += 1
                graph.add_edge(u, v, w)
                disjoint_set.union(u, v)
        return graph
