#!/usr/bin/env python3
"""
Author: Vikram Nithyanandam

描述：
以下实现是一个健壮的未加权图数据结构
使用邻接表实现。该图的顶点和边可以是
有效地初始化和修改，同时存储您选择的通用
每个顶点的值。

Adjacency List: https://en.wikipedia.org/wiki/Adjacency_list

未来潜在的想法：
- Add a flag to set edge weights on and set edge weights
- Make edge weights and vertex values customizable to store whatever the client wants
- Support multigraph functionality if the client wants it
"""

from __future__ import annotations

import random
import unittest
from pprint import pformat
from typing import TypeVar

import pytest

T = TypeVar("T")


class GraphAdjacencyList[T]:
    def __init__(
        self, vertices: list[T], edges: list[list[T]], directed: bool = True
    ) -> None:
        """
        参数：
         - vertices: (list[T]) The list of vertex names the client wants to
        传入。默认为空。
        - edges: (list[list[T]]) The list of edges the client wants to
        传入。每条边都是一个 2 元素列表。默认为空。
        - directed: (bool) Indicates if graph is directed or undirected.
        默认为 True。
        """
        self.adj_list: dict[T, list[T]] = {}  # 列表字典
        self.directed = directed

        # 虚假检查
        edges = edges or []
        vertices = vertices or []

        for vertex in vertices:
            self.add_vertex(vertex)

        for edge in edges:
            if len(edge) != 2:
                msg = f"Invalid input: {edge} is the wrong length."
                raise ValueError(msg)
            self.add_edge(edge[0], edge[1])

    def add_vertex(self, vertex: T) -> None:
        """
        向图添加一个顶点。如果给定的顶点已经存在，
        将抛出 ValueError。

        >>> g = GraphAdjacencyList(vertices=[], edges=[], directed=False)
        >>> g.add_vertex("A")
        >>> g.adj_list
        {'A': []}
        >>> g.add_vertex("A")
        Traceback (most recent call last):
        ...
        ValueError: Incorrect input: A is already in the graph.
        """
        if self.contains_vertex(vertex):
            msg = f"Incorrect input: {vertex} is already in the graph."
            raise ValueError(msg)
        self.adj_list[vertex] = []

    def add_edge(self, source_vertex: T, destination_vertex: T) -> None:
        """
        创建从源顶点到目标顶点的边。如果有的话
        给定的顶点不存在或者边已经存在，一个 ValueError
        将被抛出。
        """
        if not (
            self.contains_vertex(source_vertex)
            and self.contains_vertex(destination_vertex)
        ):
            msg = (
                f"Incorrect input: Either {source_vertex} or "
                f"{destination_vertex} does not exist"
            )
            raise ValueError(msg)
        if self.contains_edge(source_vertex, destination_vertex):
            msg = (
                "Incorrect input: The edge already exists between "
                f"{source_vertex} and {destination_vertex}"
            )
            raise ValueError(msg)

        # 将目标顶点添加到与源顶点关联的列表中
        # 如果没有指示，反之亦然
        self.adj_list[source_vertex].append(destination_vertex)
        if not self.directed:
            self.adj_list[destination_vertex].append(source_vertex)

    def remove_vertex(self, vertex: T) -> None:
        """
        从图中删除给定的顶点并删除所有传入和
        以及来自给定顶点的传出边。如果给定的顶点
        不存在，则会抛出 ValueError。
        """
        if not self.contains_vertex(vertex):
            msg = f"Incorrect input: {vertex} does not exist in this graph."
            raise ValueError(msg)

        if not self.directed:
            # 如果没有指示，则查找所有相邻顶点并删除所有引用
            # 连接到给定顶点的边数
            for neighbor in self.adj_list[vertex]:
                self.adj_list[neighbor].remove(vertex)
        else:
            # 如果有指示，则搜索所有顶点的所有邻居并删除所有顶点
            # 连接到给定顶点的边引用
            for edge_list in self.adj_list.values():
                if vertex in edge_list:
                    edge_list.remove(vertex)

        # 最后，删除给定顶点及其所有出边引用
        self.adj_list.pop(vertex)

    def remove_edge(self, source_vertex: T, destination_vertex: T) -> None:
        """
        删除两个顶点之间的边。如果任意给定的顶点
        不存在或者边不存在，将会抛出 ValueError 。
        """
        if not (
            self.contains_vertex(source_vertex)
            and self.contains_vertex(destination_vertex)
        ):
            msg = (
                f"Incorrect input: Either {source_vertex} or "
                f"{destination_vertex} does not exist"
            )
            raise ValueError(msg)
        if not self.contains_edge(source_vertex, destination_vertex):
            msg = (
                "Incorrect input: The edge does NOT exist between "
                f"{source_vertex} and {destination_vertex}"
            )
            raise ValueError(msg)

        # 从与源关联的列表中删除目标顶点
        # 顶点，反之亦然（如果没有方向）
        self.adj_list[source_vertex].remove(destination_vertex)
        if not self.directed:
            self.adj_list[destination_vertex].remove(source_vertex)

    def contains_vertex(self, vertex: T) -> bool:
        """
        如果图包含顶点，则返回 True，否则返回 False。
        """
        return vertex in self.adj_list

    def contains_edge(self, source_vertex: T, destination_vertex: T) -> bool:
        """
        如果图包含从 source_vertex 到 destination_vertex 的边，则返回 True，
        否则返回 False。如果任一给定顶点不存在，则抛出 ValueError。
        """
        if not (
            self.contains_vertex(source_vertex)
            and self.contains_vertex(destination_vertex)
        ):
            msg = (
                f"Incorrect input: Either {source_vertex} "
                f"or {destination_vertex} does not exist."
            )
            raise ValueError(msg)

        return destination_vertex in self.adj_list[source_vertex]

    def clear_graph(self) -> None:
        """
        清除所有顶点和边。
        """
        self.adj_list = {}

    def __repr__(self) -> str:
        return pformat(self.adj_list)


class TestGraphAdjacencyList(unittest.TestCase):
    def __assert_graph_edge_exists_check(
        self,
        undirected_graph: GraphAdjacencyList,
        directed_graph: GraphAdjacencyList,
        edge: list[int],
    ) -> None:
        assert undirected_graph.contains_edge(edge[0], edge[1])
        assert undirected_graph.contains_edge(edge[1], edge[0])
        assert directed_graph.contains_edge(edge[0], edge[1])

    def __assert_graph_edge_does_not_exist_check(
        self,
        undirected_graph: GraphAdjacencyList,
        directed_graph: GraphAdjacencyList,
        edge: list[int],
    ) -> None:
        assert not undirected_graph.contains_edge(edge[0], edge[1])
        assert not undirected_graph.contains_edge(edge[1], edge[0])
        assert not directed_graph.contains_edge(edge[0], edge[1])

    def __assert_graph_vertex_exists_check(
        self,
        undirected_graph: GraphAdjacencyList,
        directed_graph: GraphAdjacencyList,
        vertex: int,
    ) -> None:
        assert undirected_graph.contains_vertex(vertex)
        assert directed_graph.contains_vertex(vertex)

    def __assert_graph_vertex_does_not_exist_check(
        self,
        undirected_graph: GraphAdjacencyList,
        directed_graph: GraphAdjacencyList,
        vertex: int,
    ) -> None:
        assert not undirected_graph.contains_vertex(vertex)
        assert not directed_graph.contains_vertex(vertex)

    def __generate_random_edges(
        self, vertices: list[int], edge_pick_count: int
    ) -> list[list[int]]:
        assert edge_pick_count <= len(vertices)

        random_source_vertices: list[int] = random.sample(
            vertices[0 : int(len(vertices) / 2)], edge_pick_count
        )
        random_destination_vertices: list[int] = random.sample(
            vertices[int(len(vertices) / 2) :], edge_pick_count
        )
        random_edges: list[list[int]] = []

        for source in random_source_vertices:
            for dest in random_destination_vertices:
                random_edges.append([source, dest])

        return random_edges

    def __generate_graphs(
        self, vertex_count: int, min_val: int, max_val: int, edge_pick_count: int
    ) -> tuple[GraphAdjacencyList, GraphAdjacencyList, list[int], list[list[int]]]:
        if max_val - min_val + 1 < vertex_count:
            raise ValueError(
                "Will result in duplicate vertices. Either increase range "
                "between min_val and max_val or decrease vertex count."
            )

        # 生成图输入
        random_vertices: list[int] = random.sample(
            range(min_val, max_val + 1), vertex_count
        )
        random_edges: list[list[int]] = self.__generate_random_edges(
            random_vertices, edge_pick_count
        )

        # 构建图表
        undirected_graph = GraphAdjacencyList(
            vertices=random_vertices, edges=random_edges, directed=False
        )
        directed_graph = GraphAdjacencyList(
            vertices=random_vertices, edges=random_edges, directed=True
        )

        return undirected_graph, directed_graph, random_vertices, random_edges

    def test_init_check(self) -> None:
        (
            undirected_graph,
            directed_graph,
            random_vertices,
            random_edges,
        ) = self.__generate_graphs(20, 0, 100, 4)

        # 使用顶点和边测试图初始化
        for num in random_vertices:
            self.__assert_graph_vertex_exists_check(
                undirected_graph, directed_graph, num
            )

        for edge in random_edges:
            self.__assert_graph_edge_exists_check(
                undirected_graph, directed_graph, edge
            )
        assert not undirected_graph.directed
        assert directed_graph.directed

    def test_contains_vertex(self) -> None:
        random_vertices: list[int] = random.sample(range(101), 20)

        # 构建没有边的图
        undirected_graph = GraphAdjacencyList(
            vertices=random_vertices, edges=[], directed=False
        )
        directed_graph = GraphAdjacencyList(
            vertices=random_vertices, edges=[], directed=True
        )

        # 测试contains_vertex
        for num in range(101):
            assert (num in random_vertices) == undirected_graph.contains_vertex(num)
            assert (num in random_vertices) == directed_graph.contains_vertex(num)

    def test_add_vertices(self) -> None:
        random_vertices: list[int] = random.sample(range(101), 20)

        # 构建空图
        undirected_graph: GraphAdjacencyList = GraphAdjacencyList(
            vertices=[], edges=[], directed=False
        )
        directed_graph: GraphAdjacencyList = GraphAdjacencyList(
            vertices=[], edges=[], directed=True
        )

        # 运行add_vertex
        for num in random_vertices:
            undirected_graph.add_vertex(num)

        for num in random_vertices:
            directed_graph.add_vertex(num)

        # 测试add_vertex有效
        for num in random_vertices:
            self.__assert_graph_vertex_exists_check(
                undirected_graph, directed_graph, num
            )

    def test_remove_vertices(self) -> None:
        random_vertices: list[int] = random.sample(range(101), 20)

        # 构建没有边的图
        undirected_graph = GraphAdjacencyList(
            vertices=random_vertices, edges=[], directed=False
        )
        directed_graph = GraphAdjacencyList(
            vertices=random_vertices, edges=[], directed=True
        )

        # 测试remove_vertex有效
        for num in random_vertices:
            self.__assert_graph_vertex_exists_check(
                undirected_graph, directed_graph, num
            )

            undirected_graph.remove_vertex(num)
            directed_graph.remove_vertex(num)

            self.__assert_graph_vertex_does_not_exist_check(
                undirected_graph, directed_graph, num
            )

    def test_add_and_remove_vertices_repeatedly(self) -> None:
        random_vertices1: list[int] = random.sample(range(51), 20)
        random_vertices2: list[int] = random.sample(range(51, 101), 20)

        # 构建没有边的图
        undirected_graph = GraphAdjacencyList(
            vertices=random_vertices1, edges=[], directed=False
        )
        directed_graph = GraphAdjacencyList(
            vertices=random_vertices1, edges=[], directed=True
        )

        # 测试添加和删除顶点
        for i, _ in enumerate(random_vertices1):
            undirected_graph.add_vertex(random_vertices2[i])
            directed_graph.add_vertex(random_vertices2[i])

            self.__assert_graph_vertex_exists_check(
                undirected_graph, directed_graph, random_vertices2[i]
            )

            undirected_graph.remove_vertex(random_vertices1[i])
            directed_graph.remove_vertex(random_vertices1[i])

            self.__assert_graph_vertex_does_not_exist_check(
                undirected_graph, directed_graph, random_vertices1[i]
            )

        # 删除所有顶点
        for i, _ in enumerate(random_vertices1):
            undirected_graph.remove_vertex(random_vertices2[i])
            directed_graph.remove_vertex(random_vertices2[i])

            self.__assert_graph_vertex_does_not_exist_check(
                undirected_graph, directed_graph, random_vertices2[i]
            )

    def test_contains_edge(self) -> None:
        # 生成图和图输入
        vertex_count = 20
        (
            undirected_graph,
            directed_graph,
            random_vertices,
            random_edges,
        ) = self.__generate_graphs(vertex_count, 0, 100, 4)

        # 生成所有可能的边进行测试
        all_possible_edges: list[list[int]] = []
        for i in range(vertex_count - 1):
            for j in range(i + 1, vertex_count):
                all_possible_edges.append([random_vertices[i], random_vertices[j]])
                all_possible_edges.append([random_vertices[j], random_vertices[i]])

        # 测试contains_edge功能
        for edge in all_possible_edges:
            if edge in random_edges:
                self.__assert_graph_edge_exists_check(
                    undirected_graph, directed_graph, edge
                )
            elif [edge[1], edge[0]] in random_edges:
                # 因为这条边存在无向但相反
                # 对于定向可能不存在
                self.__assert_graph_edge_exists_check(
                    undirected_graph, directed_graph, [edge[1], edge[0]]
                )
            else:
                self.__assert_graph_edge_does_not_exist_check(
                    undirected_graph, directed_graph, edge
                )

    def test_add_edge(self) -> None:
        # 生成图输入
        random_vertices: list[int] = random.sample(range(101), 15)
        random_edges: list[list[int]] = self.__generate_random_edges(random_vertices, 4)

        # 构建没有边的图
        undirected_graph = GraphAdjacencyList(
            vertices=random_vertices, edges=[], directed=False
        )
        directed_graph = GraphAdjacencyList(
            vertices=random_vertices, edges=[], directed=True
        )

        # 运行并测试add_edge
        for edge in random_edges:
            undirected_graph.add_edge(edge[0], edge[1])
            directed_graph.add_edge(edge[0], edge[1])
            self.__assert_graph_edge_exists_check(
                undirected_graph, directed_graph, edge
            )

    def test_remove_edge(self) -> None:
        # 生成图输入和图
        (
            undirected_graph,
            directed_graph,
            _random_vertices,
            random_edges,
        ) = self.__generate_graphs(20, 0, 100, 4)

        # 运行并测试remove_edge
        for edge in random_edges:
            self.__assert_graph_edge_exists_check(
                undirected_graph, directed_graph, edge
            )
            undirected_graph.remove_edge(edge[0], edge[1])
            directed_graph.remove_edge(edge[0], edge[1])
            self.__assert_graph_edge_does_not_exist_check(
                undirected_graph, directed_graph, edge
            )

    def test_add_and_remove_edges_repeatedly(self) -> None:
        (
            undirected_graph,
            directed_graph,
            random_vertices,
            random_edges,
        ) = self.__generate_graphs(20, 0, 100, 4)

        # 做一些更多的边选项！
        more_random_edges: list[list[int]] = []

        while len(more_random_edges) != len(random_edges):
            edges: list[list[int]] = self.__generate_random_edges(random_vertices, 4)
            for edge in edges:
                if len(more_random_edges) == len(random_edges):
                    break
                if edge not in more_random_edges and edge not in random_edges:
                    more_random_edges.append(edge)

        for i, _ in enumerate(random_edges):
            undirected_graph.add_edge(more_random_edges[i][0], more_random_edges[i][1])
            directed_graph.add_edge(more_random_edges[i][0], more_random_edges[i][1])

            self.__assert_graph_edge_exists_check(
                undirected_graph, directed_graph, more_random_edges[i]
            )

            undirected_graph.remove_edge(random_edges[i][0], random_edges[i][1])
            directed_graph.remove_edge(random_edges[i][0], random_edges[i][1])

            self.__assert_graph_edge_does_not_exist_check(
                undirected_graph, directed_graph, random_edges[i]
            )

    def test_add_vertex_exception_check(self) -> None:
        (
            undirected_graph,
            directed_graph,
            random_vertices,
            _random_edges,
        ) = self.__generate_graphs(20, 0, 100, 4)

        for vertex in random_vertices:
            with pytest.raises(ValueError):
                undirected_graph.add_vertex(vertex)
            with pytest.raises(ValueError):
                directed_graph.add_vertex(vertex)

    def test_remove_vertex_exception_check(self) -> None:
        (
            undirected_graph,
            directed_graph,
            random_vertices,
            _random_edges,
        ) = self.__generate_graphs(20, 0, 100, 4)

        for i in range(101):
            if i not in random_vertices:
                with pytest.raises(ValueError):
                    undirected_graph.remove_vertex(i)
                with pytest.raises(ValueError):
                    directed_graph.remove_vertex(i)

    def test_add_edge_exception_check(self) -> None:
        (
            undirected_graph,
            directed_graph,
            _random_vertices,
            random_edges,
        ) = self.__generate_graphs(20, 0, 100, 4)

        for edge in random_edges:
            with pytest.raises(ValueError):
                undirected_graph.add_edge(edge[0], edge[1])
            with pytest.raises(ValueError):
                directed_graph.add_edge(edge[0], edge[1])

    def test_remove_edge_exception_check(self) -> None:
        (
            undirected_graph,
            directed_graph,
            random_vertices,
            random_edges,
        ) = self.__generate_graphs(20, 0, 100, 4)

        more_random_edges: list[list[int]] = []

        while len(more_random_edges) != len(random_edges):
            edges: list[list[int]] = self.__generate_random_edges(random_vertices, 4)
            for edge in edges:
                if len(more_random_edges) == len(random_edges):
                    break
                if edge not in more_random_edges and edge not in random_edges:
                    more_random_edges.append(edge)

        for edge in more_random_edges:
            with pytest.raises(ValueError):
                undirected_graph.remove_edge(edge[0], edge[1])
            with pytest.raises(ValueError):
                directed_graph.remove_edge(edge[0], edge[1])

    def test_contains_edge_exception_check(self) -> None:
        (
            undirected_graph,
            directed_graph,
            random_vertices,
            _random_edges,
        ) = self.__generate_graphs(20, 0, 100, 4)

        for vertex in random_vertices:
            with pytest.raises(ValueError):
                undirected_graph.contains_edge(vertex, 102)
            with pytest.raises(ValueError):
                directed_graph.contains_edge(vertex, 102)

        with pytest.raises(ValueError):
            undirected_graph.contains_edge(103, 102)
        with pytest.raises(ValueError):
            directed_graph.contains_edge(103, 102)


if __name__ == "__main__":
    unittest.main()
