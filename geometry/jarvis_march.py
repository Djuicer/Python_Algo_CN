"""
用于求点集凸包的 Jarvis 步进法（Jarvis March，又称 Gift Wrapping）。

凸包是包含所有点的最小凸多边形。

时间复杂度：O(n*h)，其中 n 为点的数量，h 为凸包上的点数。
空间复杂度：O(h)，其中 h 为凸包上的点数。

用法：
    -> 将此文件导入项目。
    -> 使用 jarvis_march() 函数求点集的凸包。
    -> 参数：
        -> points：表示二维坐标的 Point 对象列表

参考资料：
    -> 维基百科参考资料：https://en.wikipedia.org/wiki/Gift_wrapping_algorithm
    -> GeeksforGeeks 参考资料：
       https://www.geeksforgeeks.org/convex-hull-set-1-jarviss-algorithm-or-wrapping/
"""

from __future__ import annotations


class Point:
    """表示具有 x、y 坐标的二维点。"""

    def __init__(self, x_coordinate: float, y_coordinate: float) -> None:
        self.x = x_coordinate
        self.y = y_coordinate

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def _cross_product(origin: Point, point_a: Point, point_b: Point) -> float:
    """
    计算向量 OA 与 OB 的叉积。

    返回：
        > 0：逆时针转向（左转）
        = 0：共线
        < 0：顺时针转向（右转）
    """
    return (point_a.x - origin.x) * (point_b.y - origin.y) - (point_a.y - origin.y) * (
        point_b.x - origin.x
    )


def _is_point_on_segment(p1: Point, p2: Point, point: Point) -> bool:
    """检查点是否位于 p1 与 p2 之间的线段上。"""
    # 检查点是否与线段端点共线
    cross = (point.y - p1.y) * (p2.x - p1.x) - (point.x - p1.x) * (p2.y - p1.y)

    if abs(cross) > 1e-9:
        return False

    # 检查点是否位于线段的包围盒内
    return min(p1.x, p2.x) <= point.x <= max(p1.x, p2.x) and min(
        p1.y, p2.y
    ) <= point.y <= max(p1.y, p2.y)


def _find_leftmost_point(points: list[Point]) -> int:
    """查找最左侧点的索引（若并列则取最下方）。"""
    left_idx = 0
    for i in range(1, len(points)):
        if points[i].x < points[left_idx].x or (
            points[i].x == points[left_idx].x and points[i].y < points[left_idx].y
        ):
            left_idx = i
    return left_idx


def _find_next_hull_point(points: list[Point], current_idx: int) -> int:
    """查找凸包上的下一个点。"""
    next_idx = (current_idx + 1) % len(points)
    # 确保 next_idx 与 current_idx 不同
    while next_idx == current_idx:
        next_idx = (next_idx + 1) % len(points)

    for i in range(len(points)):
        if i == current_idx:
            continue
        cross = _cross_product(points[current_idx], points[i], points[next_idx])
        if cross > 0:
            next_idx = i

    return next_idx


def _is_valid_polygon(hull: list[Point]) -> bool:
    """检查凸包是否构成有效多边形（至少有一次非共线转向）。"""
    for i in range(len(hull)):
        p1 = hull[i]
        p2 = hull[(i + 1) % len(hull)]
        p3 = hull[(i + 2) % len(hull)]
        if abs(_cross_product(p1, p2, p3)) > 1e-9:
            return True
    return False


def _add_point_to_hull(hull: list[Point], point: Point) -> None:
    """向凸包添加一个点，并移除共线的中间点。"""
    last = len(hull) - 1
    if len(hull) > 1 and _is_point_on_segment(hull[last - 1], hull[last], point):
        hull[last] = Point(point.x, point.y)
    else:
        hull.append(Point(point.x, point.y))


def jarvis_march(points: list[Point]) -> list[Point]:
    """
    使用 Jarvis 步进法求点集的凸包。

    算法从最左侧的点开始包围点集，每一步选择最偏逆时针方向的点。

    参数：
        points：表示二维坐标的 Point 对象列表

    返回：
        按逆时针顺序构成凸包的 Point 列表。
        若非共线点少于 3 个，则返回空列表。
    """
    if len(points) <= 2:
        return []

    # 移除重复点以避免无限循环
    unique_points = list(set(points))

    if len(unique_points) <= 2:
        return []

    convex_hull: list[Point] = []

    # 查找最左侧的点
    left_point_idx = _find_leftmost_point(unique_points)
    convex_hull.append(
        Point(unique_points[left_point_idx].x, unique_points[left_point_idx].y)
    )

    current_idx = left_point_idx
    while True:
        # 查找下一个逆时针方向的点
        next_idx = _find_next_hull_point(unique_points, current_idx)

        if next_idx == left_point_idx:
            break

        if next_idx == current_idx:
            break

        current_idx = next_idx
        _add_point_to_hull(convex_hull, unique_points[current_idx])

    # 检查退化情况
    if len(convex_hull) <= 2:
        return []

    # 检查最后一点是否与第一点和倒数第二点共线
    last = len(convex_hull) - 1
    if _is_point_on_segment(convex_hull[last - 1], convex_hull[last], convex_hull[0]):
        convex_hull.pop()
        if len(convex_hull) == 2:
            return []

    # 验证凸包是否构成有效多边形
    if not _is_valid_polygon(convex_hull):
        return []

    return convex_hull


if __name__ == "__main__":
    # 使用示例
    points = [Point(0, 0), Point(1, 1), Point(0, 1), Point(1, 0), Point(0.5, 0.5)]
    hull = jarvis_march(points)
    print(f"Convex hull: {hull}")
