# @Author  : jay2219
# @File    : kronecker_product.py
# @Date    : 13/10/2024

"""
计算两个矩阵的 Kronecker 积。
https://en.wikipedia.org/wiki/Kronecker_product
"""


def is_2d(matrix: list[list[int]]) -> bool:
    """
    >>> is_2d([])
    True
    >>> is_2d([1, 2])
    False
    >>> is_2d([[1, 2], [3, 4]])
    True
    """

    return all(isinstance(matrix, list) and (isinstance(i, list) for i in matrix))


def kronecker_product(
    matrix_a: list[list[int]], matrix_b: list[list[int]]
) -> list[list[int]]:
    """
    :param matrix_a: 维数为 m x n 的二维矩阵
    :param matrix_b: 维数为 p x q 的另一个二维矩阵
    :return: matrix_a ⊗ matrix_b 的结果
    :raises ValueError: 矩阵不是二维时抛出

    >>> kronecker_product([[1, 2]], [[5, 6], [7, 8]])
    [[5, 6, 10, 12], [7, 8, 14, 16]]

    >>> kronecker_product([[1, 2], [4, 5]], [[5, 6], [7, 8]])
    [[5, 6, 10, 12], [7, 8, 14, 16], [20, 24, 25, 30], [28, 32, 35, 40]]

    >>> kronecker_product([1, 2], [[5, 6], [7, 8]])
    Traceback (most recent call last):
        ...
    ValueError: Input matrices must be 2-D.
    """

    # 检查输入矩阵是否有效
    if not all((is_2d(matrix_a), is_2d(matrix_b))):
        raise ValueError("Input matrices must be 2-D.")

    if not matrix_a or not matrix_b:
        return []

    rows_matrix_a, cols_matrix_a = len(matrix_a), len(matrix_a[0])
    rows_matrix_b, cols_matrix_b = len(matrix_b), len(matrix_b[0])

    # 结果矩阵的维数
    result = [
        [0] * (cols_matrix_a * cols_matrix_b)
        for _ in range(rows_matrix_a * rows_matrix_b)
    ]

    for r_index_a in range(rows_matrix_a):
        for c_index_a in range(cols_matrix_a):
            for r_index_b in range(rows_matrix_b):
                for c_index_b in range(cols_matrix_b):
                    result[r_index_a * rows_matrix_b + r_index_b][
                        c_index_a * cols_matrix_b + c_index_b
                    ] = matrix_a[r_index_a][c_index_a] * matrix_b[r_index_b][c_index_b]

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
