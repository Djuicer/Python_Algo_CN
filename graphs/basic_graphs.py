from collections import deque


def _input(message):
    return input(message).strip().split(" ")


def initialize_unweighted_directed_graph(
    node_count: int, edge_count: int
) -> dict[int, list[int]]:
    graph: dict[int, list[int]] = {}
    for i in range(node_count):
        graph[i + 1] = []

    for e in range(edge_count):
        x, y = (int(i) for i in _input(f"Edge {e + 1}: <node1> <node2> "))
        graph[x].append(y)
    return graph


def initialize_unweighted_undirected_graph(
    node_count: int, edge_count: int
) -> dict[int, list[int]]:
    graph: dict[int, list[int]] = {}
    for i in range(node_count):
        graph[i + 1] = []

    for e in range(edge_count):
        x, y = (int(i) for i in _input(f"Edge {e + 1}: <node1> <node2> "))
        graph[x].append(y)
        graph[y].append(x)
    return graph


def initialize_weighted_undirected_graph(
    node_count: int, edge_count: int
) -> dict[int, list[tuple[int, int]]]:
    graph: dict[int, list[tuple[int, int]]] = {}
    for i in range(node_count):
        graph[i + 1] = []

    for e in range(edge_count):
        x, y, w = (int(i) for i in _input(f"Edge {e + 1}: <node1> <node2> <weight> "))
        graph[x].append((y, w))
        graph[y].append((x, w))
    return graph


if __name__ == "__main__":
    n, m = (int(i) for i in _input("Number of nodes and edges: "))

    graph_choice = int(
        _input(
            "Press 1 or 2 or 3 \n"
            "1. Unweighted directed \n"
            "2. Unweighted undirected \n"
            "3. Weighted undirected \n"
        )[0]
    )

    g = {
        1: initialize_unweighted_directed_graph,
        2: initialize_unweighted_undirected_graph,
        3: initialize_weighted_undirected_graph,
    }[graph_choice](n, m)


"""
--------------------------------------------------------------------------------
    深度优先搜索。
        Args : G - 边字典
                s - 起始节点
        Vars : vis - 访问过的节点集
                S - 遍历堆栈
--------------------------------------------------------------------------------
"""


def dfs(g, s) -> None:
    """
    >>> dfs({1: [2, 3], 2: [4, 5], 3: [], 4: [], 5: []}, 1)
    1
    2
    4
    5
    3
    """
    vis, _s = {s}, [s]
    print(s)
    while _s:
        flag = 0
        for i in g[_s[-1]]:
            if i not in vis:
                _s.append(i)
                vis.add(i)
                flag = 1
                print(i)
                break
        if not flag:
            _s.pop()


"""
--------------------------------------------------------------------------------
    广度优先搜索。
        Args : G - 边字典
                s - 起始节点
        Vars : vis - 访问过的节点集
                Q - 遍历堆栈
--------------------------------------------------------------------------------
"""


def bfs(g, s) -> None:
    """
    >>> bfs({1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [], 5: [8], 6: [], 7: [], 8: []}, 1)
    1
    2
    3
    4
    5
    6
    7
    8
    """
    vis, q = {s}, deque([s])
    print(s)
    while q:
        u = q.popleft()
        for v in g[u]:
            if v not in vis:
                vis.add(v)
                q.append(v)
                print(v)


"""
--------------------------------------------------------------------------------
    Dijkstra最短路径算法
        Args : G - 边字典
                s - 起始节点
        Vars : dist - 存储从 s 到每个其他节点的最短距离的字典
                已知 - 已知节点集
                path - 路径中的前一个节点
--------------------------------------------------------------------------------
"""


def dijk(g, s) -> None:
    """
    >>> dijk({
    ...     1: [(2, 7), (3, 9), (6, 14)],
    ...     2: [(1, 7), (3, 10), (4, 15)],
    ...     3: [(1, 9), (2, 10), (4, 11), (6, 2)],
    ...     4: [(2, 15), (3, 11), (5, 6)],
    ...     5: [(4, 6), (6, 9)],
    ...     6: [(1, 14), (3, 2), (5, 9)]
    ... }, 1)
    7
    9
    11
    20
    20
    """
    dist, known, path = {s: 0}, set(), {s: 0}
    while True:
        if len(known) == len(g) - 1:
            break
        mini = 100000
        for key, value in dist.items():
            if key not in known and value < mini:
                mini = value
                u = key
        known.add(u)
        for v in g[u]:
            if v[0] not in known and dist[u] + v[1] < dist.get(v[0], 100000):
                dist[v[0]] = dist[u] + v[1]
                path[v[0]] = u
    for key, value in dist.items():
        if key != s:
            print(value)


"""
--------------------------------------------------------------------------------
    拓扑排序
--------------------------------------------------------------------------------
"""


def topo(g, ind=None, q=None) -> None:
    """
    对有向无环图执行拓扑排序。

    >>> topo({1: [2, 3], 2: [4], 3: [4], 4: []})
    1
    2
    3
    4
    """
    if q is None:
        q = [1]
    if ind is None:
        ind = [0] * (len(g) + 1)  # 由于其他索引被忽略
        for u in g:
            for v in g[u]:
                ind[v] += 1
        q = deque()
        for i in g:
            if ind[i] == 0:
                q.append(i)
    if len(q) == 0:
        return
    v = q.popleft()
    print(v)
    for w in g[v]:
        ind[w] -= 1
        if ind[w] == 0:
            q.append(w)
    topo(g, ind, q)


"""
--------------------------------------------------------------------------------
    读取邻接矩阵
--------------------------------------------------------------------------------
"""


def adjm():
    r"""
    读取邻接矩阵

    参数：
        None

    返回：
        tuple：包含边列表和边数的元组

    例子：
    >>> # Simulate user input for 3 nodes
    >>> input_data = "4\n0 1 0 1\n1 0 1 0\n0 1 0 1\n1 0 1 0\n"
    >>> import sys,io
    >>> original_input = sys.stdin
    >>> sys.stdin = io.StringIO(input_data)  # Redirect stdin for testing
    >>> adjm()
    ([(0, 1, 0, 1), (1, 0, 1, 0), (0, 1, 0, 1), (1, 0, 1, 0)], 4)
    >>> sys.stdin = original_input  # Restore original stdin
    """
    n = int(input().strip())
    a = []
    for _ in range(n):
        a.append(tuple(map(int, input().strip().split())))
    return a, n


"""
--------------------------------------------------------------------------------
    弗洛伊德·沃歇尔算法
        Args : G - 边字典
                s - 起始节点
        Vars : dist - 存储从 s 到每个其他节点的最短距离的字典
                已知 - 已知节点集
                path - 路径中的前一个节点

--------------------------------------------------------------------------------
"""


def floyd_warshall(a_and_n) -> None:
    """
    用于计算所有对最短路径的 Floyd-Warshall 算法。

    参数：
        a_and_n（元组）：元组 (a, n)，其中
            a 是一个 N x N 邻接矩阵（列表的列表），
            n 是节点数。

    例子：
    >>> floyd_warshall(([
    ...     [0, 5, float('inf')],
    ...     [50, 0, 10],
    ...     [float('inf'), float('inf'), 0]
    ... ], 3))
    [[0, 5, 15], [50, 0, 10], [inf, inf, 0]]
    """

    (a, n) = a_and_n
    dist = [row[:] for row in a]  # 创建矩阵一个最重要的副本
    path = [[0] * n for i in range(n)]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    path[i][k] = k  # 可能的错误

    print(dist)


"""
--------------------------------------------------------------------------------
    Prim 的 MST 算法
        Args : G - 边字典
                s - 起始节点
        Vars : dist - 存储从 s 到最近节点的最短距离的字典
                已知 - 已知节点集
                path - 路径中的前一个节点
--------------------------------------------------------------------------------
"""


def prim(g, s):
    dist, known, path = {s: 0}, set(), {s: 0}
    while True:
        if len(known) == len(g) - 1:
            break
        mini = 100000
        for key, value in dist.items():
            if key not in known and value < mini:
                mini = value
                u = key
        known.add(u)
        for v in g[u]:
            if v[0] not in known and v[1] < dist.get(v[0], 100000):
                dist[v[0]] = v[1]
                path[v[0]] = u
    return dist


"""
--------------------------------------------------------------------------------
    接受边列表
        变量：n - 节点数
                m - 边数
        返回：l - 边列表
                n - 节点数
--------------------------------------------------------------------------------
"""


def edglist():
    r"""
    从用户处获取边和边数

    参数：
        None

    返回：
        tuple：包含边列表和边数的元组

    例子：
    >>> # Simulate user input for 3 edges and 4 vertices: (1, 2), (2, 3), (3, 4)
    >>> input_data = "4 3\n1 2\n2 3\n3 4\n"
    >>> import sys,io
    >>> original_input = sys.stdin
    >>> sys.stdin = io.StringIO(input_data)  # Redirect stdin for testing
    >>> edglist()
    ([(1, 2), (2, 3), (3, 4)], 4)
    >>> sys.stdin = original_input  # Restore original stdin
    """
    n, m = tuple(map(int, input().split(" ")))
    edges = []
    for _ in range(m):
        edges.append(tuple(map(int, input().split(" "))))
    return edges, n


"""
--------------------------------------------------------------------------------
    Kruskal 的 MST 算法
        参数：E - 边列表
                n - 节点数
        Vars : s - 所有节点的集合作为唯一的不相交集合（最初）
--------------------------------------------------------------------------------
"""


def krusk(e_and_n) -> None:
    """
    根据距离对边进行排序
    """
    (e, n) = e_and_n
    e.sort(reverse=True, key=lambda x: x[2])
    s = [{i} for i in range(1, n + 1)]
    while True:
        if len(s) == 1:
            break
        print(s)
        x = e.pop()
        for i in range(len(s)):
            if x[0] in s[i]:
                break
        for j in range(len(s)):
            if x[1] in s[j]:
                if i == j:
                    break
                s[j].update(s[i])
                s.pop(i)
                break


def find_isolated_nodes(graph):
    """
    找到图中的孤立节点

    参数：
    graph (dict)：表示图的字典。

    返回：
    list：孤立节点的列表。

    示例：
    >>> graph1 = {1: [2, 3], 2: [1, 3], 3: [1, 2], 4: []}
    >>> find_isolated_nodes(graph1)
    [4]

    >>> graph2 = {'A': ['B', 'C'], 'B': ['A'], 'C': ['A'], 'D': []}
    >>> find_isolated_nodes(graph2)
    ['D']

    >>> graph3 = {'X': [], 'Y': [], 'Z': []}
    >>> find_isolated_nodes(graph3)
    ['X', 'Y', 'Z']

    >>> graph4 = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    >>> find_isolated_nodes(graph4)
    []

    >>> graph5 = {}
    >>> find_isolated_nodes(graph5)
    []
    """
    isolated = []
    for node in graph:
        if not graph[node]:
            isolated.append(node)
    return isolated
