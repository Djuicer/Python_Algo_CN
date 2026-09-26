"""
Ramer-Douglas-Peucker 折线简化算法。

给定二维点序列和容差 epsilon，该算法在保留曲线整体形状的同时减少点的数量。

时间复杂度：平均 O(n log n)，最坏 O(n²)
空间复杂度：O(n)

参考资料：
    https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
"""

from __future__ import annotations

import math


def _euclidean_distance(
    point_a: tuple[float, float],
    point_b: tuple[float, float],
) -> float:
    """返回两个二维点之间的欧几里得距离。

    >>> _euclidean_distance((0.0, 0.0), (3.0, 4.0))
    5.0
    >>> _euclidean_distance((1.0, 1.0), (1.0, 1.0))
    0.0
    """
    return math.hypot(point_b[0] - point_a[0], point_b[1] - point_a[1])


def _perpendicular_distance(
    point: tuple[float, float],
    line_start: tuple[float, float],
    line_end: tuple[float, float],
) -> float:
    """返回 *point* 到 *line_start* 与 *line_end* 之间线段的距离。

    当 *point* 在无限直线上的垂直投影落在线段内时，此值等于点到该直线的垂直距离。
    当投影落在线段外时，改为返回到最近端点的距离（将投影参数限制在 [0, 1]）。

    这是 Ramer-Douglas-Peucker 算法所需的正确距离度量；使用到无限直线的距离，
    可能会错误地舍弃投影位于线段端点之外的点。

    >>> _perpendicular_distance((4.0, 0.0), (0.0, 0.0), (0.0, 3.0))
    4.0
    >>> # order of line_start and line_end does not affect the result
    >>> _perpendicular_distance((4.0, 0.0), (0.0, 3.0), (0.0, 0.0))
    4.0
    >>> _perpendicular_distance((4.0, 1.0), (0.0, 1.0), (0.0, 4.0))
    4.0
    >>> _perpendicular_distance((2.0, 1.0), (-2.0, 1.0), (-2.0, 4.0))
    4.0
    >>> # projection falls outside the segment; distance to nearest endpoint
    >>> round(_perpendicular_distance((0.0, 2.0), (1.0, 0.0), (3.0, 0.0)), 6)
    2.236068
    """
    px, py = point
    ax, ay = line_start
    bx, by = line_end
    dx, dy = bx - ax, by - ay
    seg_len_sq = dx * dx + dy * dy
    if seg_len_sq == 0.0:
    # line_start 与 line_end 重合；改用点到点距离
        return _euclidean_distance(point, line_start)
    # 将点投影到线段所在直线，再把 t 限制在 [0, 1]，确保最近点始终在线段上，
    # 而不是仅位于无限延伸的直线上。
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / seg_len_sq))
    nearest_x = ax + t * dx
    nearest_y = ay + t * dy
    return math.hypot(px - nearest_x, py - nearest_y)


def ramer_douglas_peucker(
    pts: list[tuple[float, float]],
    epsilon: float,
) -> list[tuple[float, float]]:
    """使用 Ramer-Douglas-Peucker 算法简化折线。

    给定二维点序列和最大允许偏差 *epsilon* (>= 0)，返回简化后的点列表，
    使任何被舍弃点到简化折线的距离都不超过 *epsilon*。

    参数
    ----------
    pts:
        描述折线的有序 ``(x, y)`` 点序列。
    epsilon:
        任意被舍弃点到简化折线的最大允许距离，必须为非负数。

    返回
    -------
    list[tuple[float, float]]
        简化后的 ``(x, y)`` 点列表。始终保留 *pts* 的首尾两点。

    异常
    ------
    ValueError
        当 *epsilon* 为负数时。

    参考资料
    ----------
    https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm

    示例
    --------
    >>> ramer_douglas_peucker([], epsilon=1.0)
    []
    >>> ramer_douglas_peucker([(0.0, 0.0)], epsilon=1.0)
    [(0.0, 0.0)]
    >>> ramer_douglas_peucker([(0.0, 0.0), (1.0, 0.0)], epsilon=1.0)
    [(0.0, 0.0), (1.0, 0.0)]
    >>> # middle point is within epsilon - it is discarded
    >>> ramer_douglas_peucker([(0.0, 0.0), (1.0, 0.1), (2.0, 0.0)], epsilon=0.5)
    [(0.0, 0.0), (2.0, 0.0)]
    >>> # middle point exceeds epsilon - it is kept
    >>> ramer_douglas_peucker([(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], epsilon=0.5)
    [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)]
    >>> ramer_douglas_peucker([(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)], epsilon=-1.0)
    Traceback (most recent call last):
        ...
    ValueError: epsilon must be non-negative, got -1.0
    """
    if epsilon < 0:
        msg = f"epsilon must be non-negative, got {epsilon!r}"
        raise ValueError(msg)

    if len(pts) < 3:
        return list(pts)

    # ---------------------------------------------------------------------------
    # 基于栈的迭代实现。
    #
    # 朴素递归方法会在每层通过切片（pts[:max_index+1] / pts[max_index:]）复制子列表，
    # 每次调用需要 O(n) 空间，即使划分均衡，总体内存复杂度也会达到 O(n²)。
    # 使用显式栈操作索引区间可避免所有复制，并消除长折线触及 Python 递归限制的风险。
    # ---------------------------------------------------------------------------
    n = len(pts)

    # 当 pts[i] 必须出现在输出中时，keep[i] 为 True。
    keep: list[bool] = [False] * n
    keep[0] = True
    keep[-1] = True

    # 存放待检查 (start_index, end_index) 索引对的栈。
    stack: list[tuple[int, int]] = [(0, n - 1)]

    while stack:
        start, end = stack.pop()
        if end - start < 2:
        # 内部候选点至多一个，无需继续拆分。
            continue

        # 查找距线段最远的内部点。
        max_dist = 0.0
        max_index = start
        for i in range(start + 1, end):
            dist = _perpendicular_distance(pts[i], pts[start], pts[end])
            if dist > max_dist:
                max_dist = dist
                max_index = i

        if max_dist > epsilon:
            keep[max_index] = True
            stack.append((start, max_index))
            stack.append((max_index, end))
        # 否则所有内部点均在 epsilon 范围内，将其全部舍弃。

    return [pts[i] for i in range(n) if keep[i]]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
