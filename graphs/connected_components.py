"""
https://en.wikipedia.org/wiki/Component_(graph_theory)

查找图中的连通分量

"""

test_graph_1 = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1], 4: [5, 6], 5: [4, 6], 6: [4, 5]}

test_graph_2 = {0: [1, 2, 3], 1: [0, 3], 2: [0], 3: [0, 1], 4: [], 5: []}


def dfs(graph: dict, vert: int, visited: list) -> list:
    """
    使用深度优先搜索查找所有顶点
    与初始顶点位于同一组件中
    >>> dfs(test_graph_1, 0, 5 * [False])
    [0, 1, 3, 2]
    >>> dfs(test_graph_2, 0, 6 * [False])
    [0, 1, 3, 2]
    """

    visited[vert] = True
    connected_verts = []

    for neighbour in graph[vert]:
        if not visited[neighbour]:
            connected_verts += dfs(graph, neighbour, visited)

    return [vert, *connected_verts]


def connected_components(graph: dict) -> list:
    """
    该函数以图作为参数
    然后返回连接组件的列表
    >>> connected_components(test_graph_1)
    [[0, 1, 3, 2], [4, 5, 6]]
    >>> connected_components(test_graph_2)
    [[0, 1, 3, 2], [4], [5]]
    """

    graph_size = len(graph)
    visited = graph_size * [False]
    components_list = []

    for i in range(graph_size):
        if not visited[i]:
            i_connected = dfs(graph, i, visited)
            components_list.append(i_connected)

    return components_list


if __name__ == "__main__":
    import doctest

    doctest.testmod()
