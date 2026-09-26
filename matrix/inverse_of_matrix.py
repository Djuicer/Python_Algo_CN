from __future__ import annotations

from decimal import Decimal

from numpy import array


def inverse_of_matrix(matrix: list[list[float]]) -> list[list[float]]:
    """
    矩阵与其逆矩阵相乘可得到单位矩阵。
    本函数求 2x2 和 3x3 矩阵的逆矩阵。
    若矩阵的行列式为 0，则其逆矩阵不存在。

    修正不精确浮点运算的资料：
    https://stackoverflow.com/questions/6563058/how-do-i-use-accurate-float-arithmetic-in-python
    https://docs.python.org/3/library/decimal.html

    2x2 矩阵的 doctest
    >>> inverse_of_matrix([[2, 5], [2, 0]])
    [[0.0, 0.5], [0.2, -0.2]]
    >>> inverse_of_matrix([[2.5, 5], [1, 2]])
    Traceback (most recent call last):
        ...
    ValueError: This matrix has no inverse.
    >>> inverse_of_matrix([[12, -16], [-9, 0]])
    [[0.0, -0.1111111111111111], [-0.0625, -0.08333333333333333]]
    >>> inverse_of_matrix([[12, 3], [16, 8]])
    [[0.16666666666666666, -0.0625], [-0.3333333333333333, 0.25]]
    >>> inverse_of_matrix([[10, 5], [3, 2.5]])
    [[0.25, -0.5], [-0.3, 1.0]]

    Doctests for 3x3
    >>> inverse_of_matrix([[2, 5, 7], [2, 0, 1], [1, 2, 3]])
    [[2.0, 1.0, -5.0], [5.0, 1.0, -12.0], [-4.0, -1.0, 10.0]]
    >>> inverse_of_matrix([[1, 2, 2], [1, 2, 2], [3, 2, -1]])
    Traceback (most recent call last):
        ...
    ValueError: This matrix has no inverse.

    >>> inverse_of_matrix([[],[]])
    Traceback (most recent call last):
        ...
    ValueError: Please provide a matrix of size 2x2 or 3x3.

    >>> inverse_of_matrix([[1, 2], [3, 4], [5, 6]])
    Traceback (most recent call last):
        ...
    ValueError: Please provide a matrix of size 2x2 or 3x3.

    >>> inverse_of_matrix([[1, 2, 1], [0,3, 4]])
    Traceback (most recent call last):
        ...
    ValueError: Please provide a matrix of size 2x2 or 3x3.

    >>> inverse_of_matrix([[1, 2, 3], [7, 8, 9], [7, 8, 9]])
    Traceback (most recent call last):
        ...
    ValueError: This matrix has no inverse.

    >>> inverse_of_matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    """

    d = Decimal

        # 检查所给矩阵是否为 2 行 2 列，因为本实现仅适用于 2x2 矩阵
    if len(matrix) == 2 and len(matrix[0]) == 2 and len(matrix[1]) == 2:
        # 计算矩阵的行列式
        determinant = float(
            d(matrix[0][0]) * d(matrix[1][1]) - d(matrix[1][0]) * d(matrix[0][1])
        )
        if determinant == 0:
            raise ValueError("This matrix has no inverse.")

        # 创建元素位置已交换的矩阵副本
        swapped_matrix = [[0.0, 0.0], [0.0, 0.0]]
        swapped_matrix[0][0], swapped_matrix[1][1] = matrix[1][1], matrix[0][0]
        swapped_matrix[1][0], swapped_matrix[0][1] = -matrix[1][0], -matrix[0][1]

        # 计算矩阵的逆矩阵
        return [
            [(float(d(n)) / determinant) or 0.0 for n in row] for row in swapped_matrix
        ]
    elif (
        len(matrix) == 3
        and len(matrix[0]) == 3
        and len(matrix[1]) == 3
        and len(matrix[2]) == 3
    ):
        # 使用 Sarrus 法则计算矩阵的行列式
        determinant = float(
            (
                (d(matrix[0][0]) * d(matrix[1][1]) * d(matrix[2][2]))
                + (d(matrix[0][1]) * d(matrix[1][2]) * d(matrix[2][0]))
                + (d(matrix[0][2]) * d(matrix[1][0]) * d(matrix[2][1]))
            )
            - (
                (d(matrix[0][2]) * d(matrix[1][1]) * d(matrix[2][0]))
                + (d(matrix[0][1]) * d(matrix[1][0]) * d(matrix[2][2]))
                + (d(matrix[0][0]) * d(matrix[1][2]) * d(matrix[2][1]))
            )
        )
        if determinant == 0:
            raise ValueError("This matrix has no inverse.")

        # 创建余子式矩阵
        cofactor_matrix = [
            [d(0.0), d(0.0), d(0.0)],
            [d(0.0), d(0.0), d(0.0)],
            [d(0.0), d(0.0), d(0.0)],
        ]
        cofactor_matrix[0][0] = (d(matrix[1][1]) * d(matrix[2][2])) - (
            d(matrix[1][2]) * d(matrix[2][1])
        )
        cofactor_matrix[0][1] = -(
            (d(matrix[1][0]) * d(matrix[2][2])) - (d(matrix[1][2]) * d(matrix[2][0]))
        )
        cofactor_matrix[0][2] = (d(matrix[1][0]) * d(matrix[2][1])) - (
            d(matrix[1][1]) * d(matrix[2][0])
        )
        cofactor_matrix[1][0] = -(
            (d(matrix[0][1]) * d(matrix[2][2])) - (d(matrix[0][2]) * d(matrix[2][1]))
        )
        cofactor_matrix[1][1] = (d(matrix[0][0]) * d(matrix[2][2])) - (
            d(matrix[0][2]) * d(matrix[2][0])
        )
        cofactor_matrix[1][2] = -(
            (d(matrix[0][0]) * d(matrix[2][1])) - (d(matrix[0][1]) * d(matrix[2][0]))
        )
        cofactor_matrix[2][0] = (d(matrix[0][1]) * d(matrix[1][2])) - (
            d(matrix[0][2]) * d(matrix[1][1])
        )
        cofactor_matrix[2][1] = -(
            (d(matrix[0][0]) * d(matrix[1][2])) - (d(matrix[0][2]) * d(matrix[1][0]))
        )
        cofactor_matrix[2][2] = (d(matrix[0][0]) * d(matrix[1][1])) - (
            d(matrix[0][1]) * d(matrix[1][0])
        )

        # 转置余子式矩阵（伴随矩阵）
        adjoint_matrix = array(cofactor_matrix)
        for i in range(3):
            for j in range(3):
                adjoint_matrix[i][j] = cofactor_matrix[j][i]

        # 使用公式 (1/determinant) * adjoint matrix 求逆矩阵
        inverse_matrix = array(adjoint_matrix)
        for i in range(3):
            for j in range(3):
                inverse_matrix[i][j] /= d(determinant)

        # 计算矩阵的逆矩阵
        return [[float(d(n)) or 0.0 for n in row] for row in inverse_matrix]
    raise ValueError("Please provide a matrix of size 2x2 or 3x3.")
