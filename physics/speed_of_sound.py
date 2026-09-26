"""
标题：计算声速

说明：
    声速 (c) 是声波在单位时间内传播的距离 (m/s)。声波在弹性介质中传播。

    声音在液体和气体中以纵波传播，在固体中以横波传播。本文件根据流体的
    体积模量和密度计算其声速。

    流体中的声速方程：
    c_fluid = sqrt(K_s / p)

    c_fluid: 流体中的声速
    K_s: 等熵体积模量
    p: 流体密度

来源：https://en.wikipedia.org/wiki/Speed_of_sound
"""


def speed_of_sound_in_a_fluid(density: float, bulk_modulus: float) -> float:
    """
    根据流体的密度和体积模量计算声速。

    示例：
    示例 1 --> 20°C 的水：bulk_modulus= 2.15MPa, density=998kg/m³
    示例 2 --> 20°C 的汞：bulk_modulus= 28.5MPa, density=13600kg/m³

    >>> speed_of_sound_in_a_fluid(bulk_modulus=2.15e9, density=998)
    1467.7563207952705
    >>> speed_of_sound_in_a_fluid(bulk_modulus=28.5e9, density=13600)
    1447.614670861731
    """

    if density <= 0:
        raise ValueError("Impossible fluid density")
    if bulk_modulus <= 0:
        raise ValueError("Impossible bulk modulus")

    return (bulk_modulus / density) ** 0.5


if __name__ == "__main__":
    import doctest

    doctest.testmod()
