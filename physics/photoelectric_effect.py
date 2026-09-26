"""
光电效应是光等电磁辐射照射材料时电子逸出的现象，以这种方式逸出的电子称为
光电子。

1905 年，爱因斯坦基于光由称为光子或光量子的微小能量包组成这一概念提出了
光电效应理论。每个能量包携带与相应电磁波频率 v 成正比的能量 hv，比例常数
h 称为普朗克常数。电子吸收能量为 hv 的光子并摆脱原子束缚后，其最大动能
K_max 为：

K_max = hv-W

其中 W 是使电子从材料表面逸出所需的最小能量，称为表面逸出功。

参考资料：https://en.wikipedia.org/wiki/Photoelectric_effect

"""

PLANCK_CONSTANT_JS = 6.6261 * pow(10, -34)  # SI 单位 (Js)
PLANCK_CONSTANT_EVS = 4.1357 * pow(10, -15)  # 单位为 eVs


def maximum_kinetic_energy(
    frequency: float, work_function: float, in_ev: bool = False
) -> float:
    """
    计算从表面逸出电子的最大动能。若最大动能为零，则没有电子逸出，或给定
    电磁波频率过低。

    frequency (float): 电磁波频率。
    work_function (float): 表面逸出功。
    in_ev (optional)(bool): 数值单位为 eV 时传入 True。

    用法示例：
    >>> maximum_kinetic_energy(1000000,2)
    0
    >>> maximum_kinetic_energy(1000000,2,True)
    0
    >>> maximum_kinetic_energy(10000000000000000,2,True)
    39.357000000000006
    >>> maximum_kinetic_energy(-9,20)
    Traceback (most recent call last):
        ...
    ValueError: Frequency can't be negative.

    >>> maximum_kinetic_energy(1000,"a")
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for -: 'float' and 'str'

    """
    if frequency < 0:
        raise ValueError("Frequency can't be negative.")
    if in_ev:
        return max(PLANCK_CONSTANT_EVS * frequency - work_function, 0)
    return max(PLANCK_CONSTANT_JS * frequency - work_function, 0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
