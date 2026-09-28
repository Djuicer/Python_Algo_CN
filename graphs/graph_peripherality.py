"""
用于确定外围和最远节点的图外围和远度算法
在图表中。

该模块提供计算外围节点和最远节点的函数
基于图论距离测量的加权图。外围节点
最大化到所有其他可到达节点的最大最短路径距离
(eccentricity), while the far node maximizes the sum of shortest-path distances to
所有其他可到达的节点（距离）。

问题描述：
给定一个带权图 G = (V, E)，其中 V 是顶点集合，E 是集合
具有表示节点之间距离的正权重的边，确定：

- Peripheral Node: The node with maximal eccentricity. The eccentricity of a node v
  定义为v与从v可到达的任何其他节点之间的最大距离。

- Far Node: The node with maximal farness. Farness of a node v is the sum of the
  从v到所有其他可到达节点的最短路径距离。

实现的算法：
- Floyd-Warshall Algorithm for All-Pairs Shortest Paths.
- Calculation of Eccentricity and Farness for identifying Peripheral and Far nodes.

算法说明：

Floyd-Warshall 算法（伪代码，代码保持不变）：
---------------------------------------
for k from 1 to N:
    for i from 1 to N:
        for j from 1 to N:
            if distance[i][j] > distance[i][k] + distance[k][j]:
                distance[i][j] = distance[i][k] + distance[k][j]

外围和远端节点计算：
------------------------------------
对于每个节点i：
    - Eccentricity[i] = maximum distance from node i to any other reachable node.
    - Farness[i] = sum of distances from node i to all reachable nodes.

选择：
    - Peripheral Node: node with maximal eccentricity.
    - Far Node: node with maximal farness.

References:
- Floyd-Warshall Algorithm: https://en.wikipedia.org/wiki/Floyd-Warshall_algorithm
- Eccentricity and Farness: https://en.wikipedia.org/wiki/Distance_(graph_theory)

应用示例：
这些算法可以应用于网络分析，例如识别最
网络内的远程节点，分析通信延迟或规划
网络边界的基础设施。
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


def find_peripheral_node(
    eccentricities: list[tuple[int, float]],
) -> tuple[int, float]:
    """识别可达节点中偏心率最大的节点。

    参数：
        eccentricities：元组列表（节点索引、偏心率）。

    返回：
        具有最大偏心节点的节点及其值。返回 (-1, inf) 如果
        未找到有效节点。
    """
    return max(
        eccentricities,
        key=lambda node_eccentricity: (
            node_eccentricity[1],  # 优先考虑最高偏心率
            -node_eccentricity[0],  # 对于相同的值，优先选择索引较高的节点
        ),
        default=(-1, float("inf")),
    )


def find_far_node(farnesses: list[tuple[int, float]]) -> tuple[int, float]:
    """识别可到达节点中距离最大的节点。

    参数：
        farnesses：元组列表（节点索引、farness）。

    返回：
        距离最大的节点及其值。返回 (-1, inf) 如果
        未找到有效节点。
    """
    return max(
        farnesses,
        key=lambda node_farness: (
            node_farness[1],  # 优先考虑最高距离
            -node_farness[0],  # 对于相同的值，优先选择索引较高的节点
        ),
        default=(-1, float("inf")),
    )


def find_peripheral_and_far_node(
    distance_matrix: np.ndarray,
) -> tuple[tuple[int, float], tuple[int, float]]:
    """根据最短路径距离确定外围节点和远端节点。

    对于每个节点，计算其偏心率和距离（到所有节点的距离之和）
    可达节点）。识别外围节点（最大偏心率）和
    最远节点（最大距离）。

    参数：
        distance_matrix：表示最短路径距离的numpy.ndarray
                         所有节点对之间。

    返回：
        一个元组包含：
            - peripheral_node: A tuple (node index, eccentricity) for the node with
              最大偏心率。
            - far_node: A tuple (node index, farness) for the node with maximal
              距离（最短路径距离之和）。
    """
    num_nodes: int = len(distance_matrix)

    # 处理单节点图
    if num_nodes == 1:
        return (0, 0.0), (0, 0.0)

    eccentricities: list[tuple[int, float]] = []
    farnesses: list[tuple[int, float]] = []
    all_disconnected = True  # 假设所有设备均已断开连接，除非另有证明

    for i in range(num_nodes):
        reachable_distances = get_reachable_distances(distance_matrix[i])

        if reachable_distances.size == 0:
            # 完全断开的节点
            eccentricity = float("inf")
            farness = float("inf")
        else:
            all_disconnected = False  # 如果任何节点有可到达的节点，我们更新它
            eccentricity = float(np.max(reachable_distances))
            farness = float(np.sum(reachable_distances))

        eccentricities.append((i, eccentricity))
        farnesses.append((i, farness))

    # 如果所有节点都断开连接，我们返回 (-1, inf)
    if all_disconnected:
        return (-1, float("inf")), (-1, float("inf"))

    peripheral_node = find_peripheral_node(eccentricities)
    far_node = find_far_node(farnesses)

    return peripheral_node, far_node


# 测试用例作为文档测试包含在内
def test_single_node() -> None:
    """
    使用单个节点测试图。

    >>> graph = {0: []}
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> peripheral_node, far_node = find_peripheral_and_far_node(distance_matrix)
    >>> peripheral_node
    (0, 0.0)
    >>> far_node
    (0, 0.0)
    """


def test_two_nodes_positive_weight() -> None:
    """
    测试具有通过正权重连接的两个节点的图。

    >>> graph = {0: [(1, 5.0)], 1: [(0, 5.0)]}
    >>> distance_matrix = floyd_warshall_algorithm(graph)
    >>> peripheral_node, far_node = find_peripheral_and_far_node(distance_matrix)
    >>> peripheral_node
    (0, 5.0)
    >>> far_node
    (0, 5.0)
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
    >>> peripheral_node, far_node = find_peripheral_and_far_node(distance_matrix)
    >>> peripheral_node
    (0, 1.0)
    >>> far_node
    (0, 2.0)
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
    >>> peripheral_node, far_node = find_peripheral_and_far_node(distance_matrix)
    >>> peripheral_node
    (4, inf)
    >>> far_node
    (4, inf)
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
    >>> peripheral_node, far_node = find_peripheral_and_far_node(distance_matrix)
    >>> peripheral_node
    (0, 2.0)
    >>> far_node
    (0, 3.0)
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
    >>> peripheral_node, far_node = find_peripheral_and_far_node(distance_matrix)
    >>> peripheral_node
    (3, inf)
    >>> far_node
    (3, inf)
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
    >>> peripheral_node, far_node = find_peripheral_and_far_node(distance_matrix)
    >>> peripheral_node
    (-1, inf)
    >>> far_node
    (-1, inf)
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
    >>> peripheral_node, far_node = find_peripheral_and_far_node(distance_matrix)
    >>> peripheral_node[0] is not None  # Ensure it found a peripheral node
    True
    >>> far_node[0] is not None  # Ensure it found a far node
    True
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
