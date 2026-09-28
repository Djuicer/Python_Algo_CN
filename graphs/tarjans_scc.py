from collections import deque


def tarjan(g: list[list[int]]) -> list[list[int]]:
    """
    用于在有向图中找到强估计的 Tarjan 算法

    使用每个节点的两个主要属性来跟踪可达性，即该节点的索引
    组件内（索引），以及从该节点可到达的最低索引（低链接）。

    然后我们对每个组件执行 dfs，确保更新这些参数
并保存沿途访问的节点。

    如果我们发现当前节点的最低可达节点等于
    当前节点的索引，那么它一定是强连通的根
    组件，所以我们保存它，并且它的等可达顶点作为强
    连接的组件。

    复杂性：每个节点最多调用strong_connect()一次，并且有一个
    O(|E|) 的复杂度，因为它是 DFS。
    因此，对于图 G = (V, E) 来说，其复杂度为 O(|V| + |E|)

    >>> tarjan([[2, 3, 4], [2, 3, 4], [0, 1, 3], [0, 1, 2], [1]])
    [[4, 3, 1, 2, 0]]
    >>> tarjan([[], [], [], []])
    [[0], [1], [2], [3]]
    >>> a = [0, 1, 2, 3, 4, 5, 4]
    >>> b = [1, 0, 3, 2, 5, 4, 0]
    >>> n = 7
    >>> sorted(tarjan(create_graph(n, list(zip(a, b))))) == sorted(
    ...     tarjan(create_graph(n, list(zip(a[::-1], b[::-1])))))
    True
    >>> a = [0, 1, 2, 3, 4, 5, 6]
    >>> b = [0, 1, 2, 3, 4, 5, 6]
    >>> sorted(tarjan(create_graph(n, list(zip(a, b)))))
    [[0], [1], [2], [3], [4], [5], [6]]
    """

    n = len(g)
    stack: deque[int] = deque()
    on_stack = [False for _ in range(n)]
    index_of = [-1 for _ in range(n)]
    lowlink_of = index_of[:]

    def strong_connect(v: int, index: int, components: list[list[int]]) -> int:
        index_of[v] = index  # 看到该节点时的编号
        lowlink_of[v] = index  # 从这里可以到达的最低等级节点
        index += 1
        stack.append(v)
        on_stack[v] = True

        for w in g[v]:
            if index_of[w] == -1:
                index = strong_connect(w, index, components)
                lowlink_of[v] = (
                    lowlink_of[w] if lowlink_of[w] < lowlink_of[v] else lowlink_of[v]
                )
            elif on_stack[w]:
                lowlink_of[v] = (
                    lowlink_of[w] if lowlink_of[w] < lowlink_of[v] else lowlink_of[v]
                )

        if lowlink_of[v] == index_of[v]:
            component = []
            w = stack.pop()
            on_stack[w] = False
            component.append(w)
            while w != v:
                w = stack.pop()
                on_stack[w] = False
                component.append(w)
            components.append(component)
        return index

    components: list[list[int]] = []
    for v in range(n):
        if index_of[v] == -1:
            strong_connect(v, 0, components)

    return components


def create_graph(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """
    >>> n = 7
    >>> source = [0, 0, 1, 2, 3, 3, 4, 4, 6]
    >>> target = [1, 3, 2, 0, 1, 4, 5, 6, 5]
    >>> edges = list(zip(source, target))
    >>> create_graph(n, edges)
    [[1, 3], [2], [0], [1, 4], [5, 6], [], [5]]
    """
    g: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
    return g


if __name__ == "__main__":
    # 测试
    n_vertices = 7
    source = [0, 0, 1, 2, 3, 3, 4, 4, 6]
    target = [1, 3, 2, 0, 1, 4, 5, 6, 5]
    edges = list(zip(source, target))
    g = create_graph(n_vertices, edges)

    assert tarjan(g) == [[5], [6], [4], [3, 2, 1, 0]]
