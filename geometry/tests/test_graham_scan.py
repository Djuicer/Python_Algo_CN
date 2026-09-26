"""
Graham 扫描凸包算法的测试。
"""

from geometry.graham_scan import Point, graham_scan


def test_empty_points() -> None:
    """测试没有点的情况。"""
    assert graham_scan([]) == []


def test_single_point() -> None:
    """测试单个点的情况。"""
    assert graham_scan([Point(0, 0)]) == []


def test_two_points() -> None:
    """测试两个点的情况。"""
    assert graham_scan([Point(0, 0), Point(1, 1)]) == []


def test_duplicate_points() -> None:
    """测试所有点均重复的情况。"""
    p = Point(0, 0)
    points = [p, Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)]
    assert graham_scan(points) == []


def test_collinear_points() -> None:
    """测试所有点均位于同一直线上的情况。"""
    points = [
        Point(1, 0),
        Point(2, 0),
        Point(3, 0),
        Point(4, 0),
        Point(5, 0),
    ]
    assert graham_scan(points) == []


def test_triangle() -> None:
    """测试三角形（3 个点）。"""
    p1 = Point(1, 1)
    p2 = Point(2, 1)
    p3 = Point(1.5, 2)
    points = [p1, p2, p3]
    hull = graham_scan(points)

    assert len(hull) == 3
    assert p1 in hull
    assert p2 in hull
    assert p3 in hull


def test_rectangle() -> None:
    """测试矩形（4 个点）。"""
    p1 = Point(1, 1)
    p2 = Point(2, 1)
    p3 = Point(2, 2)
    p4 = Point(1, 2)
    points = [p1, p2, p3, p4]
    hull = graham_scan(points)

    assert len(hull) == 4
    assert all(p in hull for p in points)


def test_triangle_with_interior_points() -> None:
    """测试包含内部点的三角形。"""
    p1 = Point(1, 1)
    p2 = Point(2, 1)
    p3 = Point(1.5, 2)
    p4 = Point(1.5, 1.5)  # 内部点
    p5 = Point(1.2, 1.3)  # 内部点
    p6 = Point(1.8, 1.2)  # 内部点
    p7 = Point(1.5, 1.9)  # 内部点

    hull_points = [p1, p2, p3]
    interior_points = [p4, p5, p6, p7]
    all_points = hull_points + interior_points

    hull = graham_scan(all_points)

    # 所有凸包点都应在结果中
    for p in hull_points:
        assert p in hull

    # 结果中不应包含内部点
    for p in interior_points:
        assert p not in hull


def test_rectangle_with_interior_points() -> None:
    """测试包含内部点的矩形。"""
    p1 = Point(1, 1)
    p2 = Point(2, 1)
    p3 = Point(2, 2)
    p4 = Point(1, 2)
    p5 = Point(1.5, 1.5)  # 内部点
    p6 = Point(1.2, 1.3)  # 内部点
    p7 = Point(1.8, 1.2)  # 内部点
    p8 = Point(1.9, 1.7)  # 内部点
    p9 = Point(1.4, 1.9)  # 内部点

    hull_points = [p1, p2, p3, p4]
    interior_points = [p5, p6, p7, p8, p9]
    all_points = hull_points + interior_points

    hull = graham_scan(all_points)

    # 所有凸包点都应在结果中
    for p in hull_points:
        assert p in hull

    # 结果中不应包含内部点
    for p in interior_points:
        assert p not in hull


def test_star_shape() -> None:
    """测试仅尖端点位于凸包上的星形。"""
    # 星形的尖端点（位于凸包上）
    p1 = Point(-5, 6)
    p2 = Point(-11, 0)
    p3 = Point(-9, -8)
    p4 = Point(4, 4)
    p5 = Point(6, -7)

    # 内部点（不在凸包上）
    p6 = Point(-7, -2)
    p7 = Point(-2, -4)
    p8 = Point(0, 1)
    p9 = Point(1, 0)
    p10 = Point(-6, 1)

    hull_points = [p1, p2, p3, p4, p5]
    interior_points = [p6, p7, p8, p9, p10]
    all_points = hull_points + interior_points

    hull = graham_scan(all_points)

    # 所有凸包点都应在结果中
    for p in hull_points:
        assert p in hull

    # 结果中不应包含内部点
    for p in interior_points:
        assert p not in hull


def test_rectangle_with_collinear_points() -> None:
    """测试边上含点（与顶点共线）的矩形。"""
    p1 = Point(1, 1)
    p2 = Point(2, 1)
    p3 = Point(2, 2)
    p4 = Point(1, 2)
    p5 = Point(1.5, 1)  # 位于边 p1-p2 上
    p6 = Point(1, 1.5)  # 位于边 p1-p4 上
    p7 = Point(2, 1.5)  # 位于边 p2-p3 上
    p8 = Point(1.5, 2)  # 位于边 p3-p4 上

    hull_points = [p1, p2, p3, p4]
    edge_points = [p5, p6, p7, p8]
    all_points = hull_points + edge_points

    hull = graham_scan(all_points)

    # 所有角点都应在结果中
    for p in hull_points:
        assert p in hull

    # 边上的点不应在结果中（只保留角点）
    for p in edge_points:
        assert p not in hull


def test_point_equality() -> None:
    """测试 Point 相等性。"""
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(2, 1)

    assert p1 == p2
    assert p1 != p3


def test_point_comparison() -> None:
    """测试用于排序的 Point 比较。"""
    p1 = Point(1, 2)
    p2 = Point(1, 3)
    p3 = Point(2, 2)

    assert p1 < p2  # y 值更小
    assert p1 < p3  # y 值相同，x 值更小
    assert not p2 < p1


def test_euclidean_distance() -> None:
    """测试欧几里得距离计算。"""
    p1 = Point(0, 0)
    p2 = Point(3, 4)

    assert p1.euclidean_distance(p2) == 5.0


def test_consecutive_orientation() -> None:
    """测试方向计算。"""
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    p3_ccw = Point(1, 1)  # 逆时针
    p3_cw = Point(1, -1)  # 顺时针
    p3_collinear = Point(2, 0)  # 共线

    assert p1.consecutive_orientation(p2, p3_ccw) > 0  # 逆时针
    assert p1.consecutive_orientation(p2, p3_cw) < 0  # 顺时针
    assert p1.consecutive_orientation(p2, p3_collinear) == 0  # 共线


def test_large_hull() -> None:
    """测试较大的点集。"""
    # 创建圆周上的点集
    import math

    points = []
    for i in range(20):
        angle = 2 * math.pi * i / 20
        x = math.cos(angle)
        y = math.sin(angle)
        points.append(Point(x, y))

    # 添加一些内部点
    points.append(Point(0, 0))
    points.append(Point(0.5, 0.5))
    points.append(Point(-0.3, 0.2))

    hull = graham_scan(points)

    # 凸包应包含圆周点，但不包含内部点
    assert len(hull) >= 3
    assert Point(0, 0) not in hull
    assert Point(0.5, 0.5) not in hull
    assert Point(-0.3, 0.2) not in hull


def test_random_order() -> None:
    """测试点的顺序不影响结果。"""
    p1 = Point(0, 0)
    p2 = Point(4, 0)
    p3 = Point(4, 3)
    p4 = Point(0, 3)
    p5 = Point(2, 1.5)  # 内部点

    # 尝试不同的排列顺序
    order1 = [p1, p2, p3, p4, p5]
    order2 = [p5, p4, p3, p2, p1]
    order3 = [p3, p5, p1, p4, p2]

    hull1 = graham_scan(order1)
    hull2 = graham_scan(order2)
    hull3 = graham_scan(order3)

    # 各结果应包含相同的点（顺序可能不同）
    assert len(hull1) == len(hull2) == len(hull3) == 4
    assert {(p.x, p.y) for p in hull1} == {(p.x, p.y) for p in hull2}
    assert {(p.x, p.y) for p in hull2} == {(p.x, p.y) for p in hull3}
