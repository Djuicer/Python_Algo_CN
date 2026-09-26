"""
哈密顿回路（Hamiltonian Cycle）是图中的一个环，
它恰好访问每个节点一次。
判断图中是否存在这样的路径或回路，
称为哈密顿路径问题，这是一个 NP 完全问题。

Wikipedia: https://en.wikipedia.org/wiki/Hamiltonian_path
"""


def valid_connection(
    graph: list[list[int]], next_ver: int, curr_ind: int, path: list[int]
) -> bool:
    """
    通过验证以下两项，检查能否将 next 加入 path
    1. 当前顶点与下一个顶点之间应存在边
    2. 下一个顶点不应已在 path 中
    若两项检查均通过，返回 True，表示可以连接
    这两个顶点，否则返回 False

    情况 1：使用与主函数相同的图及初始化值
    >>> graph = [[0, 1, 0, 1, 0],
    ...          [1, 0, 1, 1, 1],
    ...          [0, 1, 0, 0, 1],
    ...          [1, 1, 0, 0, 1],
    ...          [0, 1, 1, 1, 0]]
    >>> path = [0, -1, -1, -1, -1, 0]
    >>> curr_ind = 1
    >>> next_ver = 1
    >>> valid_connection(graph, next_ver, curr_ind, path)
    True

    情况 2：使用相同的图，但尝试连接已在路径中的节点
    >>> path = [0, 1, 2, 4, -1, 0]
    >>> curr_ind = 4
    >>> next_ver = 1
    >>> valid_connection(graph, next_ver, curr_ind, path)
    False
    """

    # 1. 验证当前顶点与下一个顶点之间是否存在边
    if graph[path[curr_ind - 1]][next_ver] == 0:
        return False

    # 2. 验证下一个顶点是否尚未出现在路径中
    return not any(vertex == next_ver for vertex in path)


def util_hamilton_cycle(graph: list[list[int]], path: list[int], curr_ind: int) -> bool:
    """
    伪代码
    递归终止条件：
    1. 检查是否已访问所有顶点
        1.1 若最后访问的顶点与起始顶点之间存在边，则返回 True，否则
            返回 False
    递归步骤：
    2. 遍历每个顶点
        检查从当前顶点转移到下一个顶点是否有效
            2.1 记录下一个顶点作为下一步转移
            2.2 递归调用，检查前往该顶点能否解决问题
            2.3 若该顶点能导向解，则返回 True
            2.4 否则回溯，删除已记录的顶点

    情况 1：使用与主函数相同的图及初始化值
    >>> graph = [[0, 1, 0, 1, 0],
    ...          [1, 0, 1, 1, 1],
    ...          [0, 1, 0, 0, 1],
    ...          [1, 1, 0, 0, 1],
    ...          [0, 1, 1, 1, 0]]
    >>> path = [0, -1, -1, -1, -1, 0]
    >>> curr_ind = 1
    >>> util_hamilton_cycle(graph, path, curr_ind)
    True
    >>> path
    [0, 1, 2, 4, 3, 0]

    情况 2：使用与上一种情况相同的图，但参数取自
        计算过程的中间状态
    >>> graph = [[0, 1, 0, 1, 0],
    ...          [1, 0, 1, 1, 1],
    ...          [0, 1, 0, 0, 1],
    ...          [1, 1, 0, 0, 1],
    ...          [0, 1, 1, 1, 0]]
    >>> path = [0, 1, 2, -1, -1, 0]
    >>> curr_ind = 3
    >>> util_hamilton_cycle(graph, path, curr_ind)
    True
    >>> path
    [0, 1, 2, 4, 3, 0]
    """

    # 递归终止条件
    if curr_ind == len(graph):
        # 返回当前顶点与起始顶点之间是否存在边
        return graph[path[curr_ind - 1]][path[0]] == 1

    # 递归步骤
    for next_ver in range(len(graph)):
        if valid_connection(graph, next_ver, curr_ind, path):
            # 将当前顶点加入路径，作为下一步转移
            path[curr_ind] = next_ver
            # 验证构造的路径
            if util_hamilton_cycle(graph, path, curr_ind + 1):
                return True
            # 回溯
            path[curr_ind] = -1
    return False


def hamilton_cycle(graph: list[list[int]], start_index: int = 0) -> list[int]:
    r"""
    调用 util_hamilton_cycle 子程序的包装函数，
    返回表示哈密顿回路的顶点数组，
    未找到哈密顿回路时返回空列表。
    情况 1：
    下图包含 5 条边。
    仔细观察可发现多个哈密顿回路。
    例如，一种结果是按以下顺序遍历：
    (0)->(1)->(2)->(4)->(3)->(0)

    (0)---(1)---(2)
     |   /   \   |
     |  /     \  |
     | /       \ |
     |/         \|
    (3)---------(4)
    >>> graph = [[0, 1, 0, 1, 0],
    ...          [1, 0, 1, 1, 1],
    ...          [0, 1, 0, 0, 1],
    ...          [1, 1, 0, 0, 1],
    ...          [0, 1, 1, 1, 0]]
    >>> hamilton_cycle(graph)
    [0, 1, 2, 4, 3, 0]

    情况 2：
    与情况 1 相同的图，将起始索引由默认值改为 3

    (0)---(1)---(2)
     |   /   \   |
     |  /     \  |
     | /       \ |
     |/         \|
    (3)---------(4)
    >>> graph = [[0, 1, 0, 1, 0],
    ...          [1, 0, 1, 1, 1],
    ...          [0, 1, 0, 0, 1],
    ...          [1, 1, 0, 0, 1],
    ...          [0, 1, 1, 1, 0]]
    >>> hamilton_cycle(graph, 3)
    [3, 0, 1, 2, 4, 3]

    情况 3：
    与之前相同的图，但移除了边 3-4。
    因此不再存在哈密顿回路。

    (0)---(1)---(2)
     |   /   \   |
     |  /     \  |
     | /       \ |
     |/         \|
    (3)         (4)
    >>> graph = [[0, 1, 0, 1, 0],
    ...          [1, 0, 1, 1, 1],
    ...          [0, 1, 0, 0, 1],
    ...          [1, 1, 0, 0, 0],
    ...          [0, 1, 1, 0, 0]]
    >>> hamilton_cycle(graph,4)
    []
    """

    # 将路径初始化为 -1，表示尚未访问相应位置
    path = [-1] * (len(graph) + 1)
    # 使用起始索引初始化路径的起点和终点
    path[0] = path[-1] = start_index
    # 求解，找到答案则返回路径，否则返回空数组
    return path if util_hamilton_cycle(graph, path, 1) else []
