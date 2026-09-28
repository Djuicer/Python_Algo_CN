# https://en.wikipedia.org/wiki/Lowest_common_ancestor
# https://en.wikipedia.org/wiki/Breadth-first_search

from __future__ import annotations

from queue import Queue


def swap(a: int, b: int) -> tuple[int, int]:
    """
    返回 元组 (b，) 当 给定 两个 整数 并且 b
    >>> swap(2,3)
    (3, 2)
    >>> swap(3,4)
    (4, 3)
    >>> swap(67, 12)
    (12, 67)
    >>> swap(3,-4)
    (-4, 3)
    """
    a ^= b
    b ^= a
    a ^= b
    return a, b


def create_sparse(max_node: int, parent: list[list[int]]) -> list[list[int]]:
    """
    creating sparse table 其 saves 每个 节点 2^i-th 父节点
    >>> max_node = 6
    >>> parent = [[0, 0, 1, 1, 2, 2, 3]] + [[0] * 7 for _ in range(19)]
    >>> parent = create_sparse(max_node=max_node, parent=parent)
    >>> parent[0]
    [0, 0, 1, 1, 2, 2, 3]
    >>> parent[1]
    [0, 0, 0, 0, 1, 1, 1]
    >>> parent[2]
    [0, 0, 0, 0, 0, 0, 0]

    >>> max_node = 1
    >>> parent = [[0, 0]] + [[0] * 2 for _ in range(19)]
    >>> parent = create_sparse(max_node=max_node, parent=parent)
    >>> parent[0]
    [0, 0]
    >>> parent[1]
    [0, 0]
    """
    j = 1
    while (1 << j) < max_node:
        for i in range(1, max_node + 1):
            parent[j][i] = parent[j - 1][parent[j - 1][i]]
        j += 1
    return parent


# 返回值 lca 的 节点 u,v
def lowest_common_ancestor(
    u: int, v: int, level: list[int], parent: list[list[int]]
) -> int:
    """
    返回 lowest common ancestor 之间 u 并且 v

    >>> level = [-1, 0, 1, 1, 2, 2, 2]
    >>> parent = [[0, 0, 1, 1, 2, 2, 3],[0, 0, 0, 0, 1, 1, 1]] + \
                    [[0] * 7 for _ in range(17)]
    >>> lowest_common_ancestor(u=4, v=5, level=level, parent=parent)
    2
    >>> lowest_common_ancestor(u=4, v=6, level=level, parent=parent)
    1
    >>> lowest_common_ancestor(u=2, v=3, level=level, parent=parent)
    1
    >>> lowest_common_ancestor(u=6, v=6, level=level, parent=parent)
    6
    """
    # u 必须 为 deeper 在 该树 比 v
    if level[u] < level[v]:
        u, v = swap(u, v)
    # making 深度 的 u 相同 作为 深度 的 v
    for i in range(18, -1, -1):
        if level[u] - (1 << i) >= level[v]:
            u = parent[i][u]
    # 在 相同 深度 如果 u==v 该 mean lca 是 找到
    if u == v:
        return u
    # moving 两者 节点 upwards till lca 在 找到
    for i in range(18, -1, -1):
        if parent[i][u] not in [0, parent[i][v]]:
            u, v = parent[i][u], parent[i][v]
    # returning longest common ancestor 的 u,v
    return parent[0][u]


# runs breadth 第一个 搜索 从 根节点 的树
def breadth_first_search(
    level: list[int],
    parent: list[list[int]],
    max_node: int,
    graph: dict[int, list[int]],
    root: int = 1,
) -> tuple[list[int], list[list[int]]]:
    """
    sets 每个 节点 direct 父节点
    父节点 的 根节点 是 集合 到 0
    calculates 深度 的 每个节点 从 根节点
    >>> level = [-1] * 7
    >>> parent = [[0] * 7 for _ in range(20)]
    >>> graph = {1: [2, 3], 2: [4, 5], 3: [6], 4: [], 5: [], 6: []}
    >>> level, parent = breadth_first_search(
    ...     level=level, parent=parent, max_node=6, graph=graph, root=1)
    >>> level
    [-1, 0, 1, 1, 2, 2, 2]
    >>> parent[0]
    [0, 0, 1, 1, 2, 2, 3]


    >>> level = [-1] * 2
    >>> parent = [[0] * 2 for _ in range(20)]
    >>> graph = {1: []}
    >>> level, parent = breadth_first_search(
    ...     level=level, parent=parent, max_node=1, graph=graph, root=1)
    >>> level
    [-1, 0]
    >>> parent[0]
    [0, 0]
    """
    level[root] = 0
    q: Queue[int] = Queue(maxsize=max_node)
    q.put(root)
    while q.qsize() != 0:
        u = q.get()
        for v in graph[u]:
            if level[v] == -1:
                level[v] = level[u] + 1
                q.put(v)
                parent[0][v] = u
    return level, parent


def main() -> None:
    max_node = 13
    # initializing 带有 0
    parent = [[0 for _ in range(max_node + 10)] for _ in range(20)]
    # initializing 带有 -1 其 表示 每个 节点 是 unvisited
    level = [-1 for _ in range(max_node + 10)]
    graph: dict[int, list[int]] = {
        1: [2, 3, 4],
        2: [5],
        3: [6, 7],
        4: [8],
        5: [9, 10],
        6: [11],
        7: [],
        8: [12, 13],
        9: [],
        10: [],
        11: [],
        12: [],
        13: [],
    }
    level, parent = breadth_first_search(level, parent, max_node, graph, 1)
    parent = create_sparse(max_node, parent)
    print("LCA of node 1 and 3 is: ", lowest_common_ancestor(1, 3, level, parent))
    print("LCA of node 5 and 6 is: ", lowest_common_ancestor(5, 6, level, parent))
    print("LCA of node 7 and 11 is: ", lowest_common_ancestor(7, 11, level, parent))
    print("LCA of node 6 and 7 is: ", lowest_common_ancestor(6, 7, level, parent))
    print("LCA of node 4 and 12 is: ", lowest_common_ancestor(4, 12, level, parent))
    print("LCA of node 8 and 8 is: ", lowest_common_ancestor(8, 8, level, parent))


if __name__ == "__main__":
    main()
