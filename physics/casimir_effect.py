"""
标题：给定三个参数中的另外两个，求卡西米尔力的大小、其中一块板的表面积或
两板间距。

说明：在量子场论中，卡西米尔效应是由场的量子涨落产生、作用于受限空间
宏观边界的物理力。这种分离物体之间的力既非由电荷、引力或粒子交换产生，
而是由物体间空间中无处不在的能量场共振产生。力的强度随距离迅速衰减，
因此仅在物体间距极小时可测。在亚微米尺度上，该力会强到成为无电荷导体间
的主导作用力。

荷兰物理学家 Hendrik B. G. Casimir 首次提出这种力的存在，并于 1948 年在
Philips Research Labs 参与研究时设计实验进行探测。经典实验在真空中使用
一对不带电的平行金属板，测得结果与其理论预测值的偏差在 15% 以内。

在真空中，相距 a 米、表面积为 A 平方米的理想完全导电板之间的卡西米尔力
F 表示为：

F = - ((Reduced Planck Constant ℏ) * c * Pi^2 * A) / (240 * a^4)

负号表示该力具有吸引性质。为便于计算，此处仅考虑力的大小。

来源：
- https://en.wikipedia.org/wiki/Casimir_effect
- https://www.cs.mcgill.ca/~rwest/wikispeedia/wpcd/wp/c/Casimir_effect.htm
- Casimir, H. B. ; Polder, D. (1948) "The Influence of Retardation on the
  London-van der Waals Forces", Physical Review, vol. 73, Issue 4, pp. 360-372
"""

from __future__ import annotations

from math import pi

# 定义约化普朗克常数 ℏ（H bar）、光速 C、Pi 的值及函数
REDUCED_PLANCK_CONSTANT = 1.054571817e-34  # ℏ 的单位：J * s

SPEED_OF_LIGHT = 3e8  # c 的单位：m * s^-1


def casimir_force(force: float, area: float, distance: float) -> dict[str, float]:
    """
    输入参数
    ----------------
    force -> 卡西米尔力：大小，单位为牛顿

    area -> 每块板的表面积：单位为平方米

    distance -> 两块板之间的距离：单位为米

    返回
    -------
    result : 字典，名称和值对应输入中值为零的参数

    给定其他参数时，返回指定为 0 的那个参数的值。
    >>> casimir_force(force = 0, area = 4, distance = 0.03)
    {'force': 6.4248189174864216e-21}

    >>> casimir_force(force = 2635e-13, area = 0.0023, distance = 0)
    {'distance': 1.0323056015031114e-05}

    >>> casimir_force(force = 2737e-21, area = 0, distance = 0.0023746)
    {'area': 0.06688838837354052}

    >>> casimir_force(force = 3457e-12, area = 0, distance = 0)
    Traceback (most recent call last):
        ...
    ValueError: One and only one argument must be 0

    >>> casimir_force(force = 3457e-12, area = 0, distance = -0.00344)
    Traceback (most recent call last):
        ...
    ValueError: Distance can not be negative

    >>> casimir_force(force = -912e-12, area = 0, distance = 0.09374)
    Traceback (most recent call last):
        ...
    ValueError: Magnitude of force can not be negative
    """

    if (force, area, distance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if force < 0:
        raise ValueError("Magnitude of force can not be negative")
    if distance < 0:
        raise ValueError("Distance can not be negative")
    if area < 0:
        raise ValueError("Area can not be negative")
    if force == 0:
        force = (REDUCED_PLANCK_CONSTANT * SPEED_OF_LIGHT * pi**2 * area) / (
            240 * (distance) ** 4
        )
        return {"force": force}
    elif area == 0:
        area = (240 * force * (distance) ** 4) / (
            REDUCED_PLANCK_CONSTANT * SPEED_OF_LIGHT * pi**2
        )
        return {"area": area}
    elif distance == 0:
        distance = (
            (REDUCED_PLANCK_CONSTANT * SPEED_OF_LIGHT * pi**2 * area) / (240 * force)
        ) ** (1 / 4)
        return {"distance": distance}
    raise ValueError("One and only one argument must be 0")


# 运行 doctest
if __name__ == "__main__":
    import doctest

    doctest.testmod()
