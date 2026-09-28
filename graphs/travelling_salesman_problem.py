"""旅行商问题（TSP）"""

import itertools
import math


class InvalidGraphError(ValueError):
    """无效图输入的自定义错误。"""


def euclidean_distance(point1: list[float], point2: list[float]) -> float:
    """
    计算2D空间中两点之间的欧几里德距离。

    :param point1: 第一个点的坐标 [x, y]
    :param point2: 第二个点的坐标[x, y]
    :return: 欧氏之间两点的距离

    >>> euclidean_distance([0, 0], [3, 4])
    5.0
    >>> euclidean_distance([1, 1], [1, 1])
    0.0
    >>> euclidean_distance([1, 1], ['a', 1])
    Traceback (most recent call last):
        ...
    ValueError: Invalid input: Points must be numerical coordinates
    """
    try:
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    except TypeError:
        raise ValueError("Invalid input: Points must be numerical coordinates")


def validate_graph(graph_points: dict[str, list[float]]) -> None:
    """
    验证输入图以确保其具有有效的节点和坐标。

    :param graph_points: 一个字典，其中键是节点名称，
                         值为2D坐标，如[x, y]
    ：引发InvalidGraphError：如果图点无效

    >>> validate_graph({"A": [10, 20], "B": [30, 21], "C": [15, 35]})  # Valid graph
    >>> validate_graph(  # doctest: +IGNORE_EXCEPTION_DETAIL
    ...     {"A": [10, 20], "B": [30, "invalid"], "C": [15, 35]}
    ... )
    Traceback (most recent call last):
        ...
    InvalidGraphError: Each node must have a valid 2D coordinate [x, y]

    >>> validate_graph([10, 20])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    InvalidGraphError: Graph must be a dictionary with node names and coordinates

    >>> validate_graph(  # doctest: +IGNORE_EXCEPTION_DETAIL
    ...     {"A": [10, 20], "B": [30, 21], "C": [15]}
    ... )  # Missing coordinate
    Traceback (most recent call last):
        ...
    InvalidGraphError: Each node must have a valid 2D coordinate [x, y]
    """
    if not isinstance(graph_points, dict):
        raise InvalidGraphError(
            "Graph must be a dictionary with node names and coordinates"
        )

    for node, coordinates in graph_points.items():
        if (
            not isinstance(node, str)
            or not isinstance(coordinates, list)
            or len(coordinates) != 2
            or not all(isinstance(c, (int, float)) for c in coordinates)
        ):
            raise InvalidGraphError("Each node must have a valid 2D coordinate [x, y]")


# 蛮力方法中的TSP
def travelling_salesman_brute_force(
    graph_points: dict[str, list[float]],
) -> tuple[list[str], float]:
    """
    使用蛮力解决旅行商问题。

    :param graph_points: 节点及其坐标字典 {node: [x, y]}
    :return: 最短路径及其总距离

    >>> graph = {"A": [10, 20], "B": [30, 21], "C": [15, 35]}
    >>> travelling_salesman_brute_force(graph)
    (['A', 'B', 'C', 'A'], 56.35465722402588)
    """
    validate_graph(graph_points)

    nodes = list(graph_points.keys())  # 提取节点名称（键）

    # 有效 TSP 至少应有 2 个节点
    if len(nodes) < 2:
        raise InvalidGraphError("Graph must have at least two nodes")

    min_path = []  # 存储最短路径的列表
    min_distance = float("inf")  # 初始化最小距离到无穷远

    start_node = nodes[0]
    other_nodes = nodes[1:]

    # 迭代其他节点的所有排列
    for perm in itertools.permutations(other_nodes):
        path = [start_node, *perm, start_node]

        # 计算总距离
        total_distance = sum(
            euclidean_distance(graph_points[path[i]], graph_points[path[i + 1]])
            for i in range(len(path) - 1)
        )

        # 如果找到更短的路径，则更新最小距离
        if total_distance < min_distance:
            min_distance = total_distance
            min_path = path

    return min_path, min_distance


# TSP动态规划方法
def travelling_salesman_dynamic_programming(
    graph_points: dict[str, list[float]],
) -> tuple[list[str], float]:
    """
    使用动态规划解决旅行商问题。

    :param graph_points: 节点及其坐标字典 {node: [x, y]}
    :return: 最短路径及其总距离

    >>> graph = {"A": [10, 20], "B": [30, 21], "C": [15, 35]}
    >>> travelling_salesman_dynamic_programming(graph)
    (['A', 'C', 'B', 'A'], 56.35465722402587)
    """
    validate_graph(graph_points)

    n = len(graph_points)  # 提取节点名称（键）

    # 有效 TSP 至少应有 2 个节点
    if n < 2:
        raise InvalidGraphError("Graph must have at least two nodes")

    nodes = list(graph_points.keys())  # 提取节点名称（键）

    # 使用浮点值初始化距离矩阵
    dist = [
        [
            euclidean_distance(graph_points[nodes[i]], graph_points[nodes[j]])
            for j in range(n)
        ]
        for i in range(n)
    ]

    # 初始化一个无穷大的动态规划表
    dp = [[float("inf")] * n for _ in range(1 << n)]
    dp[1][0] = 0  # 唯一访问过的节点是从节点0开始的

    # 迭代访问节点的所有掩码
    for mask in range(1 << n):
        for u in range(n):
            # 如果当前节点'u'被访问
            if mask & (1 << u):
                # 遍历节点 'v' 使得 u->v
                for v in range(n):
                    if mask & (1 << v) == 0:  # 如果 v 没有被访问过
                        next_mask = mask | (1 << v)  # 更新掩码以包含“v”
                        # 用最小距离更新动态规划表
                        dp[next_mask][v] = min(
                            dp[next_mask][v], dp[mask][u] + dist[u][v]
                        )

    final_mask = (1 << n) - 1
    min_cost = float("inf")
    end_node = -1  # 跟踪最优路径中的最后一个节点

    for u in range(1, n):
        if min_cost > dp[final_mask][u] + dist[u][0]:
            min_cost = dp[final_mask][u] + dist[u][0]
            end_node = u

    path = []
    mask = final_mask
    while end_node != 0:
        path.append(nodes[end_node])
        for u in range(n):
            # 如果当前状态对应于访问端节点之前的最佳状态
            if (
                mask & (1 << u)
                and dp[mask][end_node]
                == dp[mask ^ (1 << end_node)][u] + dist[u][end_node]
            ):
                mask ^= 1 << end_node  # 更新掩码以删除末端节点
                end_node = u  # 将前一个节点设置为结束节点
                break

    path.append(nodes[0])  # 自下而上的顺序
    path.reverse()  # 自上而下的顺序
    path.append(nodes[0])

    return path, min_cost


# 演示图
#        C (15, 35)
#        |
#        |
#        |
# F (5, 15) --- A (10, 20)
#        |         |
#        |         |
#        |         |
#        |         |
# E (25, 5) --- B (30, 21)
#        |
#        |
#        |
#       D (40, 10)
#        |
#        |
#        |
#       G (50, 25)


if __name__ == "__main__":
    demo_graph = {
        "A": [10.0, 20.0],
        "B": [30.0, 21.0],
        "C": [15.0, 35.0],
        "D": [40.0, 10.0],
        "E": [25.0, 5.0],
        "F": [5.0, 15.0],
        "G": [50.0, 25.0],
    }

    # 暴力破解
    brute_force_result = travelling_salesman_brute_force(demo_graph)
    print(f"Brute force result: {brute_force_result}")

    # 动态规划
    dp_result = travelling_salesman_dynamic_programming(demo_graph)
    print(f"Dynamic programming result: {dp_result}")
