"""
以下无向网络由七个顶点和十二条边组成，总权重为 243。
￼
同一网络可由下列矩阵表示。

    A   B   C   D   E   F   G
A   -   16  12  21  -   -   -
B   16  -   -   17  20  -   -
C   12  -   -   28  -   31  -
D   21  17  28  -   18  19  23
E   -   20  -   18  -   -   11
F   -   -   31  19  -   -   27
G   -   -   -   23  11  27  -

可以移除一些边来优化网络，同时保证网络中所有点仍然连通。能实现最大节省的网络
如下所示，其权重为 93，相比原网络节省 243 - 93 = 150。

network.txt（右键单击并选择 'Save Link/Target As...'）是一个 6K 文本文件，
以矩阵形式给出包含四十个顶点的网络。求在保证网络连通的同时移除冗余边所能实现的
最大节省值。

解法：
    使用 Prim 算法寻找最小生成树（Minimum Spanning Tree）。
    参考资料：https://en.wikipedia.org/wiki/Prim%27s_algorithm
"""

from __future__ import annotations

import os
from collections.abc import Mapping

EdgeT = tuple[int, int]


class Graph:
    """
    表示无向加权图的类。
    """

    def __init__(self, vertices: set[int], edges: Mapping[EdgeT, int]) -> None:
        self.vertices: set[int] = vertices
        self.edges: dict[EdgeT, int] = {
            (min(edge), max(edge)): weight for edge, weight in edges.items()
        }

    def add_edge(self, edge: EdgeT, weight: int) -> None:
        """
        向图中添加一条新边。
        >>> graph = Graph({1, 2}, {(2, 1): 4})
        >>> graph.add_edge((3, 1), 5)
        >>> sorted(graph.vertices)
        [1, 2, 3]
        >>> sorted([(v,k) for k,v in graph.edges.items()])
        [(4, (1, 2)), (5, (1, 3))]
        """
        self.vertices.add(edge[0])
        self.vertices.add(edge[1])
        self.edges[(min(edge), max(edge))] = weight

    def prims_algorithm(self) -> Graph:
        """
        运行 Prim 算法以寻找最小生成树（Minimum Spanning Tree）。
        Reference: https://en.wikipedia.org/wiki/Prim%27s_algorithm
        >>> graph = Graph({1,2,3,4},{(1,2):5, (1,3):10, (1,4):20, (2,4):30, (3,4):1})
        >>> mst = graph.prims_algorithm()
        >>> sorted(mst.vertices)
        [1, 2, 3, 4]
        >>> sorted(mst.edges)
        [(1, 2), (1, 3), (3, 4)]
        """
        subgraph: Graph = Graph({min(self.vertices)}, {})
        min_edge: EdgeT
        min_weight: int
        edge: EdgeT
        weight: int

        while len(subgraph.vertices) < len(self.vertices):
            min_weight = max(self.edges.values()) + 1
            for edge, weight in self.edges.items():
                if (edge[0] in subgraph.vertices) ^ (
                    edge[1] in subgraph.vertices
                ) and weight < min_weight:
                    min_edge = edge
                    min_weight = weight

            subgraph.add_edge(min_edge, min_weight)

        return subgraph


def solution(filename: str = "p107_network.txt") -> int:
    """
    求在保证网络连通的同时移除冗余边所能实现的最大节省值。
    >>> solution("test_network.txt")
    150
    """
    script_dir: str = os.path.abspath(os.path.dirname(__file__))
    network_file: str = os.path.join(script_dir, filename)
    edges: dict[EdgeT, int] = {}
    data: list[str]
    edge1: int
    edge2: int

    with open(network_file) as f:
        data = f.read().strip().split("\n")

    adjaceny_matrix = [line.split(",") for line in data]

    for edge1 in range(1, len(adjaceny_matrix)):
        for edge2 in range(edge1):
            if adjaceny_matrix[edge1][edge2] != "-":
                edges[(edge2, edge1)] = int(adjaceny_matrix[edge1][edge2])

    graph: Graph = Graph(set(range(len(adjaceny_matrix))), edges)

    subgraph: Graph = graph.prims_algorithm()

    initial_total: int = sum(graph.edges.values())
    optimal_total: int = sum(subgraph.edges.values())

    return initial_total - optimal_total


if __name__ == "__main__":
    print(f"{solution() = }")
