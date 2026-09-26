"""
用于计算凸多边形直径的旋转卡壳（Rotating Calipers）算法。

参考资料：
- https://en.wikipedia.org/wiki/Rotating_calipers
- https://cp-algorithms.com/geometry/convex-hull-kernel.html
- Toussaint, G. T. (1983). "Solving geometric problems with the rotating calipers".
  Proceedings of IEEE MELECON '83, Athens, Greece.

旋转卡壳方法可在 O(n log n) 时间内计算二维点集的直径（任意两点间的最大欧几里得距离），
其中构建凸包需要 O(n log n)，卡壳扫描需要 O(n)。
"""

from __future__ import annotations

import math
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


def cross_product(origin: Point, point_a: Point, point_b: Point) -> float:
    """
    计算向量 (origin -> point_a) 与 (origin -> point_b) 的二维叉积。

    返回值表示三角形 (origin, point_a, point_b) 带符号面积的两倍：
        > 0：逆时针转向（左转）
        < 0：顺时针转向（右转）
        = 0：三点共线

    >>> cross_product(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0))
    1.0
    >>> cross_product(Point(0.0, 0.0), Point(1.0, 1.0), Point(1.0, 0.0))
    -1.0
    >>> cross_product(Point(0.0, 0.0), Point(1.0, 1.0), Point(2.0, 2.0))
    0.0
    """
    return (point_a.x - origin.x) * (point_b.y - origin.y) - (point_a.y - origin.y) * (
        point_b.x - origin.x
    )


def distance_squared(point_a: Point, point_b: Point) -> float:
    """
    计算 point_a 与 point_b 之间欧几里得距离的平方。

    >>> distance_squared(Point(0.0, 0.0), Point(3.0, 4.0))
    25.0
    >>> distance_squared(Point(1.0, 1.0), Point(1.0, 1.0))
    0.0
    >>> distance_squared(Point(-1.0, -1.0), Point(2.0, 3.0))
    25.0
    """
    return (point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2


def convex_hull(points: list[Point]) -> list[Point]:
    """
    使用 Andrew 单调链算法，按逆时针顺序计算二维点集的凸包。

    时间复杂度：O(n log n)，其中 n 为点的数量。
    空间复杂度：O(n)

    >>> convex_hull([Point(0.0, 0.0), Point(1.0, 1.0)])
    [Point(x=0.0, y=0.0), Point(x=1.0, y=1.0)]
    >>> convex_hull([
    ...     Point(0.0, 0.0),
    ...     Point(3.0, 0.0),
    ...     Point(3.0, 3.0),
    ...     Point(0.0, 3.0),
    ...     Point(1.0, 1.0),
    ... ])
    [Point(x=0.0, y=0.0), Point(x=3.0, y=0.0), Point(x=3.0, y=3.0), Point(x=0.0, y=3.0)]
    >>> convex_hull([Point(0.0, 0.0), Point(1.0, 1.0), Point(2.0, 2.0)])
    [Point(x=0.0, y=0.0), Point(x=2.0, y=2.0)]
    >>> convex_hull([Point(1.0, 1.0)])
    [Point(x=1.0, y=1.0)]
    """
    unique_points = sorted(set(points))
    if len(unique_points) <= 1:
        return unique_points

    lower_hull: list[Point] = []
    for candidate_point in unique_points:
        while (
            len(lower_hull) >= 2
            and cross_product(lower_hull[-2], lower_hull[-1], candidate_point) <= 0.0
        ):
            lower_hull.pop()
        lower_hull.append(candidate_point)

    upper_hull: list[Point] = []
    for candidate_point in reversed(unique_points):
        while (
            len(upper_hull) >= 2
            and cross_product(upper_hull[-2], upper_hull[-1], candidate_point) <= 0.0
        ):
            upper_hull.pop()
        upper_hull.append(candidate_point)

    return lower_hull[:-1] + upper_hull[:-1]


def rotating_calipers(points: list[Point]) -> tuple[float, tuple[Point, Point]]:
    """
    使用旋转卡壳算法，求给定二维点集的最大欧几里得距离（多边形直径）及一对对踵点。

    时间复杂度：构建凸包为 O(n log n)，卡壳扫描为 O(n)。
    空间复杂度：O(n)，用于存储凸包。

    异常：
        ValueError：当提供的点少于 2 个时。

    >>> points = [
    ...     Point(0.0, 0.0),
    ...     Point(3.0, 0.0),
    ...     Point(3.0, 4.0),
    ...     Point(0.0, 4.0),
    ... ]
    >>> max_dist, pair = rotating_calipers(points)
    >>> max_dist
    5.0
    >>> pair in [
    ...     (Point(0.0, 0.0), Point(3.0, 4.0)),
    ...     (Point(3.0, 4.0), Point(0.0, 0.0)),
    ...     (Point(3.0, 0.0), Point(0.0, 4.0)),
    ...     (Point(0.0, 4.0), Point(3.0, 0.0)),
    ... ]
    True
    >>> rotating_calipers([Point(0.0, 0.0), Point(0.0, 5.0)])
    (5.0, (Point(x=0.0, y=0.0), Point(x=0.0, y=5.0)))
    >>> rotating_calipers([Point(1.0, 1.0), Point(1.0, 1.0)])
    (0.0, (Point(x=1.0, y=1.0), Point(x=1.0, y=1.0)))
    >>> rotating_calipers([
    ...     Point(0.0, 0.0),
    ...     Point(1.0, 1.0),
    ...     Point(2.0, 2.0),
    ...     Point(3.0, 3.0),
    ... ])[0]
    4.242640687119285
    >>> rotating_calipers([Point(1.0, 1.0)])
    Traceback (most recent call last):
        ...
    ValueError: At least 2 points are required to compute polygon diameter.
    """
    if len(points) < 2:
        raise ValueError("At least 2 points are required to compute polygon diameter.")

    hull = convex_hull(points)
    hull_size = len(hull)

    if hull_size == 1:
        return 0.0, (hull[0], hull[0])
    if hull_size == 2:
        return math.hypot(hull[0].x - hull[1].x, hull[0].y - hull[1].y), (
            hull[0],
            hull[1],
        )

    max_dist_squared = 0.0
    best_pair = (hull[0], hull[1])

    # 查找距离边 hull[0]-hull[1] 最远的初始对踵点
    antipodal_idx = 1
    while cross_product(
        hull[0], hull[1], hull[(antipodal_idx + 1) % hull_size]
    ) > cross_product(hull[0], hull[1], hull[antipodal_idx]):
        antipodal_idx = (antipodal_idx + 1) % hull_size

    for current_idx in range(hull_size):
        next_idx = (current_idx + 1) % hull_size
        while cross_product(
            hull[current_idx], hull[next_idx], hull[(antipodal_idx + 1) % hull_size]
        ) > cross_product(hull[current_idx], hull[next_idx], hull[antipodal_idx]):
            antipodal_idx = (antipodal_idx + 1) % hull_size

        for p in (hull[current_idx], hull[next_idx]):
            for candidate_idx in (antipodal_idx, (antipodal_idx + 1) % hull_size):
                dist_sq = distance_squared(p, hull[candidate_idx])
                if dist_sq > max_dist_squared:
                    max_dist_squared = dist_sq
                    best_pair = (p, hull[candidate_idx])

    return math.sqrt(max_dist_squared), best_pair


if __name__ == "__main__":
    import doctest

    doctest.testmod()
