"""
Project Euler Problem 82: https://projecteuler.net/problem=82

在下面的 5 x 5 矩阵中，从左列任意单元格出发、在右列任意单元格结束，
并且只能向上、向下和向右移动时，最小路径和以红色粗体标出，等于 994。

     131    673   [234]  [103]  [18]
    [201]  [96]   [342]   965    150
     630    803    746    422    111
     537    699    497    121    956
     805    732    524    37     331

求 matrix.txt 中从左列到右列的最小路径和
(https://projecteuler.net/project/resources/p082_matrix.txt)
(right click and "Save Link/Target As..."),
该文件是一个包含 80 x 80 矩阵的 31K 文本文件。
"""

import os


def solution(filename: str = "input.txt") -> int:
    """
    返回文件中矩阵的最小路径和：从左列任意单元格出发，在右列任意单元格结束，
    并且只能向上、向下和向右移动。

    >>> solution("test_matrix.txt")
    994
    """

    with open(os.path.join(os.path.dirname(__file__), filename)) as input_file:
        matrix = [
            [int(element) for element in line.split(",")]
            for line in input_file.readlines()
        ]

    rows = len(matrix)
    cols = len(matrix[0])

    minimal_path_sums = [[-1 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        minimal_path_sums[i][0] = matrix[i][0]

    for j in range(1, cols):
        for i in range(rows):
            minimal_path_sums[i][j] = minimal_path_sums[i][j - 1] + matrix[i][j]

        for i in range(1, rows):
            minimal_path_sums[i][j] = min(
                minimal_path_sums[i][j], minimal_path_sums[i - 1][j] + matrix[i][j]
            )

        for i in range(rows - 2, -1, -1):
            minimal_path_sums[i][j] = min(
                minimal_path_sums[i][j], minimal_path_sums[i + 1][j] + matrix[i][j]
            )

    return min(minimal_path_sums_row[-1] for minimal_path_sums_row in minimal_path_sums)


if __name__ == "__main__":
    print(f"{solution() = }")
