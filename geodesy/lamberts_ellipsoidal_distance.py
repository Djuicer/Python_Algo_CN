from math import atan, cos, radians, sin, tan

from .haversine_distance import EARTH_RADIUS, haversine_distance

AXIS_A = 6378137.0
AXIS_B = 6356752.314245
EQUATORIAL_RADIUS = 6378137


def lamberts_ellipsoidal_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    根据经纬度，计算地球表面两点沿椭球面的最短距离：
    https://en.wikipedia.org/wiki/Geographical_distance#Lambert's_formula_for_long_lines

    注意：使用 geodesy/haversine_distance.py 计算圆心角 sigma。

    将地球表示为椭球体，比使用球体能更准确地估算地表两点间的距离。椭球公式
    将地球视为扁椭球，因此会考虑南北两极处的扁平化。Lambert 公式在数千千米
    范围内可达到约 10 米的精度。其他方法能达到毫米级精度，但本方法无需增加
    太多计算量，便能较简单地计算长距离。

    参数：
        lat1, lon1: 坐标 1 的纬度和经度
        lat2, lon2: 坐标 2 的纬度和经度
    返回：
        两点间的地理距离，单位为米

    >>> lamberts_ellipsoidal_distance(100, 0, 0, 0)
    Traceback (most recent call last):
    ...
    ValueError: Latitude must be between -90 and 90 degrees

    >>> lamberts_ellipsoidal_distance(0, 0, -100, 0)
    Traceback (most recent call last):
    ...
    ValueError: Latitude must be between -90 and 90 degrees

    >>> lamberts_ellipsoidal_distance(0, 200, 0, 0)
    Traceback (most recent call last):
    ...
    ValueError: Longitude must be between -180 and 180 degrees

    >>> lamberts_ellipsoidal_distance(0, 0, 0, -200)
    Traceback (most recent call last):
    ...
    ValueError: Longitude must be between -180 and 180 degrees

    >>> from collections import namedtuple
    >>> point_2d = namedtuple("point_2d", "lat lon")
    >>> SAN_FRANCISCO = point_2d(37.774856, -122.424227)
    >>> YOSEMITE = point_2d(37.864742, -119.537521)
    >>> NEW_YORK = point_2d(40.713019, -74.012647)
    >>> VENICE = point_2d(45.443012, 12.313071)
    >>> f"{lamberts_ellipsoidal_distance(*SAN_FRANCISCO, *YOSEMITE):0,.0f} meters"
    '254,032 meters'
    >>> f"{lamberts_ellipsoidal_distance(*SAN_FRANCISCO, *NEW_YORK):0,.0f} meters"
    '4,133,295 meters'
    >>> f"{lamberts_ellipsoidal_distance(*SAN_FRANCISCO, *VENICE):0,.0f} meters"
    '9,719,525 meters'
    """

    # 验证纬度值
    if not -90 <= lat1 <= 90 or not -90 <= lat2 <= 90:
        raise ValueError("Latitude must be between -90 and 90 degrees")

    # 验证经度值
    if not -180 <= lon1 <= 180 or not -180 <= lon2 <= 180:
        raise ValueError("Longitude must be between -180 and 180 degrees")

    # WGS84 常量：https://en.wikipedia.org/wiki/World_Geodetic_System
    # 距离单位为米（m）
    # 方程参数
    # https://en.wikipedia.org/wiki/Geographical_distance#Lambert's_formula_for_long_lines
    flattening = (AXIS_A - AXIS_B) / AXIS_A
    # 参数纬度
    # https://en.wikipedia.org/wiki/Latitude#Parametric_(or_reduced)_latitude
    b_lat1 = atan((1 - flattening) * tan(radians(lat1)))
    b_lat2 = atan((1 - flattening) * tan(radians(lat2)))

    # 使用 Haversine theta 计算两点间的圆心角
    # sigma =  haversine_distance / equatorial radius
    sigma = haversine_distance(lat1, lon1, lat2, lon2) / EARTH_RADIUS

    # 中间值 P 和 Q
    p_value = (b_lat1 + b_lat2) / 2
    q_value = (b_lat2 - b_lat1) / 2

    # 中间值 X
    # X = (sigma - sin(sigma)) * sin^2Pcos^2Q / cos^2(sigma/2)
    x_numerator = (sin(p_value) ** 2) * (cos(q_value) ** 2)
    x_denominator = cos(sigma / 2) ** 2
    x_value = (sigma - sin(sigma)) * (x_numerator / x_denominator)

    # 中间值 Y
    # Y = (sigma + sin(sigma)) * cos^2Psin^2Q / sin^2(sigma/2)
    y_numerator = (cos(p_value) ** 2) * (sin(q_value) ** 2)
    y_denominator = sin(sigma / 2) ** 2
    y_value = (sigma + sin(sigma)) * (y_numerator / y_denominator)

    return EQUATORIAL_RADIUS * (sigma - ((flattening / 2) * (x_value + y_value)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
