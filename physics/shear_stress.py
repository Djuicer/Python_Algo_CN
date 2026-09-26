from __future__ import annotations

"""
剪应力是与材料横截面共面的应力分量。它由剪切力产生，剪切力是平行于材料
横截面的力矢量分量。

https://en.wikipedia.org/wiki/Shear_stress
"""


def shear_stress(
    stress: float,
    tangential_force: float,
    area: float,
) -> tuple[str, float]:
    """
    本函数可以根据给出的另外两个值，计算以下三者中的任意一个：
    1. 剪应力
    2. 切向力
    3. 横截面积
    示例：
    >>> shear_stress(stress=25, tangential_force=100, area=0)
    ('area', 4.0)
    >>> shear_stress(stress=0, tangential_force=1600, area=200)
    ('stress', 8.0)
    >>> shear_stress(stress=1000, tangential_force=0, area=1200)
    ('tangential_force', 1200000)
    """
    if (stress, tangential_force, area).count(0) != 1:
        raise ValueError("You cannot supply more or less than 2 values")
    if stress < 0:
        raise ValueError("Stress cannot be negative")
    if tangential_force < 0:
        raise ValueError("Tangential Force cannot be negative")
    if area < 0:
        raise ValueError("Area cannot be negative")
    if stress == 0:
        return (
            "stress",
            tangential_force / area,
        )
    elif tangential_force == 0:
        return (
            "tangential_force",
            stress * area,
        )
    else:
        return (
            "area",
            tangential_force / stress,
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
