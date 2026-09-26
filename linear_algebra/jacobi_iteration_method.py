"""
雅可比迭代法（Jacobi Iteration Method）- https://en.wikipedia.org/wiki/Jacobi_method
"""

from __future__ import annotations

import numpy as np
from numpy import float64
from numpy.typing import NDArray


# 求解线性方程组的方法
def jacobi_iteration_method(
    coefficient_matrix: NDArray[float64],
    constant_matrix: NDArray[float64],
    init_val: list[float],
    iterations: int,
) -> list[float]:
    """
    雅可比迭代法：
    一种求解严格对角占优线性方程组的迭代算法。

    4x1 +  x2 +  x3 =  2
     x1 + 5x2 + 2x3 = -6
     x1 + 2x2 + 4x3 = -4

    x_init = [0.5, -0.5 , -0.5]

    示例：

    >>> coefficient = np.array([[4, 1, 1], [1, 5, 2], [1, 2, 4]])
    >>> constant = np.array([[2], [-6], [-4]])
    >>> init_val = [0.5, -0.5, -0.5]
    >>> iterations = 3
    >>> jacobi_iteration_method(coefficient, constant, init_val, iterations)
    [0.909375, -1.14375, -0.7484375]


    >>> coefficient = np.array([[4, 1, 1], [1, 5, 2]])
    >>> constant = np.array([[2], [-6], [-4]])
    >>> init_val = [0.5, -0.5, -0.5]
    >>> iterations = 3
    >>> jacobi_iteration_method(coefficient, constant, init_val, iterations)
    Traceback (most recent call last):
        ...
    ValueError: Coefficient matrix dimensions must be nxn but received 2x3

    >>> coefficient = np.array([[4, 1, 1], [1, 5, 2], [1, 2, 4]])
    >>> constant = np.array([[2], [-6]])
    >>> init_val = [0.5, -0.5, -0.5]
    >>> iterations = 3
    >>> jacobi_iteration_method(
    ...     coefficient, constant, init_val, iterations
    ... )  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Coefficient and constant matrices dimensions must be nxn and nx1 but
                received 3x3 and 2x1

    >>> coefficient = np.array([[4, 1, 1], [1, 5, 2], [1, 2, 4]])
    >>> constant = np.array([[2], [-6], [-4]])
    >>> init_val = [0.5, -0.5]
    >>> iterations = 3
    >>> jacobi_iteration_method(
    ...     coefficient, constant, init_val, iterations
    ... )  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Number of initial values must be equal to number of rows in coefficient
                matrix but received 2 and 3

    >>> coefficient = np.array([[4, 1, 1], [1, 5, 2], [1, 2, 4]])
    >>> constant = np.array([[2], [-6], [-4]])
    >>> init_val = [0.5, -0.5, -0.5]
    >>> iterations = 0
    >>> jacobi_iteration_method(coefficient, constant, init_val, iterations)
    Traceback (most recent call last):
        ...
    ValueError: Iterations must be at least 1
    """

    rows1, cols1 = coefficient_matrix.shape
    rows2, cols2 = constant_matrix.shape

    if rows1 != cols1:
        msg = f"Coefficient matrix dimensions must be nxn but received {rows1}x{cols1}"
        raise ValueError(msg)

    if cols2 != 1:
        msg = f"Constant matrix must be nx1 but received {rows2}x{cols2}"
        raise ValueError(msg)

    if rows1 != rows2:
        msg = (
            "Coefficient and constant matrices dimensions must be nxn and nx1 but "
            f"received {rows1}x{cols1} and {rows2}x{cols2}"
        )
        raise ValueError(msg)

    if len(init_val) != rows1:
        msg = (
            "Number of initial values must be equal to number of rows in coefficient "
            f"matrix but received {len(init_val)} and {rows1}"
        )
        raise ValueError(msg)

    if iterations <= 0:
        raise ValueError("Iterations must be at least 1")

    table: NDArray[float64] = np.concatenate(
        (coefficient_matrix, constant_matrix), axis=1
    )

    rows, _cols = table.shape

    strictly_diagonally_dominant(table)

    """
    # Iterates the whole matrix for given number of times
    for _ in range(iterations):
        new_val = []
        for row in range(rows):
            temp = 0
            for col in range(cols):
                if col == row:
                    denom = table[row][col]
                elif col == cols - 1:
                    val = table[row][col]
                else:
                    temp += (-1) * table[row][col] * init_val[col]
            temp = (temp + val) / denom
            new_val.append(temp)
        init_val = new_val
    """

    # denominator——对角线元素列表
    denominator = np.diag(coefficient_matrix)

    # val_last——table 数组最后一列的值
    val_last = table[:, -1]

    # masks——coefficient_matrix 数组中各行除对角线元素外的布尔掩码
    masks = ~np.eye(coefficient_matrix.shape[0], dtype=bool)

    # no_diagonals——coefficient_matrix 数组中除对角线元素外的值
    no_diagonals = coefficient_matrix[masks].reshape(-1, rows - 1)

    # 此处得到 'i_col'——每行除对角线元素及最后一列外的列号
    _i_row, i_col = np.where(masks)
    ind = i_col.reshape(-1, rows - 1)

    # 将 'i_col' 转换为二维列表 'ind'，用于从 'init_val' 中选取元素
    # （参见下方的 'arr' 数组）

    # 按给定次数迭代整个矩阵
    for _ in range(iterations):
        arr = np.take(init_val, ind)
        sum_product_rows = np.sum((-1) * no_diagonals * arr, axis=1)
        new_val = (sum_product_rows + val_last) / denominator
        init_val = new_val

    return new_val.tolist()


    # 检查给定矩阵是否严格对角占优
def strictly_diagonally_dominant(table: NDArray[float64]) -> bool:
    """
    >>> table = np.array([[4, 1, 1, 2], [1, 5, 2, -6], [1, 2, 4, -4]])
    >>> strictly_diagonally_dominant(table)
    True

    >>> table = np.array([[4, 1, 1, 2], [1, 5, 2, -6], [1, 2, 3, -4]])
    >>> strictly_diagonally_dominant(table)
    Traceback (most recent call last):
        ...
    ValueError: Coefficient matrix is not strictly diagonally dominant
    """

    rows, cols = table.shape

    is_diagonally_dominant = True

    for i in range(rows):
        total = 0
        for j in range(cols - 1):
            if i == j:
                continue
            total += table[i][j]

        if table[i][i] <= total:
            raise ValueError("Coefficient matrix is not strictly diagonally dominant")

    return is_diagonally_dominant


# 测试用例
if __name__ == "__main__":
    import doctest

    doctest.testmod()
