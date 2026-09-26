"""
标题：
利用爱因斯坦方程求质量对应的能量以及能量对应的质量。

说明：
爱因斯坦的质能等价关系是理论物理学中的核心概念。它指出能量 (E) 与质量
(m) 通过真空光速 (c) 的平方直接相关，即 E = mc²。质量与能量可以相互转换；
质量增加对应能量增加，反之亦然。该原理可解释核反应中原子核的微小变化
为何能够释放巨大能量。

方程：
E = mc² 和 m = E/c²，其中 m 为质量，E 为能量，c 为真空光速。

参考资料：
https://en.wikipedia.org/wiki/Mass%E2%80%93energy_equivalence
"""

from scipy.constants import c  # 真空光速 (299792458 m/s)


def energy_from_mass(mass: float) -> float:
    """
    使用 E = mc²，根据以 kg 为单位的质量计算以 SI 单位 J 表示的等价能量。

    mass (float): 物体质量。

    用法示例：
    >>> energy_from_mass(124.56)
    1.11948945063458e+19
    >>> energy_from_mass(320)
    2.8760165719578165e+19
    >>> energy_from_mass(0)
    0.0
    >>> energy_from_mass(-967.9)
    Traceback (most recent call last):
        ...
    ValueError: Mass can't be negative.

    """
    if mass < 0:
        raise ValueError("Mass can't be negative.")
    return mass * c**2


def mass_from_energy(energy: float) -> float:
    """
    使用 m = E/c²，根据以 J 为单位的能量计算以 SI 单位 kg 表示的等价质量。

    energy (float): 物体的能量。

    用法示例：
    >>> mass_from_energy(124.56)
    1.3859169098203872e-15
    >>> mass_from_energy(320)
    3.560480179371579e-15
    >>> mass_from_energy(0)
    0.0
    >>> mass_from_energy(-967.9)
    Traceback (most recent call last):
        ...
    ValueError: Energy can't be negative.

    """
    if energy < 0:
        raise ValueError("Energy can't be negative.")
    return energy / c**2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
