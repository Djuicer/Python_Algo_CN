"""
Jarvis 步进法（Jarvis March，又称 Gift Wrapping）的单元测试。
"""

from geometry.jarvis_march import Point, jarvis_march


class TestPoint:
    """Point 类的测试。"""

    def test_point_creation(self) -> None:
        """测试 Point 初始化。"""
        p = Point(1.0, 2.0)
        assert p.x == 1.0
        assert p.y == 2.0

    def test_point_equality(self) -> None:
        """测试 Point 相等性比较。"""
        p1 = Point(1.0, 2.0)
        p2 = Point(1.0, 2.0)
        p3 = Point(2.0, 1.0)
        assert p1 == p2
        assert p1 != p3

    def test_point_repr(self) -> None:
        """测试 Point 的字符串表示。"""
        p = Point(1.5, 2.5)
        assert repr(p) == "Point(1.5, 2.5)"

    def test_point_hash(self) -> None:
        """测试 Point 哈希。"""
        p1 = Point(1.0, 2.0)
        p2 = Point(1.0, 2.0)
        assert hash(p1) == hash(p2)


class TestJarvisMarch:
    """jarvis_march 函数的测试。"""

    def test_triangle(self) -> None:
        """测试三角形的凸包。"""
        p1, p2, p3 = Point(1, 1), Point(2, 1), Point(1.5, 2)
        hull = jarvis_march([p1, p2, p3])
        assert len(hull) == 3
        assert all(p in hull for p in [p1, p2, p3])

    def test_collinear_points(self) -> None:
        """测试共线点返回空凸包。"""
        points = [Point(i, 0) for i in range(5)]
        hull = jarvis_march(points)
        assert hull == []

    def test_rectangle_with_interior_point(self) -> None:
        """测试含内部点的矩形——内部点应被排除。"""
        p1, p2 = Point(1, 1), Point(2, 1)
        p3, p4 = Point(2, 2), Point(1, 2)
        p5 = Point(1.5, 1.5)
        hull = jarvis_march([p1, p2, p3, p4, p5])
        assert len(hull) == 4
        assert p5 not in hull

    def test_star_shape(self) -> None:
        """测试星形——凸包中仅包含尖端点。"""
        tips = [
            Point(-5, 6),
            Point(-11, 0),
            Point(-9, -8),
            Point(4, 4),
            Point(6, -7),
        ]
        interior = [Point(-7, -2), Point(-2, -4), Point(0, 1)]
        hull = jarvis_march(tips + interior)
        assert len(hull) == 5
        assert all(p in hull for p in tips)
        assert not any(p in hull for p in interior)

    def test_empty_list(self) -> None:
        """测试空列表返回空凸包。"""
        assert jarvis_march([]) == []

    def test_single_point(self) -> None:
        """测试单个点返回空凸包。"""
        assert jarvis_march([Point(0, 0)]) == []

    def test_two_points(self) -> None:
        """测试两个点返回空凸包。"""
        assert jarvis_march([Point(0, 0), Point(1, 1)]) == []

    def test_square(self) -> None:
        """测试正方形的凸包。"""
        p1, p2 = Point(0, 0), Point(1, 0)
        p3, p4 = Point(1, 1), Point(0, 1)
        hull = jarvis_march([p1, p2, p3, p4])
        assert len(hull) == 4
        assert all(p in hull for p in [p1, p2, p3, p4])

    def test_duplicate_points(self) -> None:
        """测试重复点的处理。"""
        p1, p2, p3 = Point(0, 0), Point(1, 0), Point(0, 1)
        points = [p1, p2, p3, p1, p2]  # 包含重复点
        hull = jarvis_march(points)
        assert len(hull) == 3

    def test_pentagon(self) -> None:
        """测试五边形的凸包。"""
        points = [
            Point(0, 1),
            Point(1, 2),
            Point(2, 1),
            Point(1.5, 0),
            Point(0.5, 0),
        ]
        hull = jarvis_march(points)
        assert len(hull) == 5
        assert all(p in hull for p in points)
