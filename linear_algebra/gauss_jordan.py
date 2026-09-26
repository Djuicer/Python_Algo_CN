# https://en.wikipedia.org/wiki/Gaussian_elimination
# https://en.wikipedia.org/wiki/Row_echelon_form

import numpy as np


def gauss_jordan(
    coefficients: np.ndarray, vertices: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    对方程组 Ax = b 执行高斯-约旦消元，将 A 化为简化行阶梯形（RREF），
    并相应变换 b。

    参数：
        coefficients: 表示系数矩阵 A 的二维 NumPy 数组。
        vertices: 表示右端项 b 的列向量（二维 NumPy 数组）。

    返回：
        包含以下内容的元组：
            - 矩阵 A 的 RREF
            - 变换后的右端项向量 b

    异常：
        ValueError: A 和 b 的形状不兼容时抛出。

    另请参阅：
        https://en.wikibooks.org/wiki/Linear_Algebra/Gauss-Jordan_Reduction

    示例：
        >>> import numpy as np
        >>> A = np.array([[1, 2, -1], [2, 4, -2], [3, 6, -3]])
        >>> b = np.array([[1], [2], [3]])
        >>> rref_A, rref_b = gauss_jordan(A, b)
        >>> np.allclose(rref_A, np.array([[1., 2., -1.], [0., 0., 0.], [0., 0., 0.]]))
        True
        >>> np.allclose(rref_b, np.array([[1.], [0.], [0.]]))
        True

    """
    if coefficients.ndim != 2 or vertices.ndim != 2:
        raise ValueError("Both inputs must be 2D arrays.")
    if coefficients.shape[0] != vertices.shape[0]:
        raise ValueError("Number of rows in coefficients and vertices must match.")

    coefficients = coefficients.astype(float).copy()
    vertices = vertices.astype(float).copy()
    rows, cols = coefficients.shape

    for col in range(cols):
        pivot_row = None
        for row in range(col, rows):
            if not np.isclose(coefficients[row, col], 0):
                pivot_row = row
                break

        if pivot_row is None:
            continue

        if pivot_row != col:
            coefficients[[col, pivot_row]] = coefficients[[pivot_row, col]]
            vertices[[col, pivot_row]] = vertices[[pivot_row, col]]

        pivot_val = coefficients[col, col]
        coefficients[col] /= pivot_val
        vertices[col] /= pivot_val

        for row in range(rows):
            if row == col:
                continue
            factor = coefficients[row, col]
            coefficients[row] -= factor * coefficients[col]
            vertices[row] -= factor * vertices[col]

    return coefficients, vertices


if __name__ == "__main__":
    import doctest

    doctest.testmod()
