from collections import defaultdict, deque


def is_bipartite_dfs(graph: dict[int, list[int]]) -> bool:
    """
    使用深度优先搜索（DFS）检查图是否是二分图。

    参数：
        `graph`：表示图的邻接表。

    返回：
        如果是二分图则返回 ``True``，否则返回 ``False``。

    检查图是否可以分为两组顶点，使得没有两个顶点
    同一集合内的顶点通过边连接。

    示例：

    >>> is_bipartite_dfs({0: [1, 2], 1: [0, 3], 2: [0, 4]})
    True
    >>> is_bipartite_dfs({0: [1, 2], 1: [0, 3], 2: [0, 1]})
    False
    >>> is_bipartite_dfs({})
    True
    >>> is_bipartite_dfs({0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]})
    True
    >>> is_bipartite_dfs({0: [1, 2, 3], 1: [0, 2], 2: [0, 1, 3], 3: [0, 2]})
    False
    >>> is_bipartite_dfs({0: [4], 1: [], 2: [4], 3: [4], 4: [0, 2, 3]})
    True
    >>> is_bipartite_dfs({0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2], 4: [0]})
    False
    >>> is_bipartite_dfs({7: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2], 4: [0]})
    False

    >>> is_bipartite_dfs({0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2], 9: [0]})
    False
    >>> is_bipartite_dfs({0: [-1, 3], 1: [0, -2]})
    False
    >>> is_bipartite_dfs({-1: [0, 2], 0: [-1, 1], 1: [0, 2], 2: [-1, 1]})
    True
    >>> is_bipartite_dfs({0.9: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]})
    True
    >>> is_bipartite_dfs({0: [1.0, 3.0], 1.0: [0, 2.0], 2.0: [1.0, 3.0], 3.0: [0, 2.0]})
    True
    >>> is_bipartite_dfs({"a": [1, 3], "b": [0, 2], "c": [1, 3], "d": [0, 2]})
    True
    >>> is_bipartite_dfs({0: ["b", "d"], 1: ["a", "c"], 2: ["b", "d"], 3: ["a", "c"]})
    True
    """

    def depth_first_search(node: int, color: int) -> bool:
        """
        从节点开始对图执行深度优先搜索(DFS)。

        参数：
            节点：当前访问的节点。
            color：分配给当前节点的颜色。

        返回：
            如果图是从当前节点开始的二分图，则为true，
            否则为假。
        """
        if visited[node] == -1:
            visited[node] = color
            if node not in graph:
                return True
            for neighbor in graph[node]:
                if not depth_first_search(neighbor, 1 - color):
                    return False
        return visited[node] == color

    visited: defaultdict[int, int] = defaultdict(lambda: -1)
    for node in graph:
        if visited[node] == -1 and not depth_first_search(node, 0):
            return False
    return True


def is_bipartite_bfs(graph: dict[int, list[int]]) -> bool:
    """
    使用广度优先搜索（BFS）检查图是否是二分图。

    参数：
        `graph`：表示图的邻接表。

    返回：
        如果是二分图则返回 ``True``，否则返回 ``False``。

    检查图是否可以分为两组顶点，使得没有两个顶点
    同一集合内的顶点通过边连接。

    示例：

    >>> is_bipartite_bfs({0: [1, 2], 1: [0, 3], 2: [0, 4]})
    True
    >>> is_bipartite_bfs({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    False
    >>> is_bipartite_bfs({})
    True
    >>> is_bipartite_bfs({0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]})
    True
    >>> is_bipartite_bfs({0: [1, 2, 3], 1: [0, 2], 2: [0, 1, 3], 3: [0, 2]})
    False
    >>> is_bipartite_bfs({0: [4], 1: [], 2: [4], 3: [4], 4: [0, 2, 3]})
    True
    >>> is_bipartite_bfs({0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2], 4: [0]})
    False
    >>> is_bipartite_bfs({7: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2], 4: [0]})
    False

    >>> is_bipartite_bfs({0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2], 9: [0]})
    False
    >>> is_bipartite_bfs({0: [-1, 3], 1: [0, -2]})
    False
    >>> is_bipartite_bfs({-1: [0, 2], 0: [-1, 1], 1: [0, 2], 2: [-1, 1]})
    True
    >>> is_bipartite_bfs({0.9: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]})
    True
    >>> is_bipartite_bfs({0: [1.0, 3.0], 1.0: [0, 2.0], 2.0: [1.0, 3.0], 3.0: [0, 2.0]})
    True
    >>> is_bipartite_bfs({"a": [1, 3], "b": [0, 2], "c": [1, 3], "d": [0, 2]})
    True
    >>> is_bipartite_bfs({0: ["b", "d"], 1: ["a", "c"], 2: ["b", "d"], 3: ["a", "c"]})
    True
    """
    visited: defaultdict[int, int] = defaultdict(lambda: -1)
    for node in graph:
        if visited[node] == -1:
            queue: deque[int] = deque()
            queue.append(node)
            visited[node] = 0
            while queue:
                curr_node = queue.popleft()
                if curr_node not in graph:
                    continue
                for neighbor in graph[curr_node]:
                    if visited[neighbor] == -1:
                        visited[neighbor] = 1 - visited[curr_node]
                        queue.append(neighbor)
                    elif visited[neighbor] == visited[curr_node]:
                        return False
    return True


if __name__ == "__main__":
    import doctest

    result = doctest.testmod()
    if result.failed:
        print(f"{result.failed} test(s) failed.")
    else:
        print("All tests passed!")
