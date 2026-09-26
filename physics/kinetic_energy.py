"""
根据物体的质量和速度求其动能。

说明：在物理学中，动能是物体因运动而具有的能量，定义为使给定质量的物体
从静止加速到指定速度所需的功。物体在加速过程中获得这部分能量，只要速度
不变就会保持该动能；从当前速度减速至静止时，物体会做同样大小的功。
形式上，动能是系统拉格朗日量中包含时间导数的项。

在经典力学中，质量为 m、速度为 v 的非旋转物体，其动能为 ½mv²。在相对论
力学中，仅当 v 远小于光速时，该式才是良好近似。动能的标准单位是焦耳，
英制单位是英尺磅。

参考资料：https://en.m.wikipedia.org/wiki/Kinetic_energy
"""


def kinetic_energy(mass: float, velocity: float) -> float:
    """
    计算动能。

    质量为 m、速度为 v 的非旋转物体，其动能为 ½mv²。

    >>> kinetic_energy(10,10)
    500.0
    >>> kinetic_energy(0,10)
    0.0
    >>> kinetic_energy(10,0)
    0.0
    >>> kinetic_energy(20,-20)
    4000.0
    >>> kinetic_energy(0,0)
    0.0
    >>> kinetic_energy(2,2)
    4.0
    >>> kinetic_energy(100,100)
    500000.0
    """
    if mass < 0:
        raise ValueError("The mass of a body cannot be negative")
    return 0.5 * mass * abs(velocity) * abs(velocity)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
