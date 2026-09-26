def area_of_polygon(xs: list[float], ys: list[float]) -> float:
    """
    使用鞋带公式（Shoelace Formula）计算多边形面积。多边形必须是平面简单多边形
    （不自相交），且顶点必须按逆时针方向排列。
    https://en.wikipedia.org/wiki/Shoelace_formula

    参数：
        xs：按逆时针顺序排列的多边形顶点 x 坐标列表
        ys：按逆时针顺序排列的多边形顶点 y 坐标列表
    返回：
        多边形面积

    >>> from math import isclose
    >>> xs = [1, 3, 7, 4, 8]
    >>> ys = [6, 1, 2, 4, 5]
    >>> isclose(area_of_polygon(xs, ys), 16.5)
    True
    """

    return 0.5 * sum(
        (ys[i] + ys[(i + 1) % len(ys)]) * (xs[i] - xs[(i + 1) % len(xs)])
        for i in range(len(xs))
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
