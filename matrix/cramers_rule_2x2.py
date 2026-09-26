# https://www.chilimath.com/lessons/advanced-algebra/cramers-rule-with-two-variables
# https://en.wikipedia.org/wiki/Cramer%27s_rule


def cramers_rule_2x2(equation1: list[int], equation2: list[int]) -> tuple[float, float]:
    """
    求解含两个变量的线性方程组。
    :param: equation1: 包含 3 个数的列表
    :param: equation2: 包含 3 个数的列表
    :return: 结果字符串
    输入格式：[a1, b1, d1], [a2, b2, d2]
    determinant = [[a1, b1], [a2, b2]]
    determinant_x = [[d1, b1], [d2, b2]]
    determinant_y = [[a1, d1], [a2, d2]]

    >>> cramers_rule_2x2([2, 3, 0], [5, 1, 0])
    (0.0, 0.0)
    >>> cramers_rule_2x2([0, 4, 50], [2, 0, 26])
    (13.0, 12.5)
    >>> cramers_rule_2x2([11, 2, 30], [1, 0, 4])
    (4.0, -7.0)
    >>> cramers_rule_2x2([4, 7, 1], [1, 2, 0])
    (2.0, -1.0)

    >>> cramers_rule_2x2([1, 2, 3], [2, 4, 6])
    Traceback (most recent call last):
        ...
    ValueError: Infinite solutions. (Consistent system)
    >>> cramers_rule_2x2([1, 2, 3], [2, 4, 7])
    Traceback (most recent call last):
        ...
    ValueError: No solution. (Inconsistent system)
    >>> cramers_rule_2x2([1, 2, 3], [11, 22])
    Traceback (most recent call last):
        ...
    ValueError: Please enter a valid equation.
    >>> cramers_rule_2x2([0, 1, 6], [0, 0, 3])
    Traceback (most recent call last):
        ...
    ValueError: No solution. (Inconsistent system)
    >>> cramers_rule_2x2([0, 0, 6], [0, 0, 3])
    Traceback (most recent call last):
        ...
    ValueError: Both a & b of two equations can't be zero.
    >>> cramers_rule_2x2([1, 2, 3], [1, 2, 3])
    Traceback (most recent call last):
        ...
    ValueError: Infinite solutions. (Consistent system)
    >>> cramers_rule_2x2([0, 4, 50], [0, 3, 99])
    Traceback (most recent call last):
        ...
    ValueError: No solution. (Inconsistent system)
    """

    # 检查输入是否有效
    if not len(equation1) == len(equation2) == 3:
        raise ValueError("Please enter a valid equation.")
    if equation1[0] == equation1[1] == equation2[0] == equation2[1] == 0:
        raise ValueError("Both a & b of two equations can't be zero.")

    # 提取系数
    a1, b1, c1 = equation1
    a2, b2, c2 = equation2

    # 计算各矩阵的行列式
    determinant = a1 * b2 - a2 * b1
    determinant_x = c1 * b2 - c2 * b1
    determinant_y = a1 * c2 - a2 * c1

    # 使用克拉默法则检查线性方程组是否有解
    if determinant == 0:
        if determinant_x == determinant_y == 0:
            raise ValueError("Infinite solutions. (Consistent system)")
        raise ValueError("No solution. (Inconsistent system)")
    if determinant_x == determinant_y == 0:
        # 平凡解（不相容方程组）
        return (0.0, 0.0)
    else:
        x = determinant_x / determinant
        y = determinant_y / determinant
    # 非平凡解（相容方程组）
        return (x, y)
