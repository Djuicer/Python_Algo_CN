"""
用于查找图的特征值和特征分析的 Lanczos 方法。

该练习模块估计了 Lanczos 方法的最大特征值
以及表示为图的对称矩阵的相应特征向量
邻接表。该方法通过转换来有效地处理大型稀疏矩阵
该图为三对角矩阵，其特征值和特征向量为
计算出来的。

主要功能：
- `find_lanczos_eigenvectors`: Computes the k largest eigenvalues and vectors.
- `lanczos_iteration`: Constructs the tridiagonal matrix and orthonormal basis vectors.
- `multiply_matrix_vector`: Multiplies an adjacency list graph with a vector.

复杂：
- Time: O(k * n), where k is the number of eigenvalues and n is the matrix size.
- Space: O(n), due to sparse representation and tridiagonal matrix structure.

进一步阅读：
- Lanczos Algorithm: https://en.wikipedia.org/wiki/Lanczos_algorithm
- Eigenvector Centrality: https://en.wikipedia.org/wiki/Eigenvector_centrality

用法示例：
给定一个由邻接表表示的图，`find_lanczos_eigenvectors`
函数返回最大特征值和特征向量。这可以用来
分析图的中心性。
"""

import numpy as np


def validate_adjacency_list(graph: list[list[int | None]]) -> None:
    """验证图的邻接列表格式。

    参数：
        图：列表的列表，其中每个子列表包含节点的邻居。

    异常：
        ValueError: If the graph is not a list of lists, or if any node has
                    无效的邻居（例如，超出范围或非整数值）。

    >>> validate_adjacency_list([[1, 2], [0], [0, 1]])
    >>> validate_adjacency_list([[]])  # No neighbors, valid case
    >>> validate_adjacency_list([[1], [2], [-1]])  # Invalid neighbor
    Traceback (most recent call last):
        ...
    ValueError: Invalid neighbor -1 in node 2 adjacency list.
    """
    if not isinstance(graph, list):
        raise ValueError("Graph should be a list of lists.")

    for node_index, neighbors in enumerate(graph):
        if not isinstance(neighbors, list):
            no_neighbors_message: str = (
                f"Node {node_index} should have a list of neighbors."
            )
            raise ValueError(no_neighbors_message)
        for neighbor_index in neighbors:
            if (
                not isinstance(neighbor_index, int)
                or neighbor_index < 0
                or neighbor_index >= len(graph)
            ):
                invalid_neighbor_message: str = (
                    f"Invalid neighbor {neighbor_index} in node {node_index} "
                    f"adjacency list."
                )
                raise ValueError(invalid_neighbor_message)


def lanczos_iteration(
    graph: list[list[int | None]], num_eigenvectors: int
) -> tuple[np.ndarray, np.ndarray]:
    """使用以下函数构造三对角矩阵和正交基向量
    兰佐斯法。

    参数：
        graph：表示为邻接列表列表的图。
        num_eigenvectors：最大特征值和特征提供的数量
                          来近似。

    返回：
        一个元组包含：
            - tridiagonal_matrix: A (num_eigenvectors x num_eigenvectors) symmetric
                                  矩阵。
            - orthonormal_basis: A (num_nodes x num_eigenvectors) matrix of orthonormal
                                 基向量。

    异常：
        ValueError: If num_eigenvectors is less than 1 or greater than the number of
                    节点。

    >>> graph = [[1, 2], [0, 2], [0, 1]]
    >>> T, Q = lanczos_iteration(graph, 2)
    >>> T.shape == (2, 2) and Q.shape == (3, 2)
    True
    """
    num_nodes: int = len(graph)
    if not (1 <= num_eigenvectors <= num_nodes):
        raise ValueError(
            "Number of eigenvectors must be between 1 and the number of "
            "nodes in the graph."
        )

    orthonormal_basis: np.ndarray = np.zeros((num_nodes, num_eigenvectors))
    tridiagonal_matrix: np.ndarray = np.zeros((num_eigenvectors, num_eigenvectors))

    rng = np.random.default_rng()
    initial_vector: np.ndarray = rng.random(num_nodes)
    initial_vector /= np.sqrt(np.dot(initial_vector, initial_vector))
    orthonormal_basis[:, 0] = initial_vector

    prev_beta: float = 0.0
    for iter_index in range(num_eigenvectors):
        result_vector: np.ndarray = multiply_matrix_vector(
            graph, orthonormal_basis[:, iter_index]
        )
        if iter_index > 0:
            result_vector -= prev_beta * orthonormal_basis[:, iter_index - 1]
        alpha_value: float = np.dot(orthonormal_basis[:, iter_index], result_vector)
        result_vector -= alpha_value * orthonormal_basis[:, iter_index]

        prev_beta = np.sqrt(np.dot(result_vector, result_vector))
        if iter_index < num_eigenvectors - 1 and prev_beta > 1e-10:
            orthonormal_basis[:, iter_index + 1] = result_vector / prev_beta
        tridiagonal_matrix[iter_index, iter_index] = alpha_value
        if iter_index < num_eigenvectors - 1:
            tridiagonal_matrix[iter_index, iter_index + 1] = prev_beta
            tridiagonal_matrix[iter_index + 1, iter_index] = prev_beta
    return tridiagonal_matrix, orthonormal_basis


def multiply_matrix_vector(
    graph: list[list[int | None]], vector: np.ndarray
) -> np.ndarray:
    """执行图的邻接列表表示与向量的乘法。

    参数：
        图：图的邻接表。
        向量：表示要相乘的向量的一维numpy内存。

    返回：
        表示邻接列表和正在处理的乘积的 numpy 数组。

    异常：
        ValueError: If the vector's length does not match the number of nodes in the
                    图。

    >>> multiply_matrix_vector([[1, 2], [0, 2], [0, 1]], np.array([1, 1, 1]))
    array([2., 2., 2.])
    >>> multiply_matrix_vector([[1, 2], [0, 2], [0, 1]], np.array([0, 1, 0]))
    array([1., 0., 1.])
    """
    num_nodes: int = len(graph)
    if vector.shape[0] != num_nodes:
        raise ValueError("Vector length must match the number of nodes in the graph.")

    result: np.ndarray = np.zeros(num_nodes)
    for node_index, neighbors in enumerate(graph):
        for neighbor_index in neighbors:
            result[node_index] += vector[neighbor_index]
    return result


def find_lanczos_eigenvectors(
    graph: list[list[int | None]], num_eigenvectors: int
) -> tuple[np.ndarray, np.ndarray]:
    """使用以下公式计算最大特征值及其相应的特征向量
    兰佐斯法。

    参数：
        图：作为邻接表列表的图。
        num_eigenvectors：要计算最大特征值和特征向量的数量。

    返回：
        一个元组包含：
            - eigenvalues: 1D array of the largest eigenvalues in descending order.
            - eigenvectors: 2D array where each column is an eigenvector corresponding
                            到一个特征值。

    异常：
        ValueError: If the graph format is invalid or num_eigenvectors is out of bounds.

    >>> eigenvalues, eigenvectors = find_lanczos_eigenvectors(
    ...     [[1, 2], [0, 2], [0, 1]], 2
    ... )
    >>> len(eigenvalues) == 2 and eigenvectors.shape[1] == 2
    True
    """
    validate_adjacency_list(graph)
    tridiagonal_matrix, orthonormal_basis = lanczos_iteration(graph, num_eigenvectors)
    eigenvalues, eigenvectors = np.linalg.eigh(tridiagonal_matrix)
    return eigenvalues[::-1], np.dot(orthonormal_basis, eigenvectors[:, ::-1])


def main() -> None:
    """
    用于使用doctests测试实现的主要驱动程序函数。
    """
    import doctest

    doctest.testmod()


if __name__ == "__main__":
    main()
