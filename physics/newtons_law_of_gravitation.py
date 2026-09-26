"""
标题：给定其他三个参数时，求引力、其中一个质量或距离。

说明：牛顿万有引力定律解释了相距一定距离、具有确定质量的物体间为何存在
吸引力。通常表述为：宇宙中每个粒子都吸引其他粒子，该力与两者质量的乘积
成正比，与两者质心距离的平方成反比。这一理论的发表被称为“第一次大统一”，
因为它统一了地球上的引力现象与已知天文行为。

万有引力方程如下：
F = (G * mass_1 * mass_2) / (distance)^2

来源：
- https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation
- Newton (1687) "Philosophiæ Naturalis Principia Mathematica"
"""

from __future__ import annotations

# 定义引力常数 G 和函数
GRAVITATIONAL_CONSTANT = 6.6743e-11  # G 的单位：m^3 * kg^-1 * s^-2


def gravitational_law(
    force: float, mass_1: float, mass_2: float, distance: float
) -> dict[str, float]:
    """
    输入参数
    ----------------
    force : 大小，单位为牛顿

    mass_1 : 质量，单位为千克

    mass_2 : 质量，单位为千克

    distance : 距离，单位为米

    返回
    -------
    result : 字典，名称和值对应输入中值为零的参数

    给定其他参数时，返回指定为 0 的那个参数的值。
    >>> gravitational_law(force=0, mass_1=5, mass_2=10, distance=20)
    {'force': 8.342875e-12}

    >>> gravitational_law(force=7367.382, mass_1=0, mass_2=74, distance=3048)
    {'mass_1': 1.385816317292268e+19}

    >>> gravitational_law(force=36337.283, mass_1=0, mass_2=0, distance=35584)
    Traceback (most recent call last):
        ...
    ValueError: One and only one argument must be 0

    >>> gravitational_law(force=36337.283, mass_1=-674, mass_2=0, distance=35584)
    Traceback (most recent call last):
        ...
    ValueError: Mass can not be negative

    >>> gravitational_law(force=-847938e12, mass_1=674, mass_2=0, distance=9374)
    Traceback (most recent call last):
        ...
    ValueError: Gravitational force can not be negative
    """

    product_of_mass = mass_1 * mass_2

    if (force, mass_1, mass_2, distance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if force < 0:
        raise ValueError("Gravitational force can not be negative")
    if distance < 0:
        raise ValueError("Distance can not be negative")
    if mass_1 < 0 or mass_2 < 0:
        raise ValueError("Mass can not be negative")
    if force == 0:
        force = GRAVITATIONAL_CONSTANT * product_of_mass / (distance**2)
        return {"force": force}
    elif mass_1 == 0:
        mass_1 = (force) * (distance**2) / (GRAVITATIONAL_CONSTANT * mass_2)
        return {"mass_1": mass_1}
    elif mass_2 == 0:
        mass_2 = (force) * (distance**2) / (GRAVITATIONAL_CONSTANT * mass_1)
        return {"mass_2": mass_2}
    elif distance == 0:
        distance = (GRAVITATIONAL_CONSTANT * product_of_mass / (force)) ** 0.5
        return {"distance": distance}
    raise ValueError("One and only one argument must be 0")


# 运行 doctest
if __name__ == "__main__":
    import doctest

    doctest.testmod()
