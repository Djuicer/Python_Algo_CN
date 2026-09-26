import numpy as np


def invert_matrix(matrix: list[list[float]]) -> list[list[float]]:
    """
    使用 NumPy 返回方阵的逆矩阵。

    参数：
    matrix (list[list[float]]): 方阵。

    返回：
    list[list[float]]: 若矩阵可逆则返回逆矩阵，否则抛出错误。

    ``numpy.linalg.inv`` 返回的精确浮点表示可能因平台和 BLAS/LAPACK 后端而略有
    差异（例如 ``0.6`` 与 ``0.6000000000000001``），因此下方 doctest 会对结果
    取整，使预期输出保持确定。

    >>> [[round(x, 6) for x in row] for row in invert_matrix([[4.0, 7.0], [2.0, 6.0]])]
    [[0.6, -0.7], [-0.2, 0.4]]
    >>> [[round(x, 6) for x in row] for row in invert_matrix([[1.0, 0.0], [0.0, 2.0]])]
    [[1.0, 0.0], [0.0, 0.5]]
    >>> invert_matrix([[1.0, 2.0], [0.0, 0.0]])
    Traceback (most recent call last):
        ...
    ValueError: Matrix is not invertible
    """
    np_matrix = np.array(matrix)

    try:
        inv_matrix = np.linalg.inv(np_matrix)
    except np.linalg.LinAlgError:
        raise ValueError("Matrix is not invertible")

    return inv_matrix.tolist()


if __name__ == "__main__":
    mat = [[4.0, 7.0], [2.0, 6.0]]
    print("Original Matrix:")
    print(mat)
    print("Inverted Matrix:")
    print(invert_matrix(mat))
