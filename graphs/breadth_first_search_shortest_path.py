"""在无权图中查找从给定源节点到目标节点的最短路径时，
可以使用广度优先搜索（Breadth-First Search, BFS）。
"""

from __future__ import annotations

graph = {
    "A": ["B", "C", "E"],
    "B": ["A", "D", "E"],
    "C": ["A", "F", "G"],
    "D": ["B"],
    "E": ["A", "B", "D"],
    "F": ["C"],
    "G": ["C"],
}


class Graph:
    def __init__(self, graph: dict[str, list[str]], source_vertex: str) -> None:
        """
        图被实现为邻接列表的字典。还，
        源顶点必须在初始化时定义。
        """
        self.graph = graph
        # 将节点映射到生成的广度优先树中的父节点
        self.parent: dict[str, str | None] = {}
        self.source_vertex = source_vertex

    def breath_first_search(self) -> None:
        """
        此函数是在此图上运行广度优先搜索的助手。
        >>> g = Graph(graph, "G")
        >>> g.breath_first_search()
        >>> g.parent
        {'G': None, 'C': 'G', 'A': 'C', 'F': 'C', 'B': 'A', 'E': 'A', 'D': 'B'}
        """
        visited = {self.source_vertex}
        self.parent[self.source_vertex] = None
        queue = [self.source_vertex]  # 先进先出队列

        while queue:
            vertex = queue.pop(0)
            for adjacent_vertex in self.graph[vertex]:
                if adjacent_vertex not in visited:
                    visited.add(adjacent_vertex)
                    self.parent[adjacent_vertex] = vertex
                    queue.append(adjacent_vertex)

    def shortest_path(self, target_vertex: str) -> str:
        """
        这个最短路径函数返回一个字符串，描述结果：
        1.) No path is found. The string is a human readable message to indicate this.
        2.) The shortest path is found. The string is in the form
            `v1(->v2->v3->...->vn)`，其中 v1 是源顶点，vn 是目标顶点
            顶点，如果它单独存在的话。

        >>> g = Graph(graph, "G")
        >>> g.breath_first_search()

        Case 1 - No path is found.
        >>> g.shortest_path("Foo")
        Traceback (most recent call last):
            ...
        ValueError: No path from vertex: G to vertex: Foo

        Case 2 - The path is found.
        >>> g.shortest_path("D")
        'G->C->A->B->D'
        >>> g.shortest_path("G")
        'G'
        """
        if target_vertex == self.source_vertex:
            return self.source_vertex

        target_vertex_parent = self.parent.get(target_vertex)
        if target_vertex_parent is None:
            msg = (
                f"No path from vertex: {self.source_vertex} to vertex: {target_vertex}"
            )
            raise ValueError(msg)

        return self.shortest_path(target_vertex_parent) + f"->{target_vertex}"


if __name__ == "__main__":
    g = Graph(graph, "G")
    g.breath_first_search()
    print(g.shortest_path("D"))
    print(g.shortest_path("G"))
    print(g.shortest_path("Foo"))
