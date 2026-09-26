"""
谢尔宾斯基地毯（Sierpinski Carpet）是 Wacław Sierpiński 于 1916 年首次描述的平面
分形。它是康托集的二维推广，与谢尔宾斯基三角形密切相关。

构造方法
    从实心正方形开始，将其划分为 3x3 网格中的九个相等子正方形，并移除中心
    正方形。然后对剩余八个子正方形无限递归地执行相同步骤。

判断 ``3**n x 3**n`` 网格中的单元格是填充状态（属于地毯）还是空洞的一种便捷
方法，是查看其行列索引的三进制数字：当且仅当某一层的行数字和列数字都等于
``1``（即该 3x3 块的中心）时，该单元格为空洞。

此模块完全使用整数运算构造地毯，因此每个函数都是确定性的，可使用 doctest
验证，无需绘图或 turtle 图形。

参考资料：https://en.wikipedia.org/wiki/Sierpi%C5%84ski_carpet
"""


def is_filled(row: int, col: int) -> bool:
    """
    当 (``row``, ``col``) 处的单元格属于地毯时返回 ``True``；当其位于某个被移除
    的中心正方形内时返回 ``False``。

    结果与分形深度无关：只要任意一对对应的三进制数字等于 ``(1, 1)``，该单元格
    就是空洞。

    >>> is_filled(0, 0)
    True
    >>> is_filled(1, 1)  # the very first central square is removed
    False
    >>> is_filled(4, 4)  # centre of the centre block -> still a hole
    False
    >>> is_filled(0, 4)
    True
    >>> [is_filled(1, col) for col in range(3)]
    [True, False, True]

    网格索引不能使用负坐标。

    >>> is_filled(-1, 0)
    Traceback (most recent call last):
        ...
    ValueError: row and col must be non-negative, got (-1, 0)
    """
    if row < 0 or col < 0:
        msg = f"row and col must be non-negative, got ({row}, {col})"
        raise ValueError(msg)
    while row > 0 or col > 0:
        if row % 3 == 1 and col % 3 == 1:
            return False
        row //= 3
        col //= 3
    return True


def generate_carpet(depth: int, filled: str = "#", hole: str = " ") -> list[str]:
    """
    将给定 ``depth`` 的谢尔宾斯基地毯构造为字符串列表。

    深度 ``0`` 表示单个填充单元格；每增加一层，边长扩大为三倍。

    >>> generate_carpet(0)
    ['#']
    >>> for line in generate_carpet(1):
    ...     print(line)
    ###
    # #
    ###
    >>> for line in generate_carpet(2, filled="X", hole="."):
    ...     print(line)
    XXXXXXXXX
    X.XX.XX.X
    XXXXXXXXX
    XXX...XXX
    X.X...X.X
    XXX...XXX
    XXXXXXXXX
    X.XX.XX.X
    XXXXXXXXX
    >>> generate_carpet(-1)
    Traceback (most recent call last):
        ...
    ValueError: depth must be non-negative, got -1
    """
    if depth < 0:
        msg = f"depth must be non-negative, got {depth}"
        raise ValueError(msg)
    size = 3**depth
    return [
        "".join(filled if is_filled(row, col) else hole for col in range(size))
        for row in range(size)
    ]


def count_filled_cells(depth: int) -> int:
    """
    返回给定 ``depth`` 的地毯中填充单元格的数量。

    每层保留九个子正方形中的八个，因此数量为 ``8**depth``。用暴力扫描验证该
    闭式结果是一项良好的健全性检查。

    >>> [count_filled_cells(depth) for depth in range(4)]
    [1, 8, 64, 512]
    >>> all(
    ...     count_filled_cells(depth)
    ...     == sum(line.count("#") for line in generate_carpet(depth))
    ...     for depth in range(4)
    ... )
    True
    """
    if depth < 0:
        msg = f"depth must be non-negative, got {depth}"
        raise ValueError(msg)
    return 8**depth


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    for carpet_line in generate_carpet(3):
        print(carpet_line)
