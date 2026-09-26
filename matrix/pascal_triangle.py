"""
本实现演示如何生成 Pascal 三角形的元素。行索引为 r、列索引为 c 的元素可由
下式推导：
triangle[r][c] = triangle[r-1][c-1]+triangle[r-1][c]

Pascal 三角形是由二项式系数组成的三角形数组。
https://en.wikipedia.org/wiki/Pascal%27s_triangle
"""


def print_pascal_triangle(num_rows: int) -> None:
    """
    输出具有不同给定行数的 Pascal 三角形。
    >>> print_pascal_triangle(5)
        1
       1 1
      1 2 1
     1 3 3 1
    1 4 6 4 1
    """
    triangle = generate_pascal_triangle(num_rows)
    for row_idx in range(num_rows):
        # 输出左侧空格
        for _ in range(num_rows - row_idx - 1):
            print(end=" ")
        # 输出行中的值
        for col_idx in range(row_idx + 1):
            if col_idx != row_idx:
                print(triangle[row_idx][col_idx], end=" ")
            else:
                print(triangle[row_idx][col_idx], end="")
        print()


def generate_pascal_triangle(num_rows: int) -> list[list[int]]:
    """
    创建具有不同给定行数的 Pascal 三角形。
    >>> generate_pascal_triangle(0)
    []
    >>> generate_pascal_triangle(1)
    [[1]]
    >>> generate_pascal_triangle(2)
    [[1], [1, 1]]
    >>> generate_pascal_triangle(3)
    [[1], [1, 1], [1, 2, 1]]
    >>> generate_pascal_triangle(4)
    [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]
    >>> generate_pascal_triangle(5)
    [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    >>> generate_pascal_triangle(-5)
    Traceback (most recent call last):
        ...
    ValueError: The input value of 'num_rows' should be greater than or equal to 0
    >>> generate_pascal_triangle(7.89)
    Traceback (most recent call last):
        ...
    TypeError: The input value of 'num_rows' should be 'int'
    """

    if not isinstance(num_rows, int):
        raise TypeError("The input value of 'num_rows' should be 'int'")

    if num_rows == 0:
        return []
    elif num_rows < 0:
        raise ValueError(
            "The input value of 'num_rows' should be greater than or equal to 0"
        )

    triangle: list[list[int]] = []
    for current_row_idx in range(num_rows):
        current_row = populate_current_row(triangle, current_row_idx)
        triangle.append(current_row)
    return triangle


def populate_current_row(triangle: list[list[int]], current_row_idx: int) -> list[int]:
    """
    >>> triangle = [[1]]
    >>> populate_current_row(triangle, 1)
    [1, 1]
    """
    current_row = [-1] * (current_row_idx + 1)
        # 当前行的首尾元素均为 1
    current_row[0], current_row[-1] = 1, 1
    for current_col_idx in range(1, current_row_idx):
        calculate_current_element(
            triangle, current_row, current_row_idx, current_col_idx
        )
    return current_row


def calculate_current_element(
    triangle: list[list[int]],
    current_row: list[int],
    current_row_idx: int,
    current_col_idx: int,
) -> None:
    """
    >>> triangle = [[1], [1, 1]]
    >>> current_row = [1, -1, 1]
    >>> calculate_current_element(triangle, current_row, 2, 1)
    >>> current_row
    [1, 2, 1]
    """
    above_to_left_elt = triangle[current_row_idx - 1][current_col_idx - 1]
    above_to_right_elt = triangle[current_row_idx - 1][current_col_idx]
    current_row[current_col_idx] = above_to_left_elt + above_to_right_elt


def generate_pascal_triangle_optimized(num_rows: int) -> list[list[int]]:
    """
    根据给定的 Pascal 三角形行数，返回表示相应 Pascal 三角形的矩阵。
    该函数通过消除冗余计算，将生成一行所需的运算量减半。

    :param num_rows: 指定 Pascal 三角形行数的整数
    :return: 表示 Pascal 三角形的二维列表（矩阵）

    返回具有给定行数的 Pascal 三角形。
    >>> generate_pascal_triangle_optimized(3)
    [[1], [1, 1], [1, 2, 1]]
    >>> generate_pascal_triangle_optimized(1)
    [[1]]
    >>> generate_pascal_triangle_optimized(0)
    []
    >>> generate_pascal_triangle_optimized(-5)
    Traceback (most recent call last):
        ...
    ValueError: The input value of 'num_rows' should be greater than or equal to 0
    >>> generate_pascal_triangle_optimized(7.89)
    Traceback (most recent call last):
        ...
    TypeError: The input value of 'num_rows' should be 'int'
    """

    if not isinstance(num_rows, int):
        raise TypeError("The input value of 'num_rows' should be 'int'")

    if num_rows == 0:
        return []
    elif num_rows < 0:
        raise ValueError(
            "The input value of 'num_rows' should be greater than or equal to 0"
        )

    result: list[list[int]] = [[1]]

    for row_index in range(1, num_rows):
        temp_row = [0] + result[-1] + [0]
        row_length = row_index + 1
    # 计算一行中不同元素的数量
        distinct_elements = sum(divmod(row_length, 2))
        row_first_half = [
            temp_row[i - 1] + temp_row[i] for i in range(1, distinct_elements + 1)
        ]
        row_second_half = row_first_half[: (row_index + 1) // 2]
        row_second_half.reverse()
        row = row_first_half + row_second_half
        result.append(row)

    return result


def benchmark() -> None:
    """
    使用三种不同长度的整数值对多个函数进行基准测试。
    """
    from collections.abc import Callable
    from timeit import timeit

    def benchmark_a_function(func: Callable, value: int) -> None:
        call = f"{func.__name__}({value})"
        timing = timeit(f"__main__.{call}", setup="import __main__")
        # print(f"{call:38} = {func(value)} -- {timing:.4f} seconds")
        print(f"{call:38} -- {timing:.4f} seconds")

    for value in range(15):  # (1, 7, 14):
        for func in (generate_pascal_triangle, generate_pascal_triangle_optimized):
            benchmark_a_function(func, value)
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
