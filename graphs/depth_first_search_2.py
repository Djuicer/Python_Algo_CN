#!/usr/bin/python

"""Author: OMKAR PATHAK"""


class Graph:
    def __init__(self) -> None:
        self.vertex = {}

    # 用于打印图顶点
    def print_graph(self) -> None:
        """
        打印图顶点。

        例子：
        >>> g = Graph()
        >>> g.add_edge(0, 1)
        >>> g.add_edge(0, 2)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 0)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(3, 3)
        >>> g.print_graph()
        {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}
        0  ->  1 -> 2
        1  ->  2
        2  ->  0 -> 3
        3  ->  3
        """
        print(self.vertex)
        for i in self.vertex:
            print(i, " -> ", " -> ".join([str(j) for j in self.vertex[i]]))

    # 用于在两个顶点之间添加边
    def add_edge(self, from_vertex: int, to_vertex: int) -> None:
        """
        在两个顶点之间添加一条边。

        :param from_vertex：源顶点。
        :param to_vertex: 目标顶点。

        例子：
        >>> g = Graph()
        >>> g.add_edge(0, 1)
        >>> g.add_edge(0, 2)
        >>> g.print_graph()
        {0: [1, 2]}
        0  ->  1 -> 2
        """
        # 检查顶点是否已经存在，
        if from_vertex in self.vertex:
            self.vertex[from_vertex].append(to_vertex)
        else:
            # 否则创建一个新顶点
            self.vertex[from_vertex] = [to_vertex]

    def dfs(self) -> None:
        """
        对图执行深度优先搜索（DFS）遍历
        并打印访问过的顶点。

        例子：
        >>> g = Graph()
        >>> g.add_edge(0, 1)
        >>> g.add_edge(0, 2)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 0)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(3, 3)
        >>> g.dfs()
        0 1 2 3
        """
        # 已访问数组，用于存储已访问过的节点
        visited = [False] * len(self.vertex)

        # 调用递归辅助函数
        for i in range(len(self.vertex)):
            if not visited[i]:
                self.dfs_recursive(i, visited)

    def dfs_recursive(self, start_vertex: int, visited: list) -> None:
        """
        对图执行梯度深度优先搜索 (DFS) 遍历。

        :param start_vertex:进入的起始顶点。
        :param Visited：跟踪访问过的顶点的列表。

        例子：
        >>> g = Graph()
        >>> g.add_edge(0, 1)
        >>> g.add_edge(0, 2)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 0)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(3, 3)
        >>> visited = [False] * len(g.vertex)
        >>> g.dfs_recursive(0, visited)
        0 1 2 3
        """
        # 将起始顶点标记为已访问
        visited[start_vertex] = True

        print(start_vertex, end="")

        # 对与该节点相邻的所有顶点进行递归
        for i in self.vertex:
            if not visited[i]:
                print(" ", end="")
                self.dfs_recursive(i, visited)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 3)

    g.print_graph()
    print("DFS:")
    g.dfs()
