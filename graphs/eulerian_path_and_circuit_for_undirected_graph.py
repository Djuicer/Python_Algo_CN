# 欧拉路径是图中的一条路径，它只访问每条边一次。
# 欧拉回路是一条欧拉路径，其起点和终点相同
# 顶点。
# 时间复杂度为O(V+E)
# 空间复杂度为O(VE)


def dfs(u, graph, visited_edge, path=None):
    """
    使用 dfs 寻找欧拉路径
    参数：
        u：start_node
        graph：要检查的图表
        visited_edge：指定节点是否被访问过
        路径：可选路径参数

    返回：
        小路

    例子：
        >>> visited_edge = [[False] * 11 for _ in range(11)]
        >>> dfs(1, {1: [2, 3], 2: [1, 3], 3: [1, 2]}, visited_edge)
        [1, 2, 3, 1]
        >>> dfs(5, {1: [2, 3, 4], 2: [1, 3], 3: [1], 4: [1, 5], 5: [4]}, visited_edge)
        [5, 4, 1]
        >>> dfs(1, {1: [], 2: [], 3: [1, 2]}, visited_edge)
        [1]
        >>> dfs(1, {1: [], 2: []}, visited_edge)
        [1]
        >>> dfs(1, {1: [], 2: []}, visited_edge, [1, 3])
        [1, 3, 1]
    """
    path = (path or []) + [u]
    for v in graph[u]:
        if visited_edge[u][v] is False:
            visited_edge[u][v], visited_edge[v][u] = True, True
            path = dfs(v, graph, visited_edge, path)
    return path


def check_circuit_or_path(graph, max_node):
    """
    用于检查图中是否有欧拉路径或电路

    参数：
        graph：要检查的图表
        max_node：要检查的最大节点

    返回：
        图的类型及其电路或路径

    例子：
        >>> check_circuit_or_path({1: [2, 3], 2: [1, 3], 3: [1, 2]}, 10)
        (1, -1)
        >>> check_circuit_or_path({1: [2, 3, 4], 2: [], 3: [1, 2], 4: [], 5: [4]}, 10)
        (2, 5)
        >>> check_circuit_or_path({1: [2, 3, 1], 2: [2], 3: [1, 3], 4: [1], 5: []}, 10)
        (3, 4)
        >>> check_circuit_or_path({1: [], 2: [], 3: [1, 2]}, 10)
        (1, -1)
        >>> check_circuit_or_path({1: [], 2: []}, 10)
        (1, -1)
    """
    odd_degree_nodes = 0
    odd_node = -1
    for i in range(max_node):
        if i not in graph:
            continue
        if len(graph[i]) % 2 == 1:
            odd_degree_nodes += 1
            odd_node = i
    if odd_degree_nodes == 0:
        return 1, odd_node
    if odd_degree_nodes == 2:
        return 2, odd_node
    return 3, odd_node


def check_euler(graph, max_node) -> None:
    """
    参数：
        graph：要检查的图表
        max_node：要检查的最大节点

    例子：
        >>> check_euler({1: [2, 3], 2: [1, 3], 3: [1, 2]}, 10)
        graph has a Euler cycle
        [1, 2, 3, 1]
        >>> check_euler({1: [2, 3, 4], 2: [1, 3], 3: [1, 2], 4: [1, 5], 5: [4]}, 10)
        graph has a Euler path
        [5, 4, 1, 2, 3, 1]
        >>> check_euler({1: [2, 3, 1], 2: [2, 3, 4], 3: [1, 3], 4: [1], 5: []}, 10)
        graph is not Eulerian
        no path
        >>> check_euler({1: [], 2: [], 3: [1, 2]}, 10)
        graph has a Euler cycle
        [1]
        >>> check_euler({1: [], 2: []}, 10)
        graph has a Euler cycle
        [1]
    """
    visited_edge = [[False for _ in range(max_node + 1)] for _ in range(max_node + 1)]
    check, odd_node = check_circuit_or_path(graph, max_node)
    if check == 3:
        print("graph is not Eulerian")
        print("no path")
        return
    start_node = 1
    if check == 2:
        start_node = odd_node
        print("graph has a Euler path")
    if check == 1:
        print("graph has a Euler cycle")
    path = dfs(start_node, graph, visited_edge)
    print(path)


def main() -> None:
    g1 = {1: [2, 3, 4], 2: [1, 3], 3: [1, 2], 4: [1, 5], 5: [4]}
    g2 = {1: [2, 3, 4, 5], 2: [1, 3], 3: [1, 2], 4: [1, 5], 5: [1, 4]}
    g3 = {1: [2, 3, 4], 2: [1, 3, 4], 3: [1, 2], 4: [1, 2, 5], 5: [4]}
    g4 = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    g5 = {
        1: [],
        2: [],
        # 所有度数均为零
    }
    max_node = 10
    check_euler(g1, max_node)
    check_euler(g2, max_node)
    check_euler(g3, max_node)
    check_euler(g4, max_node)
    check_euler(g5, max_node)


if __name__ == "__main__":
    main()

    import doctest

    doctest.testmod()
