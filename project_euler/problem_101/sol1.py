"""
如果只给出数列的前 k 项，就无法确定下一项的值，因为有无穷多个多项式函数可以拟合该数列。

例如，考虑立方数数列。它由以下生成函数定义：
u(n) = n3: 1, 8, 27, 64, 125, 216, ...

假设只给出该数列的前两项。根据“简单即最佳”原则，应假定线性关系，并预测下一项为
15（公差为 7）。即使给出前三项，根据同一简洁原则，也应假定二次关系。

定义 OP(k, n) 为拟合数列前 k 项的最优多项式生成函数的第 n 项。显然，当 n ≤ k 时，
OP(k, n) 会准确生成数列项；首个潜在错误项（FIT）为 OP(k, k+1)，此时称其为错误的
OP（BOP）。

作为基础，如果只给出数列第一项，最合理的是假定它恒定；即当 n ≥ 2 时，
OP(1, n) = u(1)。

因此得到立方数列的以下 OP：

OP(1, n) = 1            1, 1, 1, 1, ...
OP(2, n) = 7n-6         1, 8, 15, ...
OP(3, n) = 6n^2-11n+6   1, 8, 27, 58, ...
OP(4, n) = n^3          1, 8, 27, 64, 125, ...

显然，当 k ≥ 4 时不存在 BOP。

考虑 BOP 生成的 FIT（上方以红色标出）之和，可得 1 + 15 + 58 = 74。

考虑以下十次多项式生成函数：

1 - n + n^2 - n^3 + n^4 - n^5 + n^6 - n^7 + n^8 - n^9 + n^10

求这些 BOP 的 FIT 之和。
"""

from __future__ import annotations

from collections.abc import Callable

Matrix = list[list[float | int]]


def solve(matrix: Matrix, vector: Matrix) -> Matrix:
    """
    使用高斯消元与回代求解线性方程组 Ax = b 中的 x（A = "matrix"，b = "vector"）。
    假设 A 是可逆方阵，b 是高度相同的列向量。
    >>> solve([[1, 0], [0, 1]], [[1],[2]])
    [[1.0], [2.0]]
    >>> solve([[2, 1, -1],[-3, -1, 2],[-2, 1, 2]],[[8], [-11],[-3]])
    [[2.0], [3.0], [-1.0]]
    """
    size: int = len(matrix)
    augmented: Matrix = [[0 for _ in range(size + 1)] for _ in range(size)]
    row: int
    row2: int
    col: int
    col2: int
    pivot_row: int
    ratio: float

    for row in range(size):
        for col in range(size):
            augmented[row][col] = matrix[row][col]

        augmented[row][size] = vector[row][0]

    row = 0
    col = 0
    while row < size and col < size:
        # 选取主元
        pivot_row = max((abs(augmented[row2][col]), row2) for row2 in range(col, size))[
            1
        ]
        if augmented[pivot_row][col] == 0:
            col += 1
            continue
        augmented[row], augmented[pivot_row] = augmented[pivot_row], augmented[row]

        for row2 in range(row + 1, size):
            ratio = augmented[row2][col] / augmented[row][col]
            augmented[row2][col] = 0
            for col2 in range(col + 1, size + 1):
                augmented[row2][col2] -= augmented[row][col2] * ratio

        row += 1
        col += 1

    # 回代
    for col in range(1, size):
        for row in range(col):
            ratio = augmented[row][col] / augmented[col][col]
            for col2 in range(col, size + 1):
                augmented[row][col2] -= augmented[col][col2] * ratio

    # 通过舍入消除类似 2.000000000000004 的数
    return [
        [round(augmented[row][size] / augmented[row][row], 10)] for row in range(size)
    ]


def interpolate(y_list: list[int]) -> Callable[[int], int]:
    """
    给定数据点列表 (1,y0),(2,y1), ...，返回对这些数据点进行插值的函数。
    通过求解对应 x = 1, 2, 3... 的线性方程组，得到插值多项式的系数。

    >>> interpolate([1])(3)
    1
    >>> interpolate([1, 8])(3)
    15
    >>> interpolate([1, 8, 27])(4)
    58
    >>> interpolate([1, 8, 27, 64])(6)
    216
    """

    size: int = len(y_list)
    matrix: Matrix = [[0 for _ in range(size)] for _ in range(size)]
    vector: Matrix = [[0] for _ in range(size)]
    coeffs: Matrix
    x_val: int
    y_val: int
    col: int

    for x_val, y_val in enumerate(y_list):
        for col in range(size):
            matrix[x_val][col] = (x_val + 1) ** (size - col - 1)
        vector[x_val][0] = y_val

    coeffs = solve(matrix, vector)

    def interpolated_func(var: int) -> int:
        """
        >>> interpolate([1])(3)
        1
        >>> interpolate([1, 8])(3)
        15
        >>> interpolate([1, 8, 27])(4)
        58
        >>> interpolate([1, 8, 27, 64])(6)
        216
        """
        return sum(
            round(coeffs[x_val][0]) * (var ** (size - x_val - 1))
            for x_val in range(size)
        )

    return interpolated_func


def question_function(variable: int) -> int:
    """
    题目指定的生成函数 u。
    >>> question_function(0)
    1
    >>> question_function(1)
    1
    >>> question_function(5)
    8138021
    >>> question_function(10)
    9090909091
    """
    return (
        1
        - variable
        + variable**2
        - variable**3
        + variable**4
        - variable**5
        + variable**6
        - variable**7
        + variable**8
        - variable**9
        + variable**10
    )


def solution(func: Callable[[int], int] = question_function, order: int = 10) -> int:
    """
    求 BOP 的 FIT 之和。对于 1, 2, ... , 10 阶的每个插值多项式，找出使多项式值
    不等于 u(x) 的第一个 x。
    >>> solution(lambda n: n ** 3, 3)
    74
    """
    data_points: list[int] = [func(x_val) for x_val in range(1, order + 1)]

    polynomials: list[Callable[[int], int]] = [
        interpolate(data_points[:max_coeff]) for max_coeff in range(1, order + 1)
    ]

    ret: int = 0
    poly: Callable[[int], int]
    x_val: int

    for poly in polynomials:
        x_val = 1
        while func(x_val) == poly(x_val):
            x_val += 1

        ret += poly(x_val)

    return ret


if __name__ == "__main__":
    print(f"{solution() = }")
