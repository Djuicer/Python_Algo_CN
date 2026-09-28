"""
一条边是一座桥，如果在删除它之后，图中的连接组件的计数将
增加一。网桥代表互联网络中的漏洞，
对于设计可靠的网络很有用。例如，在有线计算机网络中，
铰接点表示关键计算机，桥表示关键计算机
电线或连接。

更详细的内容可以参考这篇文章：
https://www.geeksforgeeks.org/bridge-in-a-graph/
"""


def __get_demo_graph(index):
    return [
        {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1, 3, 5],
            3: [2, 4],
            4: [3],
            5: [2, 6, 8],
            6: [5, 7],
            7: [6, 8],
            8: [5, 7],
        },
        {
            0: [6],
            1: [9],
            2: [4, 5],
            3: [4],
            4: [2, 3],
            5: [2],
            6: [0, 7],
            7: [6],
            8: [],
            9: [1],
        },
        {
            0: [4],
            1: [6],
            2: [],
            3: [5, 6, 7],
            4: [0, 6],
            5: [3, 8, 9],
            6: [1, 3, 4, 7],
            7: [3, 6, 8, 9],
            8: [5, 7],
            9: [5, 7],
        },
        {
            0: [1, 3],
            1: [0, 2, 4],
            2: [1, 3, 4],
            3: [0, 2, 4],
            4: [1, 2, 3],
        },
    ][index]


def compute_bridges(graph: dict[int, list[int]]) -> list[tuple[int, int]]:
    """
    返回无向图桥列表 [(a1, b1), ..., (ak, bk)]；艾 <= 双
    >>> compute_bridges(__get_demo_graph(0))
    [(3, 4), (2, 3), (2, 5)]
    >>> compute_bridges(__get_demo_graph(1))
    [(6, 7), (0, 6), (1, 9), (3, 4), (2, 4), (2, 5)]
    >>> compute_bridges(__get_demo_graph(2))
    [(1, 6), (4, 6), (0, 4)]
    >>> compute_bridges(__get_demo_graph(3))
    []
    >>> compute_bridges({})
    []
    """

    id_ = 0
    n = len(graph)  # 图中的顶点数
    low = [0] * n
    visited = [False] * n

    def dfs(at, parent, bridges, id_) -> None:
        visited[at] = True
        low[at] = id_
        id_ += 1
        for to in graph[at]:
            if to == parent:
                pass
            elif not visited[to]:
                dfs(to, at, bridges, id_)
                low[at] = min(low[at], low[to])
                if id_ <= low[to]:
                    bridges.append((at, to) if at < to else (to, at))
            else:
                # 该边是后边，不能是桥
                low[at] = min(low[at], low[to])

    bridges: list[tuple[int, int]] = []
    for i in range(n):
        if not visited[i]:
            dfs(i, -1, bridges, id_)
    return bridges


if __name__ == "__main__":
    import doctest

    doctest.testmod()
