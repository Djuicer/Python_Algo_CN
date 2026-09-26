"""
图着色（Graph Coloring，也称 m 着色问题）要求
用至多 'm' 种颜色为图的顶点着色，
使任意两个相邻顶点的颜色不同。

Wikipedia: https://en.wikipedia.org/wiki/Graph_coloring
"""


def valid_coloring(
    neighbours: list[int], colored_vertices: list[int], color: int
) -> bool:
    """
    检查能否为给定顶点分配指定颜色，
    而不违反图着色约束（即任意两个相邻顶点
    颜色不同）。

    步骤：
    逐一检查邻居是否满足着色约束
    若任意邻居不满足约束，则返回 False
    若所有邻居均满足约束，则返回 True

    Parameters:
    neighbours: 表示哪些顶点与当前顶点
                相邻的列表。
                1 表示当前顶点与该邻居之间
                存在边。
    colored_vertices: 所有顶点当前颜色分配的列表
                      （-1 表示未着色）。
    color: 尝试分配给当前顶点的颜色。

    Returns:
    若可安全地为顶点分配给定颜色，则返回 True，
    否则返回 False。

    示例：
    >>> neighbours = [0, 1, 0, 1, 0]
    >>> colored_vertices = [0, 2, 1, 2, 0]
    >>> color = 1
    >>> valid_coloring(neighbours, colored_vertices, color)
    True

    >>> color = 2
    >>> valid_coloring(neighbours, colored_vertices, color)
    False

    >>> neighbors = [1, 0, 1, 0]
    >>> colored_vertices = [-1, -1, -1, -1]
    >>> color = 0
    >>> valid_coloring(neighbors, colored_vertices, color)
    True
    """
    # 检查是否有相邻顶点已使用相同颜色
    return not any(
        neighbour == 1 and colored_vertices[i] == color
        for i, neighbour in enumerate(neighbours)
    )


def util_color(
    graph: list[list[int]], max_colors: int, colored_vertices: list[int], index: int
) -> bool:
    """
    使用回溯法尝试为图着色的递归函数。

    递归终止条件：
    1. 检查是否已完成着色
        1.1 若完成则返回 True（表示图已成功着色）

    递归步骤：
    2. 遍历每种颜色：
        检查当前着色是否有效：
            2.1. 为给定顶点着色
            2.2. 递归调用，检查此着色能否导向一个解
            2.4. 若当前着色导向一个解，则返回
            2.5. 撤销给定顶点的着色

    Parameters:
    graph: 表示图的邻接矩阵。
           若顶点 i 与 j 之间存在边，
           则 graph[i][j] 为 1。
    max_colors: 允许使用的最多颜色数（m 着色问题中的 m）。
    colored_vertices: 各顶点当前的颜色分配。
                      -1 表示该顶点尚未
                      着色。
    index: 当前处理的顶点索引。

    Returns:
    若使用至多 max_colors 种颜色可以完成着色，则返回 True，否则返回 False。

    示例：
    >>> graph = [[0, 1, 0, 0, 0],
    ...          [1, 0, 1, 0, 1],
    ...          [0, 1, 0, 1, 0],
    ...          [0, 1, 1, 0, 0],
    ...          [0, 1, 0, 0, 0]]
    >>> max_colors = 3
    >>> colored_vertices = [0, 1, 0, 0, 0]
    >>> index = 3

    >>> util_color(graph, max_colors, colored_vertices, index)
    True

    >>> max_colors = 2
    >>> util_color(graph, max_colors, colored_vertices, index)
    False
    """
    # 递归终止条件：所有顶点都已分配颜色，说明找到了有效解
    if index == len(graph):
        return True

    # 为当前顶点尝试每种颜色
    for color in range(max_colors):
        # 检查为当前顶点分配 'color' 是否有效
        if valid_coloring(graph[index], colored_vertices, color):
            colored_vertices[index] = color  # 分配颜色
            # 递归为其余顶点着色
            if util_color(graph, max_colors, colored_vertices, index + 1):
                return True
            # 当前分配无法得到解时回溯
            colored_vertices[index] = -1

    return False  # 无法进行有效着色时返回 False


def color(graph: list[list[int]], max_colors: int) -> list[int]:
    """
    尝试使用至多 max_colors 种颜色为图着色，使任意两个相邻
    顶点颜色不同。
    若可行，返回颜色分配列表；
    否则返回空列表。

    Parameters:
    graph: 表示图的邻接矩阵。
    max_colors: 允许使用的最多颜色数。

    Returns:
    若使用 max_colors 种颜色可以完成着色，则返回颜色分配列表。
    列表中每个索引处的值表示
    对应顶点所分配的颜色。
    无法着色时返回空列表。

    示例：
    >>> graph = [[0, 1, 0, 0, 0],
    ...          [1, 0, 1, 0, 1],
    ...          [0, 1, 0, 1, 0],
    ...          [0, 1, 1, 0, 0],
    ...          [0, 1, 0, 0, 0]]
    >>> max_colors = 3
    >>> color(graph, max_colors)
    [0, 1, 0, 2, 0]

    >>> max_colors = 2
    >>> color(graph, max_colors)
    []

    >>> graph = [[0, 1], [1, 0]]  # Simple 2-node graph
    >>> max_colors = 2
    >>> color(graph, max_colors)
    [0, 1]

    >>> graph = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]  # Complete graph of 3 vertices
    >>> max_colors = 2
    >>> color(graph, max_colors)
    []

    >>> max_colors = 3
    >>> color(graph, max_colors)
    [0, 1, 2]
    >>> color([], 2)  # empty graph
    []
    >>> color([[0]], 1)  # single node, 1 color
    [0]
    >>> color([[0, 1], [1, 0]], 1)  # 2 nodes, 1 color (impossible)
    []
    >>> color([[0, 1], [1, 0]], 2)  # 2 nodes, 2 colors (possible)
    [0, 1]
    """
    # 将所有顶点初始化为未着色（-1）
    colored_vertices = [-1] * len(graph)

    # 使用辅助函数，从顶点 0 开始尝试为图着色
    if util_color(graph, max_colors, colored_vertices, 0):
        return colored_vertices  # 成功的颜色分配

    return []  # 无法进行有效着色
