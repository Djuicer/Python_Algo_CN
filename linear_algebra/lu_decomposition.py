"""
LU 分解（Lower-Upper Decomposition）将矩阵分解为下三角矩阵与上三角矩阵的
乘积。方阵在以下条件下存在 LU 分解：

    - 若矩阵可逆，则当且仅当其所有顺序主子式均非零时，它存在 LU 分解
      （矩阵顺序主子式的说明参见
      https://en.wikipedia.org/wiki/Minor_(linear_algebra)）。
    - 若矩阵奇异（即不可逆）且秩为 k（即有 k 个线性无关列），则当前 k 个
      顺序主子式均非零时，它存在 LU 分解。

本算法会尝试对任意方阵执行 LU 分解；若不存在这种分解，则抛出错误。

参考资料：https://en.wikipedia.org/wiki/LU_decomposition
"""

from __future__ import annotations

import numpy as np


def lower_upper_decomposition(table: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    对给定矩阵执行 LU 分解。若矩阵不是方阵或不存在这种分解，则抛出错误。

    >>> matrix = np.array([[2, -2, 1], [0, 1, 2], [5, 3, 1]])
    >>> lower_mat, upper_mat = lower_upper_decomposition(matrix)
    >>> lower_mat
    array([[1. , 0. , 0. ],
           [0. , 1. , 0. ],
           [2.5, 8. , 1. ]])
    >>> upper_mat
    array([[  2. ,  -2. ,   1. ],
           [  0. ,   1. ,   2. ],
           [  0. ,   0. , -17.5]])

    >>> matrix = np.array([[4, 3], [6, 3]])
    >>> lower_mat, upper_mat = lower_upper_decomposition(matrix)
    >>> lower_mat
    array([[1. , 0. ],
           [1.5, 1. ]])
    >>> upper_mat
    array([[ 4. ,  3. ],
           [ 0. , -1.5]])

    >>> # Matrix is not square
    >>> matrix = np.array([[2, -2, 1], [0, 1, 2]])
    >>> lower_mat, upper_mat = lower_upper_decomposition(matrix)
    Traceback (most recent call last):
        ...
    ValueError: 'table' has to be of square shaped array but got a 2x3 array:
    [[ 2 -2  1]
     [ 0  1  2]]

    >>> # Matrix is invertible, but its first leading principal minor is 0
    >>> matrix = np.array([[0, 1], [1, 0]])
    >>> lower_mat, upper_mat = lower_upper_decomposition(matrix)
    Traceback (most recent call last):
    ...
    ArithmeticError: No LU decomposition exists

    >>> # Matrix is singular, but its first leading principal minor is 1
    >>> matrix = np.array([[1, 0], [1, 0]])
    >>> lower_mat, upper_mat = lower_upper_decomposition(matrix)
    >>> lower_mat
    array([[1., 0.],
           [1., 1.]])
    >>> upper_mat
    array([[1., 0.],
           [0., 0.]])

    >>> # Matrix is singular, but its first leading principal minor is 0
    >>> matrix = np.array([[0, 1], [0, 1]])
    >>> lower_mat, upper_mat = lower_upper_decomposition(matrix)
    Traceback (most recent call last):
    ...
    ArithmeticError: No LU decomposition exists
    """
    # 确保 table 是方阵
    rows, columns = np.shape(table)
    if rows != columns:
        msg = (
            "'table' has to be of square shaped array but got a "
            f"{rows}x{columns} array:\n{table}"
        )
        raise ValueError(msg)

    lower = np.zeros((rows, columns))
    upper = np.zeros((rows, columns))

            # 在 'total' 中通过切片提取所需数据，并求乘积之和

    for i in range(columns):
        for j in range(i):
            total = np.sum(lower[i, :i] * upper[:i, j])
            if upper[j][j] == 0:
                raise ArithmeticError("No LU decomposition exists")
            lower[i][j] = (table[i][j] - total) / upper[j][j]
        lower[i][i] = 1
        for j in range(i, columns):
            total = np.sum(lower[i, :i] * upper[:i, j])
            upper[i][j] = table[i][j] - total
    return lower, upper


if __name__ == "__main__":
    import doctest

    doctest.testmod()
