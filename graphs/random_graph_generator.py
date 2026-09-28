"""
* Author: Manuel Di Lullo (https://github.com/manueldilullo)
* Description: Random graphs generator.
               使用以邻接列表表示的图。

URL: https://en.wikipedia.org/wiki/Random_graph
"""

import random


def random_graph(
    vertices_number: int, probability: float, directed: bool = False
) -> dict:
    """
    生成随机图
    @输入：vertices_number（顶点数），
            概率（通用边 (u,v) 存在的概率），
            有向（如果为真：图将是有向图，
                      否则它将是一个无向图）
    @例子：
    >>> random.seed(1)
    >>> random_graph(4, 0.5)
    {0: [1], 1: [0, 2, 3], 2: [1, 3], 3: [1, 2]}
    >>> random.seed(1)
    >>> random_graph(4, 0.5, True)
    {0: [1], 1: [2, 3], 2: [3], 3: []}
    """
    graph: dict = {i: [] for i in range(vertices_number)}

    # 如果概率大于或等于1，则生成完整图
    if probability >= 1:
        return complete_graph(vertices_number)
    # 如果概率低于或等于 0，则返回没有边的图
    if probability <= 0:
        return graph

    # 对于每对节点，添加一条从 u 到 v 的边
    # 如果随机生成的数字大于概率概率
    for i in range(vertices_number):
        for j in range(i + 1, vertices_number):
            if random.random() < probability:
                graph[i].append(j)
                if not directed:
                    # 如果图是无向的，则添加一条从 j 到 i 的边
                    graph[j].append(i)
    return graph


def complete_graph(vertices_number: int) -> dict:
    """
    生成具有vertices_number顶点的完整图。
    @输入：vertices_number（顶点数），
            有向（如果图无向则为False，否则为True）
    @例子：
    >>> complete_graph(3)
    {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    """
    return {
        i: [j for j in range(vertices_number) if i != j] for i in range(vertices_number)
    }


if __name__ == "__main__":
    import doctest

    doctest.testmod()
