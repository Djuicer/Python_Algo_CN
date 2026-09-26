from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS = 6371000


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    根据经纬度计算球面上两点间的大圆距离（Great-circle Distance）：
    https://en.wikipedia.org/wiki/Haversine_formula

    地球近似为球体，因此两点之间的路径并非严格的直线。计算 A 点到 B 点的
    距离时，需要考虑地球曲率。短距离下这一影响可以忽略，但会随距离增加而
    累积。Haversine 方法将地球视为球体，从而把 A、B 两点“投影”到球面上，
    近似计算两点间的球面距离。由于地球并非完美球体，对地球椭球特性建模的
    其他方法更加准确；但对于较短距离，Haversine 这种快速且易调整的计算方法
    十分实用。

    参数：
        lat1: 坐标 1 的纬度，单位为度
        lon1: 坐标 1 的经度，单位为度
        lat2: 坐标 2 的纬度，单位为度
        lon2: 坐标 2 的经度，单位为度
    返回：
        两点间的地理距离，单位为米

    >>> from collections import namedtuple
    >>> point_2d = namedtuple("point_2d", "lat lon")
    >>> SAN_FRANCISCO = point_2d(37.774856, -122.424227)
    >>> YOSEMITE = point_2d(37.864742, -119.537521)
    >>> f"{haversine_distance(*SAN_FRANCISCO, *YOSEMITE):0,.0f} meters"
    '253,748 meters'
    >>> NEW_YORK = point_2d(40.712776, -74.005974)
    >>> LOS_ANGELES = point_2d(34.052235, -118.243683)
    >>> f"{haversine_distance(*NEW_YORK, *LOS_ANGELES):0,.0f} meters"
    '3,935,746 meters'
    >>> LONDON = point_2d(51.507351, -0.127758)
    >>> PARIS = point_2d(48.856614, 2.352222)
    >>> f"{haversine_distance(*LONDON, *PARIS):0,.0f} meters"
    '343,549 meters'
    >>> haversine_distance(0, 0, 0, 0)
    0.0
    >>> from math import isclose
    >>> quarter_equator = haversine_distance(0, 0, 0, 90)
    >>> isclose(quarter_equator, 10_007_543, rel_tol=1e-3)
    True
    """
    # 将大地坐标从度转换为弧度
    # Haversine 公式在球面上运算，因此直接使用原始大地纬度，而不使用
    # 适用于 Lambert 公式等椭球模型的归化纬度
    # 参考资料：https://en.wikipedia.org/wiki/Haversine_formula#Formulation
    phi_1 = radians(lat1)
    phi_2 = radians(lat2)
    lambda_1 = radians(lon1)
    lambda_2 = radians(lon2)

    # Haversine 方程
    sin_sq_phi = sin((phi_2 - phi_1) / 2)
    sin_sq_lambda = sin((lambda_2 - lambda_1) / 2)
    sin_sq_phi *= sin_sq_phi
    sin_sq_lambda *= sin_sq_lambda
    h_value = sqrt(sin_sq_phi + (cos(phi_1) * cos(phi_2) * sin_sq_lambda))
    return 2 * EARTH_RADIUS * asin(h_value)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
