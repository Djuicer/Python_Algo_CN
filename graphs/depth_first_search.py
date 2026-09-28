"""DFS 算法的非循环实现。"""

from __future__ import annotations


def depth_first_search(graph: dict, start: str) -> set[str]:
    """图上的深度优先搜索
    :param graph: 字典格式的有向图
    :param start:作为字符串的起始顶点
    :return: 搜索结果
    >>> input_G = { "A": ["B", "C", "D"], "B": ["A", "D", "E"],
    ... "C": ["A", "F"], "D": ["B", "D"], "E": ["B", "F"],
    ... "F": ["C", "E", "G"], "G": ["F"] }
    >>> output_G = list({'A', 'B', 'C', 'D', 'E', 'F', 'G'})
    >>> all(x in output_G for x in list(depth_first_search(input_G, "A")))
    True
    >>> all(x in output_G for x in list(depth_first_search(input_G, "G")))
    True
    """
    explored, stack = set(start), [start]

    while stack:
        v = stack.pop()
        explored.add(v)
        # 与BFS的区别：
        # 1) pop last element instead of first one
        # 2) add adjacent elements to stack without exploring them
        for adj in reversed(graph[v]):
            if adj not in explored:
                stack.append(adj)
    return explored


G = {
    "A": ["B", "C", "D"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B", "D"],
    "E": ["B", "F"],
    "F": ["C", "E", "G"],
    "G": ["F"],
}

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(depth_first_search(G, "A"))
