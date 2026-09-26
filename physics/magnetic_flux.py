"""
________________________________________________________________________________________
磁通量 (Φ) 是衡量穿过闭合面积 (A) 的磁感线 (B) 数量的标量。此外，磁通量
取决于磁场与面积 A 的法线 (N) 之间的夹角。计算公式为：
 ------------------
 | Φ = B.A.cos(θ) |
 ------------------

Φ = 磁通量（韦伯 (Wb) 或特斯拉平方米 (T.m²)）
B = 磁场（特斯拉 (T)）
A = 面积（平方米 (m²)）
θ = 磁场与法线之间的夹角（度 (°)）

（说明改编自 https://en.wikipedia.org/wiki/Magnetic_flux ）
"""

from math import cos, radians


def __check_args(magnetic_field: float, area: float, angle: float) -> None:
    """
    检查参数是否有效。
    >>> __check_args(10, 10, -10)
    Traceback (most recent call last):
        ...
    ValueError: Invalid angle. Range is 0-180 degrees.
    >>> __check_args(10, -10, 10)
    Traceback (most recent call last):
        ...
    ValueError: Invalid area. Should be a positive number.
    >>> __check_args(-10, 10, 10)
    Traceback (most recent call last):
        ...
    ValueError: Invalid magnetic field. Should be a positive number.
    """

    # 确保实例有效
    if not isinstance(magnetic_field, (int, float)):
        raise TypeError("Invalid magnetic field. Should be an integer or float.")

    if not isinstance(area, (int, float)):
        raise TypeError("Invalid area. Should be an integer or float.")

    if not isinstance(angle, (int, float)):
        raise TypeError("Invalid angle. Should be an integer or float.")

    # 确保角度有效
    if angle < 0 or angle > 180:
        raise ValueError("Invalid angle. Range is 0-180 degrees.")

    # 确保磁场有效
    if magnetic_field < 0:
        raise ValueError("Invalid magnetic field. Should be a positive number.")

    # 确保面积有效
    if area < 0:
        raise ValueError("Invalid area. Should be a positive number.")


def magnetic_flux(magnetic_field: float, area: float, angle: float) -> float:
    """
    >>> magnetic_flux(50.0, 2, 0.0)
    100.0
    >>> magnetic_flux(50, 2, 60.0)
    50.0
    >>> magnetic_flux(0.5, 4.0, 90.0)
    0.0
    >>> magnetic_flux(1, 2.0, 180.0)
    -2.0
    >>> magnetic_flux(-1.0, 2.0, 30.0)
    Traceback (most recent call last):
        ...
    ValueError: Invalid magnetic field. Should be a positive number.
    >>> magnetic_flux(1.0, 'a', 30.0)
    Traceback (most recent call last):
        ...
    TypeError: Invalid area. Should be an integer or float.
    >>> magnetic_flux(1.0, -2.0, 30.0)
    Traceback (most recent call last):
        ...
    ValueError: Invalid area. Should be a positive number.
    """
    __check_args(magnetic_field, area, angle)
    rad = radians(angle)
    return round(magnetic_field * area * cos(rad), 1)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
