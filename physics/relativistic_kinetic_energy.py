"""
根据粒子的静止质量和速度求其相对论动能。

说明：在狭义相对论中，粒子动能是其因运动而在静止能量之外具有的额外能量，
定义为相对论总能量与静止能量之差。力做功使粒子从静止加速到接近光速后，
只要速度不变，粒子就保持这部分相对论动能；要使其减速至静止，必须移除
同样多的能量。相对论动能出现在相对论能量－动量关系中，并取决于描述高速
下时空变化的洛伦兹因子。

在相对论力学中，静止质量为 m、速度为 v 的粒子，其动能 K 为：

    K = (y - 1) m c^2,

其中 c 为真空光速，并且：

    y = 1 / sqrt(1 - v^2 / c^2)

即洛伦兹因子。当速度远低于 c 时，该表达式化为经典公式 K ≈ (1/2) m v^2，
所以低速极限下相对论结果与牛顿力学动能一致。动能的标准单位为焦耳，英制
单位为英尺磅。

参考资料：https://en.wikipedia.org/wiki/Kinetic_energy
"""

from math import sqrt

from scipy.constants import c  # 真空光速 (299792458 m/s)


def relativistic_kinetic_energy(mass: float, velocity: float) -> float:
    """
    计算相对论动能。
    mass --- kg
    velocity ---- m/s
    K.E ---- j

    >>> relativistic_kinetic_energy(10,10)
    598.6912157608277
    >>> relativistic_kinetic_energy(40,200000)
    800000266962.5057
    >>> relativistic_kinetic_energy(50,100000)
    250000021062.11475
    >>> relativistic_kinetic_energy(0,0)
    0.0
    >>> relativistic_kinetic_energy(100,0)
    0.0

    """

    if mass < 0:
        raise ValueError("The mass of a body cannot be negative")
    gamma = 1 / sqrt(1 - (velocity**2 / c**2))
    return (gamma - 1) * mass * c**2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
