"""
本程序以螺旋顺序输出矩阵，并使用递归方法求解。
      矩阵必须满足以下条件：
        i) 矩阵只能是一维或二维
        ii) 所有行的列数必须相等
"""


def check_matrix(matrix: list[list[int]]) -> bool:
    # 必须满足条件
    matrix = [list(row) for row in matrix]
    if matrix and isinstance(matrix, list):
        if isinstance(matrix[0], list):
            prev_len = 0
            for row in matrix:
                if prev_len == 0:
                    prev_len = len(row)
                    result = True
                else:
                    result = prev_len == len(row)
        else:
            result = True
    else:
        result = False

    return result


def spiral_print_clockwise(a: list[list[int]]) -> None:
    """
    >>> spiral_print_clockwise([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    1
    2
    3
    4
    8
    12
    11
    10
    9
    5
    6
    7
    """
    if check_matrix(a) and len(a) > 0:
        a = [list(row) for row in a]
        mat_row = len(a)
        if isinstance(a[0], list):
            mat_col = len(a[0])
        else:
            for dat in a:
                print(dat)
            return

        # 水平方向递增输出
        for i in range(mat_col):
            print(a[0][i])
        # 垂直向下输出
        for i in range(1, mat_row):
            print(a[i][mat_col - 1])
        # 水平方向递减输出
        if mat_row > 1:
            for i in range(mat_col - 2, -1, -1):
                print(a[mat_row - 1][i])
        # 垂直向上输出
        for i in range(mat_row - 2, 0, -1):
            print(a[i][0])
        remain_mat = [row[1 : mat_col - 1] for row in a[1 : mat_row - 1]]
        if len(remain_mat) > 0:
            spiral_print_clockwise(remain_mat)
        else:
            return
    else:
        print("Not a valid matrix")
        return


# 另一种易于理解的方法


def spiral_traversal(matrix: list[list]) -> list[int]:
    """
    >>> spiral_traversal([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]

    示例：
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    算法：
        第 1 步：先弹出索引为 0 的列表（即 [1,2,3,4]），并拼接第 2 步的输出。
        第 2 步：对矩阵执行转置操作（行列互换），再反转所得矩阵。
        第 3 步：将第 2 步的输出传给同一递归函数，直至到达基本情况。
    推演：
    阶段 1。
    [1, 2, 3, 4] +   spiral_traversal([
        [8, 12], [7, 11], [6, 10], [5, 9]]
     ])
    阶段 2。
    [1, 2, 3, 4, 8, 12] + spiral_traversal([
        [11, 10, 9], [7, 6, 5]
    ])
    阶段 3。
    [1, 2, 3, 4, 8, 12, 11, 10, 9] + spiral_traversal([
        [5], [6], [7]
    ])
    阶段 4。
    [1, 2, 3, 4, 8, 12, 11, 10, 9, 5] + spiral_traversal([
        [5], [6], [7]
    ])
    阶段 5。
    [1, 2, 3, 4, 8, 12, 11, 10, 9, 5] + spiral_traversal([[6, 7]])
    阶段 6。
    [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7] + spiral_traversal([])
    """
    if matrix:
        return list(matrix.pop(0)) + spiral_traversal(
            [list(row) for row in zip(*matrix)][::-1]
        )
    else:
        return []


# 驱动代码
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    a = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    spiral_print_clockwise(a)
