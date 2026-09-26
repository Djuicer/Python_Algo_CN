"""
https://en.wikipedia.org/wiki/Transitive_closure#In_graph_theory
https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
"""


def transitive_closure(graph: list[list[int]]) -> list[list[int]]:
    """
    使用 Floyd-Warshall 算法计算有向图的传递闭包。

    参数：
        graph: 图的邻接矩阵表示。

    返回：
        传递闭包矩阵。

    >>> graph = [
    ...     [0, 1, 1, 0],
    ...     [0, 0, 1, 0],
    ...     [1, 0, 0, 1],
    ...     [0, 0, 0, 0]
    ... ]
    >>> transitive_closure(graph)  # doctest: +NORMALIZE_WHITESPACE
    [[1, 1, 1, 1],
     [1, 1, 1, 1],
     [1, 1, 1, 1],
     [0, 0, 0, 1]]
    """
    width = len(graph)
    ans = [[graph[i][j] for j in range(width)] for i in range(width)]

    # (i, i) 的传递闭包始终为 1
    for i in range(width):
        ans[i][i] = 1

    # 应用 Floyd-Warshall 算法
    # 遍历每个中间节点 k
    for k in range(width):
        for i in range(width):
            for j in range(width):
                # 检查是否同时存在从 i 到 k 及从 k 到 j 的路径
                if ans[i][k] == 1 and ans[k][j] == 1:
                    ans[i][j] = 1

    return ans


if __name__ == "__main__":
    import doctest

    doctest.testmod()
