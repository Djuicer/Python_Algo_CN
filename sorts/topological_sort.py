"""有向无环图（DAG）的拓扑排序（Topological Sort）

https://en.wikipedia.org/wiki/Topological_sorting
https://en.wikipedia.org/wiki/Directed_acyclic_graph

注意：topological_sort() 对有向无环图排序，因此 topological_sort(2, 1, 3)
    应失败。
"""

#     a
#    / \
#   b   c
#  / \
# d   e

edges: dict[str, list[str]] = {
    "a": ["c", "b"],
    "b": ["d", "e"],
    "c": [],
    "d": [],
    "e": [],
}

vertices: list[str] = ["a", "b", "c", "d", "e"]


# 从指定节点开始，对 DAG 进行拓扑排序
def topological_sort(start: str, visited: list[str], sort: list[str]) -> list[str]:
    """
    对有向无环图进行拓扑排序。

    >>> topological_sort('a', [], [])
    ['c', 'd', 'e', 'b', 'a']

    >>> topological_sort("a", "b", "c")
    Traceback (most recent call last):
        ...
    ValueError: visited must be a list

    >>> topological_sort("a", [], "c")
    Traceback (most recent call last):
        ...
    ValueError: sort must be a list
    """
    if not isinstance(visited, list):
        raise ValueError("visited must be a list")
    if not isinstance(sort, list):
        raise ValueError("sort must be a list")
    current = start
    # 将当前节点标记为已访问
    visited.append(current)
    # 当前节点的所有邻居列表
    neighbors = edges[current]

    # 遍历当前节点的所有邻居
    for neighbor in neighbors:
        # 递归访问每个尚未访问的邻居
        if neighbor not in visited:
            sort = topological_sort(neighbor, visited, sort)

    # 访问所有邻居后，将当前节点加入排序结果列表
    sort.append(current)

    # 若仍有未访问的节点（不连通的分量）
    if len(visited) != len(vertices):
        for vertex in vertices:
            if vertex not in visited:
                sort = topological_sort(vertex, visited, sort)

    # 返回排序后的列表
    return sort


if __name__ == "__main__":
    # 从节点 "a" 开始拓扑排序（得到自底向上的顺序）
    sort = topological_sort("a", [], [])

    # 反转列表，得到正确的拓扑顺序（自顶向下）
    sort.reverse()
    print(sort)
