"""
https://en.wikipedia.org/wiki/Median
"""


def median(matrix: list[list[int]]) -> int:
    """
    计算已排序矩阵的中位数。

    参数：
        matrix: 整数组成的二维矩阵。

    返回：
        矩阵的中位数。

    示例：
        >>> matrix = [[1, 3, 5], [2, 6, 9], [3, 6, 9]]
        >>> median(matrix)
        5

        >>> matrix = [[1, 2, 3], [4, 5, 6]]
        >>> median(matrix)
        3
    """
    # 将矩阵展平为已排序的一维列表
    linear = sorted(num for row in matrix for num in row)

    # 计算中间索引
    mid = (len(linear) - 1) // 2

    # 返回中位数
    return linear[mid]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
