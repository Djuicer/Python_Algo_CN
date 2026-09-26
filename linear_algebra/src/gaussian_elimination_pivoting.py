import numpy as np


def solve_linear_system(matrix: np.ndarray) -> np.ndarray:
    """
    使用带部分选主元的高斯消元法求解线性方程组。

    参数：
      - `matrix`: 系数矩阵，其最后一列表示常数项。

    返回：
      - 解向量。

    异常：
      - ``ValueError``: 矩阵不正确（即为奇异矩阵）时抛出。

    https://courses.engr.illinois.edu/cs357/su2013/lect.htm Lecture 7

    示例：

    >>> A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
    >>> B = np.array([8, -11, -3], dtype=float)
    >>> solution = solve_linear_system(np.column_stack((A, B)))
    >>> np.allclose(solution, np.array([2., 3., -1.]))
    True
    >>> solve_linear_system(np.array([[0, 0, 0]], dtype=float))
    Traceback (most recent call last):
        ...
    ValueError: Matrix is not square
    >>> solve_linear_system(np.array([[0, 0, 0], [0, 0, 0]], dtype=float))
    Traceback (most recent call last):
        ...
    ValueError: Matrix is singular
    """
    ab = np.copy(matrix)
    num_of_rows = ab.shape[0]
    num_of_columns = ab.shape[1] - 1
    x_lst: list[float] = []

    if num_of_rows != num_of_columns:
        raise ValueError("Matrix is not square")

    for column_num in range(num_of_rows):
    # 搜索主元
        for i in range(column_num, num_of_columns):
            if abs(ab[i][column_num]) > abs(ab[column_num][column_num]):
                ab[[column_num, i]] = ab[[i, column_num]]

    # 上三角矩阵
        if abs(ab[column_num, column_num]) < 1e-8:
            raise ValueError("Matrix is singular")

        if column_num != 0:
            for i in range(column_num, num_of_rows):
                ab[i, :] -= (
                    ab[i, column_num - 1]
                    / ab[column_num - 1, column_num - 1]
                    * ab[column_num - 1, :]
                )

    # 通过回代求向量 x
    for column_num in range(num_of_rows - 1, -1, -1):
        x = ab[column_num, -1] / ab[column_num, column_num]
        x_lst.insert(0, x)
        for i in range(column_num - 1, -1, -1):
            ab[i, -1] -= ab[i, column_num] * x

    # 返回解向量
    return np.asarray(x_lst)


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    example_matrix = np.array(
        [
            [5.0, -5.0, -3.0, 4.0, -11.0],
            [1.0, -4.0, 6.0, -4.0, -10.0],
            [-2.0, -5.0, 4.0, -5.0, -12.0],
            [-3.0, -3.0, 5.0, -5.0, 8.0],
        ],
        dtype=float,
    )

    print(f"Matrix:\n{example_matrix}")
    print(f"{solve_linear_system(example_matrix) = }")
