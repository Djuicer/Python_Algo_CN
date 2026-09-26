from scipy.constants import g

"""
以地球为参考，根据物体质量和离地高度计算其重力势能。


说明：引力势能或重力势能是有质量物体因重力而相对于另一有质量物体具有的
势能。它与引力场相关，当物体相互靠近并下落时会释放（转化为动能）。
两个物体相距更远时，引力势能增加。

对于一对相互作用的点粒子，引力势能 U 为：
U=-GMm/R
其中 M 和 m 为两个粒子的质量，R 为两者间距，G 为引力常数。
在地球表面附近，引力场近似恒定，物体的重力势能简化为：
U=mgh
其中 m 为物体质量，g=GM/R² 为地球重力加速度，h 为物体质心高于所选参考面
的高度。

参考资料："https://en.m.wikipedia.org/wiki/Gravitational_energy"
"""


def potential_energy(mass: float, height: float) -> float:
    # 函数接收质量和高度作为参数，并返回重力势能
    """
    >>> potential_energy(10,10)
    980.665
    >>> potential_energy(0,5)
    0.0
    >>> potential_energy(8,0)
    0.0
    >>> potential_energy(10,5)
    490.3325
    >>> potential_energy(0,0)
    0.0
    >>> potential_energy(2,8)
    156.9064
    >>> potential_energy(20,100)
    19613.3
    """
    if mass < 0:
        # 处理质量为负值的情况
        raise ValueError("The mass of a body cannot be negative")
    if height < 0:
        # 处理高度为负值的情况
        raise ValueError("The height above the ground cannot be negative")
    return mass * g * height


if __name__ == "__main__":
    from doctest import testmod

    testmod(name="potential_energy")
