"""
集合 矩阵 Zeroes 算法
---------------------------
如果 元素 在 m x n 矩阵 是 0，集合 其 整个 row 并且 column 到 0。

Explanation:
我们 使用 第一个 row 并且 第一个 column 作为 markers 到 track 其 rows 并且
columns 应 为 zeroed，avoiding extra 空间 usage (O(1) 空间复杂度)。

引用：
https://leetcode.com/problems/set-matrix-zeroes/

Doctest:
>>> matrix = [
...     [1, 1, 1],
...     [1, 0, 1],
...     [1, 1, 1]
... ]
>>> set_matrix_zeroes(matrix)
>>> matrix
[[1, 0, 1], [0, 0, 0], [1, 0, 1]]
>>> matrix = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
>>> set_matrix_zeroes(matrix)
>>> matrix
[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
"""


def set_matrix_zeroes(matrix: list[list[int]]) -> None:
    """
    Modify 矩阵 在-位置 such 该 如果 元素 是 0,
    其 整个 row 并且 column 是 集合 到 0。

    :param 矩阵: 2D 列表 的 整数
    :返回: None (modifies 矩阵 在-位置)

    时间复杂度: O(m * n)
    空间复杂度: O(1)
    """
    rows = len(matrix)
    cols = len(matrix[0])
    col0 = 1

    # 步骤 1: Mark rows 并且 columns 该 need 到 为 zeroed
    for i in range(rows):
        if matrix[i][0] == 0:
            col0 = 0
        for j in range(1, cols):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # 步骤 2: 更新 inner 矩阵 cells
    for i in range(1, rows):
        for j in range(1, cols):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # 步骤 3: Handle 第一个 row
    if matrix[0][0] == 0:
        for j in range(cols):
            matrix[0][j] = 0

    # 步骤 4: Handle 第一个 column
    if col0 == 0:
        for i in range(rows):
            matrix[i][0] = 0
