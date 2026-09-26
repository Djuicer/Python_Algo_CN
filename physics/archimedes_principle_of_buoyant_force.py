"""
计算完全或部分浸没在静止流体中的物体所受浮力。该原理由古希腊数学家
阿基米德发现。

浮力计算公式：
Fb = p * V * g

https://en.wikipedia.org/wiki/Archimedes%27_principle
"""

# 地球重力加速度常量（单位 m/s^2）
g = 9.80665  # 也可从 scipy.constants.g 获取


def archimedes_principle(
    fluid_density: float, volume: float, gravity: float = g
) -> float:
    """
    参数：
        fluid_density: 流体密度 (kg/m^3)
        volume: 物体排开流体的体积 (m^3)
        gravity: 重力加速度，默认值为地球重力加速度
    返回：
        物体所受浮力，单位为牛顿

    >>> archimedes_principle(fluid_density=500, volume=4, gravity=9.8)
    19600.0
    >>> archimedes_principle(fluid_density=997, volume=0.5, gravity=9.8)
    4885.3
    >>> archimedes_principle(fluid_density=997, volume=0.7)
    6844.061035
    >>> archimedes_principle(fluid_density=997, volume=-0.7)
    Traceback (most recent call last):
        ...
    ValueError: Impossible object volume
    >>> archimedes_principle(fluid_density=0, volume=0.7)
    Traceback (most recent call last):
        ...
    ValueError: Impossible fluid density
    >>> archimedes_principle(fluid_density=997, volume=0.7, gravity=0)
    0.0
    >>> archimedes_principle(fluid_density=997, volume=0.7, gravity=-9.8)
    Traceback (most recent call last):
        ...
    ValueError: Impossible gravity
    """

    if fluid_density <= 0:
        raise ValueError("Impossible fluid density")
    if volume <= 0:
        raise ValueError("Impossible object volume")
    if gravity < 0:
        raise ValueError("Impossible gravity")

    return fluid_density * gravity * volume


if __name__ == "__main__":
    import doctest

    doctest.testmod()
