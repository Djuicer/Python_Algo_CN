"""
给定两条线段，判断它们是否相交。

本实现基于《算法导论》（CLRS）第 33 章所述算法。

参考资料：
    - https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    - https://en.wikipedia.org/wiki/Orientation_(geometry)
"""

from __future__ import annotations

from typing import NamedTuple


class Point(NamedTuple):
    """二维空间中的点。

    >>> Point(0, 0)
    Point(x=0, y=0)
    >>> Point(1, -3)
    Point(x=1, y=-3)
    """

    x: float
    y: float


def direction(pivot: Point, target: Point, query: Point) -> float:
    """返回向量 (pivot->query) 与 (pivot->target) 的叉积。

    结果的符号表示有序三元组 (pivot, target, query) 的方向：
      - 负值 -> 逆时针（左转）
      - 正值 -> 顺时针（右转）
      - 零   -> 共线

    >>> direction(Point(0, 0), Point(1, 0), Point(0, 1))
    -1
    >>> direction(Point(0, 0), Point(0, 1), Point(1, 0))
    1
    >>> direction(Point(0, 0), Point(1, 1), Point(2, 2))
    0
    """
    return (query.x - pivot.x) * (target.y - pivot.y) - (target.x - pivot.x) * (
        query.y - pivot.y
    )


def on_segment(seg_start: Point, seg_end: Point, point: Point) -> bool:
    """检查已知与线段共线的 *point* 是否位于该线段上。

    >>> on_segment(Point(0, 0), Point(4, 4), Point(2, 2))
    True
    >>> on_segment(Point(0, 0), Point(4, 4), Point(5, 5))
    False
    >>> on_segment(Point(0, 0), Point(4, 0), Point(2, 0))
    True
    """
    return min(seg_start.x, seg_end.x) <= point.x <= max(
        seg_start.x, seg_end.x
    ) and min(seg_start.y, seg_end.y) <= point.y <= max(seg_start.y, seg_end.y)


def segments_intersect(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    """若线段 p1p2 与线段 p3p4 相交，则返回 True。

    使用 CLRS 的叉积/方向方法。既处理一般情况（正规相交），也处理某个端点
    恰好位于另一条线段上的退化情况。

    >>> segments_intersect(Point(0, 0), Point(2, 2), Point(0, 2), Point(2, 0))
    True
    >>> segments_intersect(Point(0, 0), Point(2, 2), Point(1, 1), Point(3, 3))
    True
    >>> segments_intersect(Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0))
    False
    >>> segments_intersect(Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 1))
    False
    >>> segments_intersect(Point(0, 0), Point(1, 1), Point(0, 1), Point(0, 2))
    False
    >>> segments_intersect(Point(0, 0), Point(1, 0), Point(1, 0), Point(2, 0))
    True
    """
    d1 = direction(p3, p4, p1)
    d2 = direction(p3, p4, p2)
    d3 = direction(p1, p2, p3)
    d4 = direction(p1, p2, p4)

    if ((d1 < 0 < d2) or (d2 < 0 < d1)) and ((d3 < 0 < d4) or (d4 < 0 < d3)):
        return True

    if d1 == 0 and on_segment(p3, p4, p1):
        return True
    if d2 == 0 and on_segment(p3, p4, p2):
        return True
    if d3 == 0 and on_segment(p1, p2, p3):
        return True
    return d4 == 0 and on_segment(p1, p2, p4)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Enter four points as 'x y' pairs (one per line):")
    points = [Point(*map(float, input().split())) for _ in range(4)]
    p1, p2, p3, p4 = points
    result = segments_intersect(p1, p2, p3, p4)
    print(1 if result else 0)
