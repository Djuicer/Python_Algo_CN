"""
凸包（Convex Hull）问题是在平面点集中，找出凸多边形 P 的所有顶点，
使所有点都位于 P 的顶点上或
P 的内部。凸包问题在几何问题、
计算机图形学和游戏开发中有多种应用。

此处实现了两种求解凸包问题的算法。
1. 时间复杂度为 O(n^3) 的暴力算法
2. 时间复杂度为 O(n log(n)) 的分治算法

凸包问题还有其他多种算法，
此处尚未实现。

"""

from __future__ import annotations

from collections.abc import Iterable


class Point:
    """
    定义供所有凸包算法使用的二维点。

    参数
    ----------
    x: int 或 float，二维点的 x 坐标
    y: int 或 float，二维点的 y 坐标

    示例
    --------
    >>> Point(1, 2)
    (1.0, 2.0)
    >>> Point("1", "2")
    (1.0, 2.0)
    >>> Point(1, 2) > Point(0, 1)
    True
    >>> Point(1, 1) == Point(1, 1)
    True
    >>> Point(-0.5, 1) == Point(0.5, 1)
    False
    >>> Point("pi", "e")
    Traceback (most recent call last):
        ...
    ValueError: could not convert string to float: 'pi'
    """

    def __init__(self, x, y) -> None:
        self.x, self.y = float(x), float(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if self.x > other.x:
            return True
        elif self.x == other.x:
            return self.y > other.y
        return False

    def __lt__(self, other):
        return not self > other

    def __ge__(self, other):
        if self.x > other.x:
            return True
        elif self.x == other.x:
            return self.y >= other.y
        return False

    def __le__(self, other):
        if self.x < other.x:
            return True
        elif self.x == other.x:
            return self.y <= other.y
        return False

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash(self.x)


def _construct_points(
    list_of_tuples: list[Point] | list[list[float]] | Iterable[list[float]],
) -> list[Point]:
    """
    从包含数值的类数组对象构造点列表

    参数
    ---------

    list_of_tuples: 包含数值的类数组对象。目前支持的类型
    包括列表、元组和集合。

    返回
    --------
    points: 每个元素均为 Point 类型的列表。仅包含
    可转换为 Point 的对象。

    示例
    -------
    >>> _construct_points([[1, 1], [2, -1], [0.3, 4]])
    [(1.0, 1.0), (2.0, -1.0), (0.3, 4.0)]
    >>> _construct_points([1, 2])
    Ignoring deformed point 1. All points must have at least 2 coordinates.
    Ignoring deformed point 2. All points must have at least 2 coordinates.
    []
    >>> _construct_points([])
    []
    >>> _construct_points(None)
    []
    """

    points: list[Point] = []
    if list_of_tuples:
        for p in list_of_tuples:
            if isinstance(p, Point):
                points.append(p)
            else:
                try:
                    points.append(Point(p[0], p[1]))
                except IndexError, TypeError:
                    print(
                        f"Ignoring deformed point {p}. All points"
                        " must have at least 2 coordinates."
                    )
    return points


def _validate_input(points: list[Point] | list[list[float]]) -> list[Point]:
    """
    在凸包算法使用输入实例之前对其进行验证

    参数
    ---------
    points: 类数组对象，使用凸包算法前待验证的
    二维点。points 的元素必须是列表、元组或
    Point。

    返回
    -------
    points: array_like，包含传入数据构造出的所有有效 Point 的可迭代对象。


    异常
    ---------
    ValueError: points 为空或为 None，或者传入标量等不正确的
                 数据结构时抛出

    TypeError: 传入可迭代但无法按索引访问的对象（如字典）时抛出。
                集合除外，使用前会将其转换为列表


    示例
    -------
    >>> _validate_input([[1, 2]])
    [(1.0, 2.0)]
    >>> _validate_input([(1, 2)])
    [(1.0, 2.0)]
    >>> _validate_input([Point(2, 1), Point(-1, 2)])
    [(2.0, 1.0), (-1.0, 2.0)]
    >>> _validate_input([])
    Traceback (most recent call last):
        ...
    ValueError: Expecting a list of points but got []
    >>> _validate_input(1)
    Traceback (most recent call last):
        ...
    ValueError: Expecting an iterable object but got an non-iterable type 1
    """

    if not hasattr(points, "__iter__"):
        msg = f"Expecting an iterable object but got an non-iterable type {points}"
        raise ValueError(msg)

    if not points:
        msg = f"Expecting a list of points but got {points}"
        raise ValueError(msg)

    return _construct_points(points)


def _det(a: Point, b: Point, c: Point) -> float:
    """
    计算二维点 c 到线段 ab 的带符号垂直距离。
    符号表示 c 相对于 ab 的方向：正值表示 c 位于 ab 上方（左侧），
    负值表示 c 位于 ab 下方（右侧），0 表示三点共线。

    此外，0.5 * abs|det| 是三角形 abc 的面积

    参数
    ----------
    a: point，线段 ab 左端的点
    b: point，线段 ab 右端的点
    c: point，待确定其方向和位置的点。

    返回
    --------
    det: float，abs(det) 是 c 到 ab 的距离。符号表示 c 位于线段 ab 的哪一侧。
    det 的计算公式为
    (a_xb_y + c_xa_y + b_xc_y) - (a_yb_x + c_ya_x + b_yc_x)

    示例
    ----------
    >>> _det(Point(1, 1), Point(1, 2), Point(1, 5))
    0.0
    >>> _det(Point(0, 0), Point(10, 0), Point(0, 10))
    100.0
    >>> _det(Point(0, 0), Point(10, 0), Point(0, -10))
    -100.0
    """

    det = (a.x * b.y + b.x * c.y + c.x * a.y) - (a.y * b.x + b.y * c.x + c.y * a.x)
    return det


def convex_hull_bf(points: list[Point]) -> list[Point]:
    """
    使用暴力算法构造二维点集的凸包。
    该算法考虑所有点对组合 (i, j)，并根据
    凸性的定义判断 (i, j) 是否属于
    凸包。当且仅当连接 i、j 的线段两侧不存在同时分布的点，
    且不存在位于该线段任一端之外的点 k 时，
    (i, j) 属于凸包。

    运行时间：O(n^3)，效率很低

    参数
    ---------
    points: 由 Point、列表或元组组成的类数组对象。
    需要求凸包的二维点集

    返回
    ------
    convex_set: list，按非递减顺序排列的凸包点集。

    另请参阅
    --------
    convex_hull_recursive,

     示例
     ---------
     >>> convex_hull_bf([[0, 0], [1, 0], [10, 1]])
     [(0.0, 0.0), (1.0, 0.0), (10.0, 1.0)]
     >>> convex_hull_bf([[0, 0], [1, 0], [10, 0]])
     [(0.0, 0.0), (10.0, 0.0)]
     >>> convex_hull_bf([[-1, 1],[-1, -1], [0, 0], [0.5, 0.5], [1, -1], [1, 1],
     ...                 [-0.75, 1]])
     [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]
     >>> convex_hull_bf([(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3),
     ...                 (2, -1), (2, -4), (1, -3)])
     [(0.0, 0.0), (0.0, 3.0), (1.0, -3.0), (2.0, -4.0), (3.0, 0.0), (3.0, 3.0)]
    """

    points = sorted(_validate_input(points))
    n = len(points)
    convex_set = set()

    for i in range(n - 1):
        for j in range(i + 1, n):
            points_left_of_ij = points_right_of_ij = False
            ij_part_of_convex_hull = True
            for k in range(n):
                if k not in {i, j}:
                    det_k = _det(points[i], points[j], points[k])

                    if det_k > 0:
                        points_left_of_ij = True
                    elif det_k < 0:
                        points_right_of_ij = True
                    # point[i]、point[j]、point[k] 位于同一直线上
                    # 如果 point[k] 位于 point[i] 左侧，或位于
                    # point[j] 右侧，则 point[i]、point[j] 不能共同
                    # 构成 A 的凸包边
                    elif points[k] < points[i] or points[k] > points[j]:
                        ij_part_of_convex_hull = False
                        break

                if points_left_of_ij and points_right_of_ij:
                    ij_part_of_convex_hull = False
                    break

            if ij_part_of_convex_hull:
                convex_set.update([points[i], points[j]])

    return sorted(convex_set)


def convex_hull_recursive(points: list[Point]) -> list[Point]:
    """
    使用分治策略构造二维点集的凸包
    该算法利用问题的几何性质，反复
    将点集划分为更小的凸包，并求出
    这些较小凸包的凸包。较小凸包所得结果的并集，
    就是较大问题的凸包解。

    参数
    ---------
    points: 由 Point、列表或元组组成的类数组对象。
    需要求凸包的二维点集

    运行时间：O(n log n)

    返回
    -------
    convex_set: list，按非递减顺序排列的凸包点集。

    示例
    ---------
    >>> convex_hull_recursive([[0, 0], [1, 0], [10, 1]])
    [(0.0, 0.0), (1.0, 0.0), (10.0, 1.0)]
    >>> convex_hull_recursive([[0, 0], [1, 0], [10, 0]])
    [(0.0, 0.0), (10.0, 0.0)]
    >>> convex_hull_recursive([[-1, 1],[-1, -1], [0, 0], [0.5, 0.5], [1, -1], [1, 1],
    ...                        [-0.75, 1]])
    [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]
    >>> convex_hull_recursive([(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3),
    ...                        (2, -1), (2, -4), (1, -3)])
    [(0.0, 0.0), (0.0, 3.0), (1.0, -3.0), (2.0, -4.0), (3.0, 0.0), (3.0, 3.0)]

    """
    points = sorted(_validate_input(points))
    n = len(points)

    # 将所有点划分为上凸包和下凸包
    # 根据定义，最左点和最右点一定
    # 属于凸包。
    # 以这两个点为基准，将所有点划分为
    # 上凸包和下凸包。

    # 连接两个端点的直线左侧（上方）的所有点属于
    # 上凸包
    # 连接两个端点的直线右侧（下方）的所有点属于
    # 下凸包
    # 忽略连接两个端点的直线上的所有点，因为它们不能
    # 成为凸包的顶点

    left_most_point = points[0]
    right_most_point = points[n - 1]

    convex_set = {left_most_point, right_most_point}
    upper_hull = []
    lower_hull = []

    for i in range(1, n - 1):
        det = _det(left_most_point, right_most_point, points[i])

        if det > 0:
            upper_hull.append(points[i])
        elif det < 0:
            lower_hull.append(points[i])

    _construct_hull(upper_hull, left_most_point, right_most_point, convex_set)
    _construct_hull(lower_hull, right_most_point, left_most_point, convex_set)

    return sorted(convex_set)


def _construct_hull(
    points: list[Point], left: Point, right: Point, convex_set: set[Point]
) -> None:
    """

    参数
    ---------
    points: list 或 None，用于选择下一个凸包顶点的
        点集
    left: Point，连接 left 和 right 的线段左端点
    right: 连接 left 和 right 的线段右端点
    convex_set: set，当前凸包。此函数会更新
        convex-set 的状态

    注意
    ----
    对于线段 'ab'，'a' 在左，'b' 在右。
    对于线段 'ba' 则相反。

    返回
    -------
    无返回值，仅更新 convex-set 的状态
    """
    if points:
        extreme_point = None
        extreme_point_distance = float("-inf")
        candidate_points = []

        for p in points:
            det = _det(left, right, p)

            if det > 0:
                candidate_points.append(p)

                if det > extreme_point_distance:
                    extreme_point_distance = det
                    extreme_point = p

        if extreme_point:
            _construct_hull(candidate_points, left, extreme_point, convex_set)
            convex_set.add(extreme_point)
            _construct_hull(candidate_points, extreme_point, right, convex_set)


def convex_hull_melkman(points: list[Point]) -> list[Point]:
    """
    使用 Melkman 算法构造二维点集的凸包。
    该算法依次插入简单折线上的点
    （即连接相邻点的线段彼此不相交）。
    对点排序可以得到这样的折线。

    详细说明见 http://cgm.cs.mcgill.ca/~athens/cs601/Melkman.html

    运行时间：O(n log n)；输入点已排序时为 O(n)

    参数
    ---------
    points: 由 Point、列表或元组组成的类数组对象。
    需要求凸包的二维点集

    返回
    ------
    convex_set: list，按非递减顺序排列的凸包点集。

    另请参阅
    --------

    示例
    ---------
    >>> convex_hull_melkman([[0, 0], [1, 0], [10, 1]])
    [(0.0, 0.0), (1.0, 0.0), (10.0, 1.0)]
    >>> convex_hull_melkman([[0, 0], [1, 0], [10, 0]])
    [(0.0, 0.0), (10.0, 0.0)]
    >>> convex_hull_melkman([[-1, 1],[-1, -1], [0, 0], [0.5, 0.5], [1, -1], [1, 1],
    ...                 [-0.75, 1]])
    [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]
    >>> convex_hull_melkman([(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3),
    ...                 (2, -1), (2, -4), (1, -3)])
    [(0.0, 0.0), (0.0, 3.0), (1.0, -3.0), (2.0, -4.0), (3.0, 0.0), (3.0, 3.0)]
    """
    points = sorted(_validate_input(points))
    n = len(points)

    convex_hull = points[:2]
    for i in range(2, n):
        det = _det(convex_hull[1], convex_hull[0], points[i])
        if det > 0:
            convex_hull.insert(0, points[i])
            break
        if det < 0:
            convex_hull.append(points[i])
            break
        convex_hull[1] = points[i]
    i += 1

    for j in range(i, n):
        if (
            _det(convex_hull[0], convex_hull[-1], points[j]) > 0
            and _det(convex_hull[-1], convex_hull[0], points[1]) < 0
        ):
            # 该点位于凸包内部
            continue

        convex_hull.insert(0, points[j])
        convex_hull.append(points[j])
        while _det(convex_hull[0], convex_hull[1], convex_hull[2]) >= 0:
            del convex_hull[1]
        while _det(convex_hull[-1], convex_hull[-2], convex_hull[-3]) <= 0:
            del convex_hull[-2]

    # `convex_hull` 按环绕顺序保存凸包顶点
    return sorted(convex_hull[1:] if len(convex_hull) > 3 else convex_hull)


def main() -> None:
    points = [
        (0, 3),
        (2, 2),
        (1, 1),
        (2, 1),
        (3, 0),
        (0, 0),
        (3, 3),
        (2, -1),
        (2, -4),
        (1, -3),
    ]
    # 凸包点集为
    # [(0, 0), (0, 3), (1, -3), (2, -4), (3, 0), (3, 3)]
    results_bf = convex_hull_bf(points)

    results_recursive = convex_hull_recursive(points)
    assert results_bf == results_recursive

    results_melkman = convex_hull_melkman(points)
    assert results_bf == results_melkman

    print(results_bf)


if __name__ == "__main__":
    main()
