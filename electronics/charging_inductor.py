# 来源 - The ARRL Handbook for Radio Communications
# https://en.wikipedia.org/wiki/RL_circuit

"""
说明
-----------
电感器是一种无源电子器件。与电容器不同，它将能量储存在“磁场”或“静磁场”中。

电感器接入 'DC' 电流源时，其表现类似导线，无法观察到实际效应，也不会储存能量。
电感器仅在 'AC' 电流下工作时储存能量。

将电感器与电阻串联后接入 'AC' 电源，电流从零变为有限值时，电感器中会突然产生
阻碍电流变化的感应电压，导致电流在初始阶段缓慢上升。如果电流不再变化，感应
电压也会消失。电阻为零时，电流将持续上升。

'Resistance(ohms) / Inductance(henrys)' 称为 RL 时间常数，也可表示为 τ (tau)。
电感器与电阻组成电路时，其充电过程呈指数函数关系。

电感器接入 'AC' 电源后，会开始在“磁场”中储存能量。利用“RL 时间常数”，可以求出
电感器充电过程中任意时刻的电流。
"""

from math import exp  # exp 的值 = 2.718281828459…


def charging_inductor(
    source_voltage: float,  # source_voltage 的单位应为 volts。
    resistance: float,  # resistance 的单位应为 ohms。
    inductance: float,  # inductance 的单位应为 henrys。
    time: float,  # time 的单位应为 seconds。
) -> float:
    """
    求电感器开始充电后任意第 n 秒的电流。

    示例
    --------
    >>> charging_inductor(source_voltage=5.8,resistance=1.5,inductance=2.3,time=2)
    2.817

    >>> charging_inductor(source_voltage=8,resistance=5,inductance=3,time=2)
    1.543

    >>> charging_inductor(source_voltage=8,resistance=5*pow(10,2),inductance=3,time=2)
    0.016

    >>> charging_inductor(source_voltage=-8,resistance=100,inductance=15,time=12)
    Traceback (most recent call last):
        ...
    ValueError: Source voltage must be positive.

    >>> charging_inductor(source_voltage=80,resistance=-15,inductance=100,time=5)
    Traceback (most recent call last):
        ...
    ValueError: Resistance must be positive.

    >>> charging_inductor(source_voltage=12,resistance=200,inductance=-20,time=5)
    Traceback (most recent call last):
        ...
    ValueError: Inductance must be positive.

    >>> charging_inductor(source_voltage=0,resistance=200,inductance=20,time=5)
    Traceback (most recent call last):
        ...
    ValueError: Source voltage must be positive.

    >>> charging_inductor(source_voltage=10,resistance=0,inductance=20,time=5)
    Traceback (most recent call last):
        ...
    ValueError: Resistance must be positive.

    >>> charging_inductor(source_voltage=15, resistance=25, inductance=0, time=5)
    Traceback (most recent call last):
        ...
    ValueError: Inductance must be positive.
    """

    if source_voltage <= 0:
        raise ValueError("Source voltage must be positive.")
    if resistance <= 0:
        raise ValueError("Resistance must be positive.")
    if inductance <= 0:
        raise ValueError("Inductance must be positive.")
    return round(
        source_voltage / resistance * (1 - exp((-time * resistance) / inductance)), 3
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
