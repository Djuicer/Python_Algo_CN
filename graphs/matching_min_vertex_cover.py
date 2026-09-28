"""
* Author: Manuel Di Lullo (https://github.com/manueldilullo)
* Description: Approximization algorithm for minimum vertex cover problem.
               匹配方法。使用以邻接列表表示的图

URL: https://mathworld.wolfram.com/MinimumVertexCover.html
URL: https://www.princeton.edu/~aaa/Public/Teaching/ORF523/ORF523_Lec6.pdf
"""


def matching_min_vertex_cover(graph: dict) -> set:
    """
    使用匹配方法的最小边界覆盖 APX 算法
    @input：图（存储在邻接列表中的图，其中每个顶点
            表示为整数）
    @例子：
    >>> graph = {0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]}
    >>> matching_min_vertex_cover(graph)
    {0, 1, 2, 4}
    """
    # chosen_vertices = 首选顶点的集合
    chosen_vertices = set()
    # Edges = 图的边列表
    edges = get_edges(graph)

    # 当边列表中仍有元素时，取任意边
    # (from_node, to_node) and add his extremity to chosen_vertices and then
    # 删除与 from_node 和 to_node 相邻的所有弧
    while edges:
        from_node, to_node = edges.pop()
        chosen_vertices.add(from_node)
        chosen_vertices.add(to_node)
        for edge in edges.copy():
            if from_node in edge or to_node in edge:
                edges.discard(edge)
    return chosen_vertices


def get_edges(graph: dict) -> set:
    """
    返回一组代表所有边的对。
    @input：图（图存储在邻接列表中，其中每个顶点是
            表示为整数）
    @例子：
    >>> graph = {0: [1, 3], 1: [0, 3], 2: [0, 3], 3: [0, 1, 2]}
    >>> get_edges(graph)
    {(0, 1), (3, 1), (0, 3), (2, 0), (3, 0), (2, 3), (1, 0), (3, 2), (1, 3)}
    """
    edges = set()
    for from_node, to_nodes in graph.items():
        for to_node in to_nodes:
            edges.add((from_node, to_node))
    return edges


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 图 = {0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]}
    # print(f"Matching vertex cover:\n{matching_min_vertex_cover(graph)}")
