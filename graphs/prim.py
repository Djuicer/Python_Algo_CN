"""普里姆算法。

使用Prim算法确定图的最小生成树（MST）。

Details: https://en.wikipedia.org/wiki/Prim%27s_algorithm
"""

import heapq as hq
import math
from collections.abc import Iterator


class Vertex:
    """类顶点。"""

    def __init__(self, id_) -> None:
        """
        论据：
            id - 输入一个 id 来标识
        属性：
            邻居 - 它链接到的顶点列表
            Edges - 存储边权重的字典
        """
        self.id = str(id_)
        self.key = None
        self.pi = None
        self.neighbors = []
        self.edges = {}  # {vertex:distance}

    def __lt__(self, other):
        """与 < 运算符的比较规则。"""
        return self.key < other.key

    def __repr__(self) -> str:
        """返回顶点ID。"""
        return self.id

    def add_neighbor(self, vertex) -> None:
        """在邻居列表中添加一个指向顶点的指针。"""
        self.neighbors.append(vertex)

    def add_edge(self, vertex, weight) -> None:
        """目标顶点和权重。"""
        self.edges[vertex.id] = weight


def connect(graph, a, b, edge) -> None:
    # 添加邻居：
    graph[a - 1].add_neighbor(graph[b - 1])
    graph[b - 1].add_neighbor(graph[a - 1])
    # 添加边：
    graph[a - 1].add_edge(graph[b - 1], edge)
    graph[b - 1].add_edge(graph[a - 1], edge)


def prim(graph: list, root: Vertex) -> list:
    """普里姆算法。

    运行时间：
        O(mn) with `m` edges and `n` vertices

    返回：
        具有最小生成树边的列表

    用法：
        prim(图，图[0])
    """
    a = []
    for u in graph:
        u.key = math.inf
        u.pi = None
    root.key = 0
    q = graph[:]
    while q:
        u = min(q)
        q.remove(u)
        for v in u.neighbors:
            if (v in q) and (u.edges[v.id] < v.key):
                v.pi = u
                v.key = u.edges[v.id]
    for i in range(1, len(graph)):
        a.append((int(graph[i].id) + 1, int(graph[i].pi.id) + 1))
    return a


def prim_heap(graph: list, root: Vertex) -> Iterator[tuple]:
    """带最小堆的 Prim 算法。

    运行时间：
        O((m + n)log n) with `m` edges and `n` vertices

    屈服：
        最小生成树的边

    用法：
        prim(图，图[0])
    """
    for u in graph:
        u.key = math.inf
        u.pi = None
    root.key = 0

    h = list(graph)
    hq.heapify(h)

    while h:
        u = hq.heappop(h)
        for v in u.neighbors:
            if (v in h) and (u.edges[v.id] < v.key):
                v.pi = u
                v.key = u.edges[v.id]
                hq.heapify(h)

    for i in range(1, len(graph)):
        yield (int(graph[i].id) + 1, int(graph[i].pi.id) + 1)


def test_vector() -> None:
    """
    # 创建一个列表来存储 x 顶点。
    >>> x = 5
    >>> G = [Vertex(n) for n in range(x)]

    >>> connect(G, 1, 2, 15)
    >>> connect(G, 1, 3, 12)
    >>> connect(G, 2, 4, 13)
    >>> connect(G, 2, 5, 5)
    >>> connect(G, 3, 2, 6)
    >>> connect(G, 3, 4, 6)
    >>> connect(G, 0, 0, 0)  # Generate the minimum spanning tree:
    >>> G_heap = G[:]
    >>> MST = prim(G, G[0])
    >>> MST_heap = prim_heap(G, G[0])
    >>> for i in MST:
    ...     print(i)
    (2, 3)
    (3, 1)
    (4, 3)
    (5, 2)
    >>> for i in MST_heap:
    ...     print(i)
    (2, 3)
    (3, 1)
    (4, 3)
    (5, 2)
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
