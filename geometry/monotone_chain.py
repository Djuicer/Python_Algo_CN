"""
Andrew 单调链凸包算法（Monotone Chain Convex Hull Algorithm）。

参考资料：https://en.wikipedia.org/wiki/Convex_hull_algorithms#Andrew's_monotone_chain_algorithm
参考资料：Andrew, A. M. (1979). "Another efficient algorithm for convex hulls
           in two dimensions". Information Processing Letters, 9(5), 216-219.

Andrew 单调链算法以 O(n log n) 时间计算二维点集的凸包。它首先按字典序对点排序
（先按 x 坐标，若相同则按 y 坐标），随后分别用一次 O(n) 遍历构建下凸包和上凸包。
"""

from __future__ import annotations

from typing import NamedTuple


class Point(NamedTuple):
    """
    坐标为实数的二维点。

    >>> Point(0.0, 0.0)
    Point(x=0.0, y=0.0)
    >>> Point(1.5, -2.0)
    Point(x=1.5, y=-2.0)
    """

    x: float
    y: float


def cross_product_direction(origin: Point, point_a: Point, point_b: Point) -> float:
    """
    计算向量 (origin -> point_a) 与 (origin -> point_b) 的二维叉积。

    返回值表示有序三元组 (origin, point_a, point_b) 的方向：
        > 0：逆时针转向（左转）
        < 0：顺时针转向（右转）
        = 0：三点共线

    参数：
        origin：参考基点。
        point_a：第一个端点。
        point_b：第二个端点。

    返回：
        二维叉积的带符号数值。

    >>> cross_product_direction(Point(0, 0), Point(1, 0), Point(1, 1))
    1
    >>> cross_product_direction(Point(0, 0), Point(1, 1), Point(1, 0))
    -1
    >>> cross_product_direction(Point(0, 0), Point(1, 1), Point(2, 2))
    0
    """
    return (point_a.x - origin.x) * (point_b.y - origin.y) - (point_a.y - origin.y) * (
        point_b.x - origin.x
    )


def monotone_chain(points: list[Point]) -> list[Point]:
    """
    使用 Andrew 单调链算法，按逆时针顺序计算二维点集的凸包。

    参数：
        points：二维点列表。

    返回：
        按逆时针顺序构成凸包的顶点列表。

    时间复杂度：O(n log n)，其中 n 为点的数量。
    空间复杂度：O(n)

    示例：
    >>> monotone_chain([])
    []
    >>> monotone_chain([Point(1, 1)])
    [Point(x=1, y=1)]
    >>> monotone_chain([Point(0, 0), Point(1, 1)])
    [Point(x=0, y=0), Point(x=1, y=1)]
    >>> square_points = [
    ...     Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),
    ...     Point(1, 1), Point(1, 0.5)
    ... ]
    >>> monotone_chain(square_points)
    [Point(x=0, y=0), Point(x=2, y=0), Point(x=2, y=2), Point(x=0, y=2)]
    >>> triangle_with_duplicates = [
    ...     Point(0, 0), Point(4, 0), Point(2, 3),
    ...     Point(0, 0), Point(4, 0), Point(2, 1)
    ... ]
    >>> monotone_chain(triangle_with_duplicates)
    [Point(x=0, y=0), Point(x=4, y=0), Point(x=2, y=3)]
    >>> collinear_points = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)]
    >>> monotone_chain(collinear_points)
    [Point(x=0, y=0), Point(x=3, y=3)]
    """
    unique_sorted_points = sorted(set(points))
    if len(unique_sorted_points) <= 1:
        return unique_sorted_points

    # 构建下凸包：只保留逆时针转向
    lower_hull: list[Point] = []
    for candidate_point in unique_sorted_points:
        while (
            len(lower_hull) >= 2
            and cross_product_direction(lower_hull[-2], lower_hull[-1], candidate_point)
            <= 0
        ):
            lower_hull.pop()
        lower_hull.append(candidate_point)

    # 构建上凸包：只保留逆时针转向
    upper_hull: list[Point] = []
    for candidate_point in reversed(unique_sorted_points):
        while (
            len(upper_hull) >= 2
            and cross_product_direction(upper_hull[-2], upper_hull[-1], candidate_point)
            <= 0
        ):
            upper_hull.pop()
        upper_hull.append(candidate_point)

    # 每一半的最后一点会在端部重复，因此将其省略
    return lower_hull[:-1] + upper_hull[:-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
