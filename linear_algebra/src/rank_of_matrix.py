"""
计算矩阵的秩。

参见：https://en.wikipedia.org/wiki/Rank_(linear_algebra)
"""


def rank_of_matrix(matrix: list[list[int | float]]) -> int:
    """
    求矩阵的秩。

    参数：
        `matrix`: 以列表的列表表示的矩阵。

    返回：
        矩阵的秩。

    示例：

    >>> matrix1 = [[1, 2, 3],
    ...            [4, 5, 6],
    ...            [7, 8, 9]]
    >>> rank_of_matrix(matrix1)
    2
    >>> matrix2 = [[1, 0, 0],
    ...            [0, 1, 0],
    ...            [0, 0, 0]]
    >>> rank_of_matrix(matrix2)
    2
    >>> matrix3 = [[1, 2, 3, 4],
    ...            [5, 6, 7, 8],
    ...            [9, 10, 11, 12]]
    >>> rank_of_matrix(matrix3)
    2
    >>> rank_of_matrix([[2,3,-1,-1],
    ...                [1,-1,-2,4],
    ...                [3,1,3,-2],
    ...                [6,3,0,-7]])
    4
    >>> rank_of_matrix([[2,1,-3,-6],
    ...                [3,-3,1,2],
    ...                [1,1,1,2]])
    3
    >>> rank_of_matrix([[2,-1,0],
    ...                [1,3,4],
    ...                [4,1,-3]])
    3
    >>> rank_of_matrix([[3,2,1],
    ...                [-6,-4,-2]])
    1
    >>> rank_of_matrix([[],[]])
    0
    >>> rank_of_matrix([[1]])
    1
    >>> rank_of_matrix([[]])
    0
    """

    rows = len(matrix)
    columns = len(matrix[0])
    rank = min(rows, columns)

    for row in range(rank):
        # 检查对角线元素是否非零
        if matrix[row][row] != 0:
            # 消去对角线下方的所有元素
            for col in range(row + 1, rows):
                multiplier = matrix[col][row] / matrix[row][row]
                for i in range(row, columns):
                    matrix[col][i] -= multiplier * matrix[row][i]
        else:
            # 寻找非零对角线元素以交换行
            reduce = True
            for i in range(row + 1, rows):
                if matrix[i][row] != 0:
                    matrix[row], matrix[i] = matrix[i], matrix[row]
                    reduce = False
                    break
            if reduce:
                rank -= 1
                for i in range(rows):
                    matrix[i][row] = matrix[i][rank]

                # 将行指针减一，以停留在同一行
            row -= 1

    return rank


if __name__ == "__main__":
    import doctest

    doctest.testmod()
