"""
气体分子的均方根速率、平均速率和最概然速率均由 Maxwell-Boltzmann 分布
导出。Maxwell-Boltzmann 分布是描述理想气体粒子速率分布的概率分布。

该分布由以下方程给出：

        -------------------------------------------------
        | f(v) = (M/2πRT)^(3/2) * 4πv^2 * e^(-Mv^2/2RT) |
        -------------------------------------------------

其中：
    * ``f(v)`` 是速率为 ``v`` 的分子比例
    * ``M`` 是气体摩尔质量，单位为 kg/mol
    * ``R`` 是气体常数
    * ``T`` 是绝对温度

有关 Maxwell-Boltzmann 分布的更多信息见：
https://en.wikipedia.org/wiki/Maxwell%E2%80%93Boltzmann_distribution

对 Maxwell-Boltzmann 分布从 0 到无穷积分，再除以分子总数，可计算平均速率。
结果为：

        ----------------------
        | v_avg = √(8RT/πM)  |
        ----------------------

最概然速率是 Maxwell-Boltzmann 分布达到最大值时的速率。对该分布关于 ``v``
求导并令结果为零即可求得：

        ----------------------
        | v_mp = √(2RT/M)    |
        ----------------------

均方根速率是衡量气体分子平均速率的另一指标，等于分子速率平方平均值的
平方根。结果为：

        ----------------------
        | v_rms = √(3RT/M)   |
        ----------------------

这里定义函数，根据气体温度和摩尔质量计算分子的平均速率和最概然速率。
"""

# 从 scipy.constants 库导入常数 R 和 pi
from scipy.constants import R, pi


def avg_speed_of_molecule(temperature: float, molar_mass: float) -> float:
    """
    接收气体温度（单位 K）和摩尔质量（单位 kg/mol），返回气体分子的平均
    速率（单位 m/s）。

    示例：

    >>> avg_speed_of_molecule(273, 0.028) # nitrogen at 273 K
    454.3488755062257
    >>> avg_speed_of_molecule(300, 0.032) # oxygen at 300 K
    445.5257273433045
    >>> avg_speed_of_molecule(-273, 0.028) # invalid temperature
    Traceback (most recent call last):
        ...
    Exception: Absolute temperature cannot be less than 0 K
    >>> avg_speed_of_molecule(273, 0) # invalid molar mass
    Traceback (most recent call last):
        ...
    Exception: Molar mass should be greater than 0 kg/mol
    """

    if temperature < 0:
        raise Exception("Absolute temperature cannot be less than 0 K")
    if molar_mass <= 0:
        raise Exception("Molar mass should be greater than 0 kg/mol")
    return (8 * R * temperature / (pi * molar_mass)) ** 0.5


def mps_speed_of_molecule(temperature: float, molar_mass: float) -> float:
    """
    接收气体温度（单位 K）和摩尔质量（单位 kg/mol），返回气体分子的最概然
    速率（单位 m/s）。

    示例：

    >>> mps_speed_of_molecule(273, 0.028) # nitrogen at 273 K
    402.65620702280023
    >>> mps_speed_of_molecule(300, 0.032) # oxygen at 300 K
    394.8368955535605
    >>> mps_speed_of_molecule(-273, 0.028) # invalid temperature
    Traceback (most recent call last):
        ...
    Exception: Absolute temperature cannot be less than 0 K
    >>> mps_speed_of_molecule(273, 0) # invalid molar mass
    Traceback (most recent call last):
        ...
    Exception: Molar mass should be greater than 0 kg/mol
    """

    if temperature < 0:
        raise Exception("Absolute temperature cannot be less than 0 K")
    if molar_mass <= 0:
        raise Exception("Molar mass should be greater than 0 kg/mol")
    return (2 * R * temperature / molar_mass) ** 0.5


if __name__ == "__main__":
    import doctest

    doctest.testmod()
