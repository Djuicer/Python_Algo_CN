"""
用于确定图中的中心节点和中值节点的图中心性算法。

该模块提供计算加权中的中心节点和中值节点的函数
基于图论中心性度量的图。中心节点最小化
到所有其他可到达节点的最大最短路径距离（偏心率），而
中值节点最大化到所有节点的最短路径距离的倒数之和
其他可达节点（谐波接近中心性）。

问题描述：
给定一个权重图 G = (V, E)，其中 V 是顶点的集合，E 是
具有表示节点之间距离的正权重的边，确定：

- Central Node: The node with minimal eccentricity. The eccentricity of a node v is
  定义为v与可从v到达的任何其他节点之间的最大距离。

- Median Node: The node with maximal harmonic closeness centrality. The harmonic
  节点 v 的紧密中心性是最短路径的倒数之和
  从v到所有其他可到达节点的距离。

实现的算法：
- Floyd-Warshall Algorithm for All-Pairs Shortest Paths.
- Calculation of Eccentricity and Harmonic Closeness Centrality.

算法说明：

Floyd-Warshall 算法（伪代码，代码保持不变）：
---------------------------------------
for k from 1 to N:
    for i from 1 to N:
        for j from 1 to N:
            if distance[i][j] > distance[i][k] + distance[k][j]:
                distance[i][j] = distance[i][k] + distance[k][j]

中心节点和中值节点计算：
------------------------------------
对于每个节点i：
    - Eccentricity[i] = maximum distance from node i to any other reachable node.
    - Closeness[i] = sum of reciprocals of distances from node i to all reachable nodes.

选择：
    - Central Node: node with minimal eccentricity.
    - Median Node: node with maximal closeness.

References:
- https://en.wikipedia.org/wiki/Centrality
- Floyd-Warshall Algorithm: https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
- Closeness Centrality: https://en.wikipedia.org/wiki/Closeness_centrality

应用示例：
这些算法可以应用于现实世界的问题，例如确定最优
设施（例如应急响应中心）的位置，以最大限度地缩短响应时间
在一个网络内。通过识别中心或中间节点，组织可以使
有关资源配置的明智决策，以提高效率和可及性。
"""

import numpy as np


def initialize_distance_matrix(
    graph: dict[int, list[tuple[int, float]]], number_of_nodes: int
) -> np.ndarray:
    """初始化距离矩阵并验证边权重。

    参数：
        graph：表示为邻接列表的图。
        number_of_nodes：图的节点总数。

    返回：
        表示初始距离矩阵的numpy.ndarray。

    异常：
        ValueError：如果任一边的权重不是正数。
    """
    distance_matrix: np.ndarray = np.full((number_of_nodes, number_of_nodes), np.inf)
    np.fill_diagonal(distance_matrix, 0)

    for node_index, edges in graph.items():
        for neighbor_index, edge_weight in edges:
            if edge_weight <= 0:
                error_message: str = (
                    f"Edge weight must be positive. Found {edge_weight} between "
                    f"nodes {node_index} and {neighbor_index}."
                )
                raise ValueError(error_message)
            distance_matrix[node_index, neighbor_index] = edge_weight

    return distance_matrix


def floyd_warshall_algorithm(graph: dict[int, list[tuple[int, float]]]) -> np.ndarray:
    """使用 Floyd-Warshall 算法计算所有对最短路径。

    弗洛伊德-沃歇尔复杂性：
    --------------------------
    时间复杂度：O(N^3)，其中N是节点数。
    空间复杂度：O(N^2)，用于存储距离矩阵。

    参数：
        graph：表示为邻接列表的图。

    返回：
        所有节点对之间具有最短路径的距离矩阵。
    """
    number_of_nodes: int = len(graph)
    distance_matrix: np.ndarray = initialize_distance_matrix(graph, number_of_nodes)

    for k in range(number_of_nodes):
        # 使用广播就地更新距离矩阵
        distance_matrix[:] = np.minimum(
            distance_matrix,
            distance_matrix[:, k][:, np.newaxis] + distance_matrix[k, :],
        )

    return distance_matrix


def get_reachable_distances(distances: np.ndarray) -> np.ndarray:
    """过滤可达距离，排除无限值（不可到达的节点）。

    参数：
        distances：距特定节点的最短路径距离的数组。

    返回：
        仅到可到达节点的距离数组（有限值）。
    """
    return distances[np.isfinite(distances) & (distances != 0)]


def find_central_node(
    eccentricities: list[tuple[int, float]],
) -> tuple[int, float]:
    """识别可达节点中偏心率最小的节点。

    参数：
        eccentricities：元组列表（节点索引、偏心率）。

    返回：
        具有最小偏心节点的节点及其值。返回 (-1, inf) 如果
        未找到有效节点。
    """
    valid_eccentricities = [e for e in eccentricities if e[1] != float("inf")]
    return min(
        valid_eccentricities,
        key=lambda node_eccentricity: (node_eccentricity[1], node_eccentricity[0]),
        default=(-1, float("inf")),
    )


def find_median_node(closenesses: list[tuple[int, float]]) -> tuple[int, float]:
    """识别可到达节点中具有最大接近度的节点。

    参数：
        紧密度：元组列表（节点索引、紧密度中心性）。

    返回：
        具有最大紧密度的节点及其值。返回 (-1, inf) 如果
        未找到有效节点。
    """
    valid_closenesses = [c for c in closenesses if c[1] != float("inf")]
    return max(
        valid_closenesses,
        key=lambda node_closeness: (node_closeness[1], -node_closeness[0]),
        default=(-1, float("inf")),
    )


def find_central_and_median_node(
    distance_matrix: np.ndarray,
) -> tuple[tuple[int, float], tuple[int, float]]:
    """根据最短路径距离确定中心节点和中间节点。

    对于每个节点，计算其偏心率和谐波接近中心性，
    只考虑可达节点。然后，识别中心节点（最小
    偏心率）和中值节点（最大接近度）。

    参数：
        distance_matrix：表示最短路径距离的numpy.ndarray
                         所有节点对之间。

    返回：
        一个元组包含：
            - central_node: A tuple (node index, eccentricity) for the node with
              最小的偏心率。
            - median_node: A tuple (node index, closeness) for the node with maximal
              谐波接近中心性。
    """
    num_nodes: int = len(distance_matrix)

    # 单节点图案例
    if num_nodes == 1:
        return (0, 0.0), (0, 0.0)

    eccentricities: list[tuple[int, float]] = []
    closenesses: list[tuple[int, float]] = []

    for i in range(num_nodes):
        reachable_distances = get_reachable_distances(distance_matrix[i])

        if reachable_distances.size == 0:
            # 无可达节点，组件孤立
            eccentricity = float("inf")
            closeness = float("inf")
        else:
            # 计算可达节点的偏心率和接近度
            eccentricity = float(np.max(reachable_distances))
            closeness = float(np.sum(1 / reachable_distances))

        eccentricities.append((i, eccentricity))
        closenesses.append((i, closeness))

    central_node = find_central_node(eccentricities)
    median_node = find_median_node(closenesses)

    return central_node, median_node


# 测试用例作为文档测试包含在内
def test_single_node() -> None:
    """
    使用单个节点测试图。

    >>> graph = {0: []}
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> central_node, median_node = find_central_and_median_node(distance_matrix)
    >>> central_node
    (0, 0.0)
    >>> median_node
    (0, 0.0)
    """


def test_two_nodes_positive_weight() -> None:
    """
    测试具有通过正权重连接的两个节点的图。

    >>> graph = {0: [(1, 5.0)], 1: [(0, 5.0)]}
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> central_node, median_node = find_central_and_median_node(distance_matrix)
    >>> central_node
    (0, 5.0)
    >>> median_node
    (0, 0.2)
    """


def test_fully_connected_graph() -> None:
    """
    测试全连接图。

    >>> graph = {
    ...     0: [(1, 1.0), (2, 1.0)],
    ...     1: [(0, 1.0), (2, 1.0)],
    ...     2: [(0, 1.0), (1, 1.0)],
    ... }
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> central_node, median_node = find_central_and_median_node(distance_matrix)
    >>> central_node
    (0, 1.0)
    >>> median_node
    (0, 2.0)
    """


def test_directed_acyclic_graph() -> None:
    """
    测试有向无环图(DAG)。

    >>> graph = {
    ...     0: [(1, 1.0), (2, 2.0)],
    ...     1: [(3, 3.0)],
    ...     2: [(3, 1.0)],
    ...     3: []
    ... }
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> central_node, median_node = find_central_and_median_node(distance_matrix)
    >>> central_node
    (2, 1.0)
    >>> median_node
    (0, 1.8333333333333333)
    """


def test_disconnected_graph() -> None:
    """
    测试具有无法相互访问的节点的断开连接图。

    >>> graph = {
    ...     0: [],
    ...     1: [],
    ...     2: []
    ... }
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> central_node, median_node = find_central_and_median_node(distance_matrix)
    >>> central_node
    (-1, inf)
    >>> median_node
    (-1, inf)
    """


def test_graph_with_zero_weight() -> None:
    """
    权测试重重置的图，这会引发ValueError。

    >>> graph = {0: [(1, 0.0)], 1: []}
    >>> floyd_warshall_algorithm(graph)
    Traceback (most recent call last):
    ...
    ValueError: Edge weight must be positive. Found 0.0 between nodes 0 and 1.
    """


def test_graph_with_negative_weight() -> None:
    """
    具有测试负权重的图表，这应该会引发 ValueError。

    >>> graph = {0: [(1, -2.0)], 1: []}
    >>> floyd_warshall_algorithm(graph)
    Traceback (most recent call last):
    ...
    ValueError: Edge weight must be positive. Found -2.0 between nodes 0 and 1.
    """


def test_cyclic_graph() -> None:
    """
    测试节点之间存在循环的循环图。

    >>> graph = {
    ...     0: [(1, 1.0)],
    ...     1: [(2, 1.0)],
    ...     2: [(0, 1.0)]
    ... }
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> central_node, median_node = find_central_and_median_node(distance_matrix)
    >>> central_node
    (0, 2.0)
    >>> median_node
    (0, 1.5)
    """


def test_sparse_graph() -> None:
    """
    测试更大的稀疏图。

    >>> graph = {
    ...     0: [(1, 2.0)],
    ...     1: [(2, 3.0)],
    ...     2: [(3, 4.0)],
    ...     3: [(4, 5.0)],
    ...     4: []
    ... }
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> central_node, median_node = find_central_and_median_node(distance_matrix)
    >>> central_node
    (3, 5.0)
    >>> median_node
    (0, 0.8825396825396825)
    """


def test_large_fully_connected_graph() -> None:
    """
    使用随机权重测试更大的全连接图。

    >>> import random
    >>> random.seed(42)
    >>> number_of_nodes = 10
    >>> graph = {i: [(j, random.uniform(1, 10)) for j in
    ...          range(number_of_nodes) if i != j]
    ...          for i in range(number_of_nodes)}
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> central_node, median_node = find_central_and_median_node(distance_matrix)
    >>> central_node[0] is not None  # Ensure it found a central node
    True
    >>> median_node[0] is not None  # Ensure it found a median node
    True
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
