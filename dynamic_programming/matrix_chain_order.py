import sys

"""
动态规划（Dynamic Programming）
矩阵链乘法的实现
时间复杂度：O(n^3)
空间复杂度：O(n^2)

Reference: https://en.wikipedia.org/wiki/Matrix_chain_multiplication
"""


def matrix_chain_order(array: list[int]) -> tuple[list[list[int]], list[list[int]]]:
    """
    >>> matrix_chain_order([10, 30, 5])
    ([[0, 0, 0], [0, 0, 1500], [0, 0, 0]], [[0, 0, 0], [0, 0, 1], [0, 0, 0]])
    """
    n = len(array)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    sol = [[0 for _ in range(n)] for _ in range(n)]

    for chain_length in range(2, n):
        for a in range(1, n - chain_length + 1):
            b = a + chain_length - 1

            matrix[a][b] = sys.maxsize
            for c in range(a, b):
                cost = (
                    matrix[a][c] + matrix[c + 1][b] + array[a - 1] * array[c] * array[b]
                )
                if cost < matrix[a][b]:
                    matrix[a][b] = cost
                    sol[a][b] = c
    return matrix, sol


def print_optimal_solution(optimal_solution: list[list[int]], i: int, j: int) -> None:
    """
    输出矩阵的顺序，其中 Ai 表示矩阵。
    """

    if i == j:
        print("A" + str(i), end=" ")
    else:
        print("(", end=" ")
        print_optimal_solution(optimal_solution, i, optimal_solution[i][j])
        print_optimal_solution(optimal_solution, optimal_solution[i][j] + 1, j)
        print(")", end=" ")


def main() -> None:
    """
    由数组 [30, 35, 15, 5, 10, 20, 25] 创建的矩阵大小为：
    30*35 35*15 15*5 5*10 10*20 20*25
    """

    array = [30, 35, 15, 5, 10, 20, 25]
    n = len(array)

    matrix, optimal_solution = matrix_chain_order(array)

    print("No. of Operation required: " + str(matrix[1][n - 1]))
    print_optimal_solution(optimal_solution, 1, n - 1)


if __name__ == "__main__":
    main()
