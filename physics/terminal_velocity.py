"""
标题：计算物体在流体中下落时的终端速度。

终端速度定义为物体在流体中下落时达到的最高速度。当阻力与浮力之和等于
物体所受向下的重力时，物体达到终端速度。此时合力为零，物体加速度也为零。

Vt = ((2 * m * g)/(p * A * Cd))^0.5

其中：
Vt = 终端速度 (m/s)
m = 下落物体的质量 (Kg)
g = 重力加速度（取自 scipy）
p = 物体下落所处流体的密度 (Kg/m^3)
A = 物体的投影面积 (m^2)
Cd = 阻力系数（无量纲）

参考资料：https://byjus.com/physics/derivation-of-terminal-velocity/
"""

from scipy.constants import g


def terminal_velocity(
    mass: float, density: float, area: float, drag_coefficient: float
) -> float:
    """
    >>> terminal_velocity(1, 25, 0.6, 0.77)
    1.3031197996044768
    >>> terminal_velocity(2, 100, 0.45, 0.23)
    1.9467947148674276
    >>> terminal_velocity(5, 50, 0.2, 0.5)
    4.428690551393267
    >>> terminal_velocity(-5, 50, -0.2, -2)
    Traceback (most recent call last):
        ...
    ValueError: mass, density, area and the drag coefficient all need to be positive
    >>> terminal_velocity(3, -20, -1, 2)
    Traceback (most recent call last):
        ...
    ValueError: mass, density, area and the drag coefficient all need to be positive
    >>> terminal_velocity(-2, -1, -0.44, -1)
    Traceback (most recent call last):
        ...
    ValueError: mass, density, area and the drag coefficient all need to be positive
    """
    if mass <= 0 or density <= 0 or area <= 0 or drag_coefficient <= 0:
        raise ValueError(
            "mass, density, area and the drag coefficient all need to be positive"
        )
    return ((2 * mass * g) / (density * area * drag_coefficient)) ** 0.5


if __name__ == "__main__":
    import doctest

    doctest.testmod()
