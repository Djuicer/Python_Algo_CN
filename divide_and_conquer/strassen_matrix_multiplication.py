"""
https://en.wikipedia.org/wiki/Strassen_algorithm
"""

from __future__ import annotations

import math


def default_matrix_multiplication(a: list, b: list) -> list:
    """
    仅用于 2x2 矩阵的乘法
    """
    if len(a) != 2 or len(a[0]) != 2 or len(b) != 2 or len(b[0]) != 2:
        raise Exception("Matrices are not 2x2")
    new_matrix = [
        [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
    ]
    return new_matrix


def matrix_addition(matrix_a: list, matrix_b: list):
    return [
        [matrix_a[row][col] + matrix_b[row][col] for col in range(len(matrix_a[row]))]
        for row in range(len(matrix_a))
    ]


def matrix_subtraction(matrix_a: list, matrix_b: list):
    return [
        [matrix_a[row][col] - matrix_b[row][col] for col in range(len(matrix_a[row]))]
        for row in range(len(matrix_a))
    ]


def split_matrix(a: list) -> tuple[list, list, list, list]:
    """
    给定边长为偶数的矩阵，返回 top_left、top_right、bot_left、bot_right
    四个象限。

    >>> split_matrix([[4,3,2,4],[2,3,1,1],[6,5,4,3],[8,4,1,6]])
    ([[4, 3], [2, 3]], [[2, 4], [1, 1]], [[6, 5], [8, 4]], [[4, 3], [1, 6]])
    >>> split_matrix([
    ...     [4,3,2,4,4,3,2,4],[2,3,1,1,2,3,1,1],[6,5,4,3,6,5,4,3],[8,4,1,6,8,4,1,6],
    ...     [4,3,2,4,4,3,2,4],[2,3,1,1,2,3,1,1],[6,5,4,3,6,5,4,3],[8,4,1,6,8,4,1,6]
    ... ])  # doctest: +NORMALIZE_WHITESPACE
    ([[4, 3, 2, 4], [2, 3, 1, 1], [6, 5, 4, 3], [8, 4, 1, 6]], [[4, 3, 2, 4],
      [2, 3, 1, 1], [6, 5, 4, 3], [8, 4, 1, 6]], [[4, 3, 2, 4], [2, 3, 1, 1],
      [6, 5, 4, 3], [8, 4, 1, 6]], [[4, 3, 2, 4], [2, 3, 1, 1], [6, 5, 4, 3],
      [8, 4, 1, 6]])
    """
    if len(a) % 2 != 0 or len(a[0]) % 2 != 0:
        raise Exception("Odd matrices are not supported!")

    def extract_submatrix(rows, cols):
        return [[a[i][j] for j in cols] for i in rows]

    mid = len(a) // 2

    rows_top, rows_bot = range(mid), range(mid, len(a))
    cols_left, cols_right = range(mid), range(mid, len(a))

    return (
        extract_submatrix(rows_top, cols_left),  # 左上
        extract_submatrix(rows_top, cols_right),  # 右上
        extract_submatrix(rows_bot, cols_left),  # 左下
        extract_submatrix(rows_bot, cols_right),  # 右下
    )


def matrix_dimensions(matrix: list) -> tuple[int, int]:
    return len(matrix), len(matrix[0])


def print_matrix(matrix: list) -> None:
    print("\n".join(str(line) for line in matrix))


def actual_strassen(matrix_a: list, matrix_b: list) -> list:
    """
    使用 Strassen 算法递归计算
    两个矩阵的乘积。

    时间复杂度：
        递推式为 T(n) = 7 T(n/2) + \u0398(n^2)，解为
        T(n) = \u0398(n^{log_2 7}) \u2248 \u0398(n^{2.8074})。当 n 足够大时，
        其渐近复杂度优于朴素的 \u0398(n^3) 算法。

    空间复杂度：
        临时子矩阵和填充需要额外内存；总体
        空间复杂度为 O(n^2)。

    说明：
        此函数要求方阵的边长为 2 的幂。
        其他大小的矩阵由 `strassen` 处理，将其填充到
        下一个 2 的幂。

    仅支持边长为 2 的幂的方阵。

    Strassen 算法将两个 n x n 矩阵相乘所需的递归乘法次数，
    从朴素分治法的 8 次
    减少到 7 次，代价是增加少量矩阵加减法
    （这些操作代价较低，为 O(n^2)）。每个矩阵分为四个
    (n/2) x (n/2) 象限；递归计算象限组合的 7 个乘积，
    然后通过加减法组合这些乘积，
    形成结果矩阵的四个象限。

    时间复杂度：O(n^log2(7)) ~= O(n^2.807)，优于
    标准朴素矩阵乘法算法的 O(n^3)。
    空间复杂度：存储中间象限矩阵需要 O(n^2)，另有
    深度为 O(log n) 的递归调用栈。
    """
    if matrix_dimensions(matrix_a) == (2, 2):
        return default_matrix_multiplication(matrix_a, matrix_b)

    a, b, c, d = split_matrix(matrix_a)
    e, f, g, h = split_matrix(matrix_b)

    t1 = actual_strassen(a, matrix_subtraction(f, h))
    t2 = actual_strassen(matrix_addition(a, b), h)
    t3 = actual_strassen(matrix_addition(c, d), e)
    t4 = actual_strassen(d, matrix_subtraction(g, e))
    t5 = actual_strassen(matrix_addition(a, d), matrix_addition(e, h))
    t6 = actual_strassen(matrix_subtraction(b, d), matrix_addition(g, h))
    t7 = actual_strassen(matrix_subtraction(a, c), matrix_addition(e, f))

    top_left = matrix_addition(matrix_subtraction(matrix_addition(t5, t4), t2), t6)
    top_right = matrix_addition(t1, t2)
    bot_left = matrix_addition(t3, t4)
    bot_right = matrix_subtraction(matrix_subtraction(matrix_addition(t1, t5), t3), t7)

    # 由四个象限构造新矩阵
    new_matrix = []
    for i in range(len(top_right)):
        new_matrix.append(top_left[i] + top_right[i])
    for i in range(len(bot_right)):
        new_matrix.append(bot_left[i] + bot_right[i])
    return new_matrix


def strassen(matrix1: list, matrix2: list) -> list:
    """
    使用 Strassen 分治算法计算两个矩阵的乘积。

    时间复杂度：
        \u0398(n^{log_2 7}) \u2248 \u0398(n^{2.8074})
        （递推式 T(n) = 7 T(n/2) + \u0398(n^2)）。

    空间复杂度：
        填充和递归期间的临时矩阵使其为 O(n^2)。

    使用 Strassen 算法计算两个矩阵的乘积，运行时间为
    O(n^log2(7)) ~= O(n^2.807)，而朴素矩阵乘法的时间复杂度为
    O(n^3)。本实现对两个输入矩阵补零，
    使其成为边长为 2 的幂的方阵（这是
    actual_strassen 中分治递归的要求），完成
    乘法后，再去掉结果中的填充部分。

    示例：

    >>> strassen([[2,1,3],[3,4,6],[1,4,2],[7,6,7]], [[4,2,3,4],[2,1,1,1],[8,6,4,2]])
    [[34, 23, 19, 15], [68, 46, 37, 28], [28, 18, 15, 12], [96, 62, 55, 48]]
    >>> strassen([[3,7,5,6,9],[1,5,3,7,8],[1,4,4,5,7]], [[2,4],[5,2],[1,7],[5,5],[7,8]])
    [[139, 163], [121, 134], [100, 121]]
    """
    if matrix_dimensions(matrix1)[1] != matrix_dimensions(matrix2)[0]:
        msg = (
            "Unable to multiply these matrices, please check the dimensions.\n"
            f"Matrix A: {matrix1}\n"
            f"Matrix B: {matrix2}"
        )
        raise Exception(msg)
    dimension1 = matrix_dimensions(matrix1)
    dimension2 = matrix_dimensions(matrix2)

    if dimension1[0] == dimension1[1] and dimension2[0] == dimension2[1]:
        return [matrix1, matrix2]

    maximum = max(*dimension1, *dimension2)
    maxim = int(math.pow(2, math.ceil(math.log2(maximum))))
    new_matrix1 = matrix1
    new_matrix2 = matrix2

    # 为矩阵补零，使二者成为边长相同、
    # 且边长为 2 的幂的方阵
    for i in range(maxim):
        if i < dimension1[0]:
            for _ in range(dimension1[1], maxim):
                new_matrix1[i].append(0)
        else:
            new_matrix1.append([0] * maxim)
        if i < dimension2[0]:
            for _ in range(dimension2[1], maxim):
                new_matrix2[i].append(0)
        else:
            new_matrix2.append([0] * maxim)

    final_matrix = actual_strassen(new_matrix1, new_matrix2)

    # 移除额外填充的零
    for i in range(maxim):
        if i < dimension1[0]:
            for _ in range(dimension2[1], maxim):
                final_matrix[i].pop()
        else:
            final_matrix.pop()
    return final_matrix


if __name__ == "__main__":
    matrix1 = [
        [2, 3, 4, 5],
        [6, 4, 3, 1],
        [2, 3, 6, 7],
        [3, 1, 2, 4],
        [2, 3, 4, 5],
        [6, 4, 3, 1],
        [2, 3, 6, 7],
        [3, 1, 2, 4],
        [2, 3, 4, 5],
        [6, 2, 3, 1],
    ]
    matrix2 = [[0, 2, 1, 1], [16, 2, 3, 3], [2, 2, 7, 7], [13, 11, 22, 4]]
    print(strassen(matrix1, matrix2))
