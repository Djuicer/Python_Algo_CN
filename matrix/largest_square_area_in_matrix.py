"""
问题：
给定大小为 n * m 的二进制矩阵 mat，求全部由 1 组成的最大正方形子矩阵边长。

---
示例 1：

输入：
n = 2, m = 2
mat = [[1, 1],
       [1, 1]]

输出：
2

说明：正方形子矩阵的最大边长为 2；在此情形下，矩阵本身就是最大的子矩阵。
---
示例 2

输入：
n = 2, m = 2
mat = [[0, 0],
       [0, 0]]
输出：0

说明：矩阵中没有 1。


方法：
初始化另一个与原矩阵维数相同且元素全为 0 的矩阵（dp）。

dp_array(i,j) 表示以原矩阵中索引为 (i,j) 的单元格作为右下角的最大正方形边长。

从索引 (0,0) 开始，每当在原矩阵中找到 1，就按下式更新当前元素的值：

dp_array(i,j)=dp_array(dp(i-1,j),dp_array(i-1,j-1),dp_array(i,j-1)) + 1.
"""


def largest_square_area_in_matrix_top_down_approch(
    rows: int, cols: int, mat: list[list[int]]
) -> int:
    """
    若递归调用找到面积最大的正方形，则更新 largest_square_area[0]。

    此处未使用 dp_array，因此时间复杂度为指数级。

    >>> largest_square_area_in_matrix_top_down_approch(2, 2, [[1,1], [1,1]])
    2
    >>> largest_square_area_in_matrix_top_down_approch(2, 2, [[0,0], [0,0]])
    0
    """

    def update_area_of_max_square(row: int, col: int) -> int:
    # 基本情况
        if row >= rows or col >= cols:
            return 0

        right = update_area_of_max_square(row, col + 1)
        diagonal = update_area_of_max_square(row + 1, col + 1)
        down = update_area_of_max_square(row + 1, col)

        if mat[row][col]:
            sub_problem_sol = 1 + min([right, diagonal, down])
            largest_square_area[0] = max(largest_square_area[0], sub_problem_sol)
            return sub_problem_sol
        else:
            return 0

    largest_square_area = [0]
    update_area_of_max_square(0, 0)
    return largest_square_area[0]


def largest_square_area_in_matrix_top_down_approch_with_dp(
    rows: int, cols: int, mat: list[list[int]]
) -> int:
    """
    若递归调用找到面积最大的正方形，则更新 largest_square_area[0]。

    此处使用 dp_array，因此时间复杂度为 O(N^2)。

    >>> largest_square_area_in_matrix_top_down_approch_with_dp(2, 2, [[1,1], [1,1]])
    2
    >>> largest_square_area_in_matrix_top_down_approch_with_dp(2, 2, [[0,0], [0,0]])
    0
    """

    def update_area_of_max_square_using_dp_array(
        row: int, col: int, dp_array: list[list[int]]
    ) -> int:
        if row >= rows or col >= cols:
            return 0
        if dp_array[row][col] != -1:
            return dp_array[row][col]

        right = update_area_of_max_square_using_dp_array(row, col + 1, dp_array)
        diagonal = update_area_of_max_square_using_dp_array(row + 1, col + 1, dp_array)
        down = update_area_of_max_square_using_dp_array(row + 1, col, dp_array)

        if mat[row][col]:
            sub_problem_sol = 1 + min([right, diagonal, down])
            largest_square_area[0] = max(largest_square_area[0], sub_problem_sol)
            dp_array[row][col] = sub_problem_sol
            return sub_problem_sol
        else:
            return 0

    largest_square_area = [0]
    dp_array = [[-1] * cols for _ in range(rows)]
    update_area_of_max_square_using_dp_array(0, 0, dp_array)

    return largest_square_area[0]


def largest_square_area_in_matrix_bottom_up(
    rows: int, cols: int, mat: list[list[int]]
) -> int:
    """
    使用自底向上的方法更新 largest_square_area。

    >>> largest_square_area_in_matrix_bottom_up(2, 2, [[1,1], [1,1]])
    2
    >>> largest_square_area_in_matrix_bottom_up(2, 2, [[0,0], [0,0]])
    0

    """
    dp_array = [[0] * (cols + 1) for _ in range(rows + 1)]
    largest_square_area = 0
    for row in range(rows - 1, -1, -1):
        for col in range(cols - 1, -1, -1):
            right = dp_array[row][col + 1]
            diagonal = dp_array[row + 1][col + 1]
            bottom = dp_array[row + 1][col]

            if mat[row][col] == 1:
                dp_array[row][col] = 1 + min(right, diagonal, bottom)
                largest_square_area = max(dp_array[row][col], largest_square_area)
            else:
                dp_array[row][col] = 0

    return largest_square_area


def largest_square_area_in_matrix_bottom_up_space_optimization(
    rows: int, cols: int, mat: list[list[int]]
) -> int:
    """
    使用经过空间优化的自底向上方法更新 largest_square_area。

    >>> largest_square_area_in_matrix_bottom_up_space_optimization(2, 2, [[1,1], [1,1]])
    2
    >>> largest_square_area_in_matrix_bottom_up_space_optimization(2, 2, [[0,0], [0,0]])
    0
    """
    current_row = [0] * (cols + 1)
    next_row = [0] * (cols + 1)
    largest_square_area = 0
    for row in range(rows - 1, -1, -1):
        for col in range(cols - 1, -1, -1):
            right = current_row[col + 1]
            diagonal = next_row[col + 1]
            bottom = next_row[col]

            if mat[row][col] == 1:
                current_row[col] = 1 + min(right, diagonal, bottom)
                largest_square_area = max(current_row[col], largest_square_area)
            else:
                current_row[col] = 0
        next_row = current_row

    return largest_square_area


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(largest_square_area_in_matrix_bottom_up(2, 2, [[1, 1], [1, 1]]))
