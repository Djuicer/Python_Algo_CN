"""
本模块提供大地坐标与地心地固（Earth-Centered, Earth-Fixed，ECEF）笛卡尔坐标
之间的转换函数，并可根据雷达测量值计算目标坐标。

参考资料：
- https://en.wikipedia.org/wiki/Geographic_coordinate_conversion
- https://en.wikipedia.org/wiki/Local_tangent_plane_coordinates
"""

import math

# WGS84 椭球常量
WGS84_A = 6378137.0  # 长半轴，单位为米
WGS84_B = 6356752.314245  # 短半轴，单位为米
WGS84_E_SQ = 1.0 - (WGS84_B**2 / WGS84_A**2)  # 第一偏心率的平方
WGS84_EP_SQ = (WGS84_A**2 - WGS84_B**2) / WGS84_B**2  # 第二偏心率的平方


def geodetic_to_ecef(
    lat_deg: float, lon_deg: float, alt_m: float
) -> tuple[float, float, float]:
    """
    将大地坐标（纬度、经度、高度）转换为地心地固（ECEF）笛卡尔坐标。

    >>> x, y, z = geodetic_to_ecef(0.0, 0.0, 0.0)
    >>> round(x, 2), round(y, 2), round(z, 2)
    (6378137.0, 0.0, 0.0)
    >>> x, y, z = geodetic_to_ecef(90.0, 0.0, 0.0)
    >>> round(x, 2), round(y, 2), round(z, 2)
    (0.0, 0.0, 6356752.31)
    """
    lat_rad = math.radians(lat_deg)
    lon_rad = math.radians(lon_deg)

    sin_lat = math.sin(lat_rad)
    cos_lat = math.cos(lat_rad)

    # N 为卯酉圈曲率半径
    n_radius = WGS84_A / math.sqrt(1.0 - WGS84_E_SQ * sin_lat**2)

    # 计算 ECEF 的 X、Y、Z
    x = (n_radius + alt_m) * cos_lat * math.cos(lon_rad)
    y = (n_radius + alt_m) * cos_lat * math.sin(lon_rad)
    z = (n_radius * (1.0 - WGS84_E_SQ) + alt_m) * sin_lat

    return x, y, z


def ecef_to_geodetic(
    x_ecef: float, y_ecef: float, z_ecef: float
) -> tuple[float, float, float]:
    """
    使用 Bowring 方法将地心地固（ECEF）坐标转换为大地坐标（纬度、经度、高度）。

    >>> lat, lon, alt = ecef_to_geodetic(6378137.0, 0.0, 0.0)
    >>> round(lat, 2), round(lon, 2), round(alt, 2)
    (0.0, 0.0, 0.0)
    >>> lat, lon, alt = ecef_to_geodetic(0.0, 0.0, 6356752.314245)
    >>> round(lat, 2), round(lon, 2), round(alt, 2)
    (90.0, 0.0, 0.0)
    """
    p = math.sqrt(x_ecef**2 + y_ecef**2)

    # 处理点恰好位于两极的特殊情况
    if p == 0:
        lon_deg = 0.0
        lat_deg = 90.0 if z_ecef > 0 else -90.0
        alt_m = abs(z_ecef) - WGS84_B
        return lat_deg, lon_deg, alt_m

    theta = math.atan2(z_ecef * WGS84_A, p * WGS84_B)

    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)

    # 计算精确的纬度和经度
    lon_rad = math.atan2(y_ecef, x_ecef)
    lat_rad = math.atan2(
        z_ecef + WGS84_EP_SQ * WGS84_B * sin_theta**3,
        p - WGS84_E_SQ * WGS84_A * cos_theta**3,
    )

    sin_lat = math.sin(lat_rad)

    # 重新计算卯酉圈曲率半径以求高度
    n_radius = WGS84_A / math.sqrt(1.0 - WGS84_E_SQ * sin_lat**2)

    alt_m = (p / math.cos(lat_rad)) - n_radius

    return math.degrees(lat_rad), math.degrees(lon_rad), alt_m


def enu_to_ecef(
    east: float, north: float, up: float, ref_lat_deg: float, ref_lon_deg: float
) -> tuple[float, float, float]:
    """
    根据参考点（雷达）的纬度和经度，将东-北-天（ENU）偏移坐标旋转为 ECEF
    偏移坐标。

    >>> dx, dy, dz = enu_to_ecef(100.0, 200.0, 50.0, 0.0, 0.0)
    >>> round(dx, 2), round(dy, 2), round(dz, 2)
    (50.0, 100.0, 200.0)
    """
    lat_rad = math.radians(ref_lat_deg)
    lon_rad = math.radians(ref_lon_deg)

    sin_lat = math.sin(lat_rad)
    cos_lat = math.cos(lat_rad)
    sin_lon = math.sin(lon_rad)
    cos_lon = math.cos(lon_rad)

    # 从 ENU 转换到 ECEF 的旋转矩阵分量
    dx = -sin_lon * east - sin_lat * cos_lon * north + cos_lat * cos_lon * up
    dy = cos_lon * east - sin_lat * sin_lon * north + cos_lat * sin_lon * up
    dz = cos_lat * north + sin_lat * up

    return dx, dy, dz


def calculate_target_coordinates(
    radar_lat: float,
    radar_lon: float,
    radar_alt: float,
    azimuth_deg: float,
    range_m: float,
    elevation_deg: float = 0.0,
) -> tuple[float, float, float]:
    """
    根据雷达测量值计算目标（船舶）坐标的主函数。

    参数：
    radar_lat (float): 雷达纬度，单位为度
    radar_lon (float): 雷达经度，单位为度
    radar_alt (float): 雷达海拔高度，单位为米
    azimuth_deg (float): 目标的真方位角（0 表示北，90 表示东）
    range_m (float): 到目标的直视距离，单位为米
    elevation_deg (float): 天线仰角，单位为度（水面船舶默认为 0）

    返回：
    tuple:（目标纬度、目标经度、目标高度）

    >>> lat, lon, alt = calculate_target_coordinates(0.0, 0.0, 0.0, 90.0, 111319.5)
    >>> round(lat, 1), round(lon, 1), round(alt, 1)
    (0.0, 1.0, 971.4)
    """
    # 第 1 步：将雷达极坐标测量值转换为局部 ENU 笛卡尔坐标
    az_rad = math.radians(azimuth_deg)
    el_rad = math.radians(elevation_deg)

    # ENU 的标准球坐标到笛卡尔坐标转换
    # 北向对应方位角 0 度，东向对应 90 度
    east = range_m * math.cos(el_rad) * math.sin(az_rad)
    north = range_m * math.cos(el_rad) * math.cos(az_rad)
    up = range_m * math.sin(el_rad)

    # 第 2 步：获取雷达的绝对 ECEF 位置
    radar_x, radar_y, radar_z = geodetic_to_ecef(radar_lat, radar_lon, radar_alt)

    # 第 3 步：将局部 ENU 偏移量转换为 ECEF 偏移量
    dx, dy, dz = enu_to_ecef(east, north, up, radar_lat, radar_lon)

    # 第 4 步：将偏移量加入雷达的 ECEF 坐标，求目标 ECEF 坐标
    target_x = radar_x + dx
    target_y = radar_y + dy
    target_z = radar_z + dz

    # 第 5 步：将目标 ECEF 坐标转换回大地坐标
    target_lat, target_lon, target_alt = ecef_to_geodetic(target_x, target_y, target_z)

    return target_lat, target_lon, target_alt


if __name__ == "__main__":
    import doctest

    doctest.testmod()
