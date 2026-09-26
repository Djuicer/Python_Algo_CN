"""
用于求点集凸包的 Graham 扫描（Graham Scan）算法。

Graham 扫描用于计算平面上有限点集的凸包，时间复杂度为 O(n log n)。
该算法以 Ronald Graham 命名，他于 1972 年发表了原始算法。

该算法按凸包边界顺序找出所有顶点，并使用栈高效识别和移除会形成非凸角的点。

参考资料：
- https://en.wikipedia.org/wiki/Graham_scan
- Graham, R.L. (1972). "An Efficient Algorithm for Determining the Convex Hull of a
  Finite Planar Set"
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T", bound="Point")


@dataclass
class Point:
    """
    二维空间中的点。

    >>> Point(0, 0)
    Point(x=0.0, y=0.0)
    >>> Point(1.5, 2.5)
    Point(x=1.5, y=2.5)
    """

    x: float
    y: float

    def __init__(self, x_coordinate: float, y_coordinate: float) -> None:
        """
        初始化一个二维点。

        参数：
            x_coordinate：点的 x 坐标（水平位置）
            y_coordinate：点的 y 坐标（垂直位置）
        """
        self.x = float(x_coordinate)
        self.y = float(y_coordinate)

    def __eq__(self, other: object) -> bool:
        """
        检查两个点是否相等。

        >>> Point(1, 2) == Point(1, 2)
        True
        >>> Point(1, 2) == Point(2, 1)
        False
        """
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: Point) -> bool:
        """
        比较两个点以进行排序（先按最下方，再按最左侧）。

        >>> Point(1, 2) < Point(1, 3)
        True
        >>> Point(1, 2) < Point(2, 2)
        True
        >>> Point(2, 2) < Point(1, 2)
        False
        """
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

    def euclidean_distance(self, other: Point) -> float:
        """
        计算两点之间的欧几里得距离。

        >>> Point(0, 0).euclidean_distance(Point(3, 4))
        5.0
        >>> Point(1, 1).euclidean_distance(Point(4, 5))
        5.0
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def consecutive_orientation(self, point_a: Point, point_b: Point) -> float:
        """
        计算向量 (self -> point_a) 与 (point_a -> point_b) 的叉积。

        返回：
        - 正值：逆时针转向
        - 负值：顺时针转向
        - 零：三点共线

        >>> Point(0, 0).consecutive_orientation(Point(1, 0), Point(1, 1))
        1.0
        >>> Point(0, 0).consecutive_orientation(Point(1, 0), Point(1, -1))
        -1.0
        >>> Point(0, 0).consecutive_orientation(Point(1, 0), Point(2, 0))
        0.0
        """
        return (point_a.x - self.x) * (point_b.y - point_a.y) - (point_a.y - self.y) * (
            point_b.x - point_a.x
        )


def graham_scan(points: Sequence[Point]) -> list[Point]:
    """
    使用 Graham 扫描算法求点集的凸包。

    算法步骤如下：
    1. 找到最下方的点（若并列则取最左侧）
    2. 以最下方的点为基准，按极角对其余点排序
    3. 按顺序处理各点，并用栈维护凸包候选点
    4. 移除会形成顺时针转向的点

    参数：
        points：Point 对象序列

    返回：
        按逆时针顺序表示凸包的 Point 对象列表。
        若不同的点少于 3 个或所有点共线，则返回空列表。

    时间复杂度：O(n log n)，由排序决定
    空间复杂度：O(n)，用于输出凸包

    >>> graham_scan([])
    []
    >>> graham_scan([Point(0, 0)])
    []
    >>> graham_scan([Point(0, 0), Point(1, 1)])
    []
    >>> hull = graham_scan([Point(0, 0), Point(1, 0), Point(0.5, 1)])
    >>> len(hull)
    3
    >>> Point(0, 0) in hull and Point(1, 0) in hull and Point(0.5, 1) in hull
    True
    """
    if len(points) <= 2:
        return []

    # 找到最下方的点（若并列则取最左侧）
    min_point = min(points)

    # 从列表中移除 min_point
    points_list = [p for p in points if p != min_point]
    if not points_list:
        # 处理所有点均相同的边界情况
        return []

    def polar_angle_key(point: Point) -> tuple[float, float, float]:
        """
        以 min_point 为基准按极角排序各点的键函数。

        各点按逆时针顺序排列。当两个点的角度相同时，距离较远的点排在前面
        （稍后会移除重复点）。
        """
        # 使用虚拟的第三个点（min_point 本身）计算相对角度
        # 改为直接计算点之间的角度
        dx = point.x - min_point.x
        dy = point.y - min_point.y

        # 使用 atan2 计算角度，也可以使用叉积进行比较
        # 排序时比较相邻点之间的方向
        distance = min_point.euclidean_distance(point)
        return (dx, dy, -distance)  # 使用负距离，使较远的点排在前面

    # 使用基于叉积的比较按极角排序
    def compare_points(point_a: Point, point_b: Point) -> int:
        """以 min_point 为基准，按极角比较两个点。"""
        orientation = min_point.consecutive_orientation(point_a, point_b)
        if orientation < 0.0:
            return 1  # point_a 位于 point_b 之后（顺时针）
        elif orientation > 0.0:
            return -1  # point_a 位于 point_b 之前（逆时针）
        else:
            # 共线时，较远的点应排在前面
            dist_a = min_point.euclidean_distance(point_a)
            dist_b = min_point.euclidean_distance(point_b)
            if dist_b < dist_a:
                return -1
            elif dist_b > dist_a:
                return 1
            else:
                return 0

    from functools import cmp_to_key

    points_list.sort(key=cmp_to_key(compare_points))

    # 构建凸包
    convex_hull: list[Point] = [min_point, points_list[0]]

    for point in points_list[1:]:
        # 跳过角度相同的连续点（与 min_point 共线）
        if min_point.consecutive_orientation(point, convex_hull[-1]) == 0.0:
            continue

        # 移除形成顺时针转向（或共线）的点
        while len(convex_hull) >= 2:
            orientation = convex_hull[-2].consecutive_orientation(
                convex_hull[-1], point
            )
            if orientation <= 0.0:
                convex_hull.pop()
            else:
                break

        convex_hull.append(point)

    # 有效凸包至少需要 3 个点
    if len(convex_hull) <= 2:
        return []

    return convex_hull


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 使用示例
    points = [
        Point(0, 0),
        Point(1, 0),
        Point(2, 0),
        Point(2, 1),
        Point(2, 2),
        Point(1, 2),
        Point(0, 2),
        Point(0, 1),
        Point(1, 1),  # 内部点
    ]

    hull = graham_scan(points)
    print("Convex hull vertices:")
    for point in hull:
        print(f"  ({point.x}, {point.y})")
