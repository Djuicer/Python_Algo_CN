#!/usr/bin/env python3

# Author: OMKAR PATHAK, Nwachukwu Chidiebere

# 使用Python字典构建图表。
from __future__ import annotations

from pprint import pformat
from typing import TypeVar

T = TypeVar("T")


class GraphAdjacencyList[T]:
    """
    邻接表类型图数据结构，考虑有向和无向
    图表。  初始化图对象，指示它是有向的还是无向的。

    有向图示例：
    >>> d_graph = GraphAdjacencyList()
    >>> print(d_graph)
    {}
    >>> d_graph.add_edge(0, 1)
    {0: [1], 1: []}
    >>> d_graph.add_edge(1, 2).add_edge(1, 4).add_edge(1, 5)
    {0: [1], 1: [2, 4, 5], 2: [], 4: [], 5: []}
    >>> d_graph.add_edge(2, 0).add_edge(2, 6).add_edge(2, 7)
    {0: [1], 1: [2, 4, 5], 2: [0, 6, 7], 4: [], 5: [], 6: [], 7: []}
    >>> d_graph
    {0: [1], 1: [2, 4, 5], 2: [0, 6, 7], 4: [], 5: [], 6: [], 7: []}
    >>> print(repr(d_graph))
    {0: [1], 1: [2, 4, 5], 2: [0, 6, 7], 4: [], 5: [], 6: [], 7: []}

    Undirected graph example:
    >>> u_graph = GraphAdjacencyList(directed=False)
    >>> u_graph.add_edge(0, 1)
    {0: [1], 1: [0]}
    >>> u_graph.add_edge(1, 2).add_edge(1, 4).add_edge(1, 5)
    {0: [1], 1: [0, 2, 4, 5], 2: [1], 4: [1], 5: [1]}
    >>> u_graph.add_edge(2, 0).add_edge(2, 6).add_edge(2, 7)
    {0: [1, 2], 1: [0, 2, 4, 5], 2: [1, 0, 6, 7], 4: [1], 5: [1], 6: [2], 7: [2]}
    >>> u_graph.add_edge(4, 5)
    {0: [1, 2],
     1: [0, 2, 4, 5],
     2: [1, 0, 6, 7],
     4: [1, 5],
     5: [1, 4],
     6: [2],
     7: [2]}
    >>> print(u_graph)
    {0: [1, 2],
     1: [0, 2, 4, 5],
     2: [1, 0, 6, 7],
     4: [1, 5],
     5: [1, 4],
     6: [2],
     7: [2]}
    >>> print(repr(u_graph))
    {0: [1, 2],
     1: [0, 2, 4, 5],
     2: [1, 0, 6, 7],
     4: [1, 5],
     5: [1, 4],
     6: [2],
     7: [2]}
     >>> char_graph = GraphAdjacencyList(directed=False)
     >>> char_graph.add_edge('a', 'b')
     {'a': ['b'], 'b': ['a']}
     >>> char_graph.add_edge('b', 'c').add_edge('b', 'e').add_edge('b', 'f')
     {'a': ['b'], 'b': ['a', 'c', 'e', 'f'], 'c': ['b'], 'e': ['b'], 'f': ['b']}
     >>> char_graph
     {'a': ['b'], 'b': ['a', 'c', 'e', 'f'], 'c': ['b'], 'e': ['b'], 'f': ['b']}
    """

    def __init__(self, directed: bool = True) -> None:
        """
        参数：
        direct: (bool) 指示图是有向的还是无向的。默认为 True。
        """

        self.adj_list: dict[T, list[T]] = {}  # 列表字典
        self.directed = directed

    def add_edge(
        self, source_vertex: T, destination_vertex: T
    ) -> GraphAdjacencyList[T]:
        """
        将顶点连接在一起。创建从源顶点到目标的边
        顶点。
        如果在图中找不到顶点，将创建顶点
        """

        if not self.directed:  # 对于无向图
            # 如果源顶点和目标顶点都存在于
            # 邻接列表，将目标顶点添加到相邻的源顶点列表中
            # 顶点并将源顶点添加到相邻顶点的目标顶点列表中
            # 顶点。
            if source_vertex in self.adj_list and destination_vertex in self.adj_list:
                self.adj_list[source_vertex].append(destination_vertex)
                self.adj_list[destination_vertex].append(source_vertex)
            # 如果邻接列表中仅存在源顶点，则添加目标顶点
            # 获取相邻顶点的顶点列表，然后使用以下命令创建一个新顶点
            # 目标顶点作为键并分配包含源顶点的列表
            # 因为它是第一个相邻顶点。
            elif source_vertex in self.adj_list:
                self.adj_list[source_vertex].append(destination_vertex)
                self.adj_list[destination_vertex] = [source_vertex]
            # 如果邻接列表中仅存在目标顶点，则添加源顶点
            # 到相邻顶点的目标顶点列表，然后创建一个新顶点
            # 以源顶点为键并分配包含源顶点的列表
            # 因为它是第一个相邻顶点。
            elif destination_vertex in self.adj_list:
                self.adj_list[destination_vertex].append(source_vertex)
                self.adj_list[source_vertex] = [destination_vertex]
            # 如果源顶点和目标顶点都不相邻
            # 列表，以源顶点为键创建一个新顶点并分配一个列表
            # 也包含目标顶点作为它的第一个相邻顶点
            # 创建一个以目标顶点为键的新顶点并分配一个列表
            # 包含源顶点作为它的第一个相邻顶点。
            else:
                self.adj_list[source_vertex] = [destination_vertex]
                self.adj_list[destination_vertex] = [source_vertex]
        # 对于有向图
        # 如果源顶点和目标顶点都相邻
        # list，将目标顶点添加到顶点顶点的源顶点列表中。
        elif source_vertex in self.adj_list and destination_vertex in self.adj_list:
            self.adj_list[source_vertex].append(destination_vertex)
        # 如果邻接列表中仅存在源顶点，则添加目标顶点
        # 顶点到相邻顶点的源顶点列表并创建一个新顶点
        # 以目标顶点为键，没有相邻顶点
        elif source_vertex in self.adj_list:
            self.adj_list[source_vertex].append(destination_vertex)
            self.adj_list[destination_vertex] = []
        # 如果邻接列表中仅存在目标顶点，则创建一个新的
        # 以源顶点为键的顶点并分配包含目标的列表
        # 顶点作为第一个相邻顶点
        elif destination_vertex in self.adj_list:
            self.adj_list[source_vertex] = [destination_vertex]
        # 如果源顶点和目标顶点都不相邻
        # 列表，创建一个以源顶点为键的新顶点和一个包含以下内容的列表
        # 目标顶点作为它的第一个相邻顶点。然后创建一个新的顶点
        # 以目标顶点为键，没有相邻顶点
        else:
            self.adj_list[source_vertex] = [destination_vertex]
            self.adj_list[destination_vertex] = []

        return self

    def __repr__(self) -> str:
        return pformat(self.adj_list)
