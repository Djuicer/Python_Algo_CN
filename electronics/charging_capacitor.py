# 来源 - The ARRL Handbook for Radio Communications
# https://en.wikipedia.org/wiki/RC_time_constant

"""
说明
-----------
电容器连接电源（AC 或 DC）后会开始充电。如果电路中有一个电阻与电容器串联，
电容器的充电速度会降低，所需时间比通常情况更长。
电容器充电时，其电压随时间按指数函数变化。

'resistance(ohms) * capacitance(farads)' 称为 RC 时间常数，也可表示为 τ (tau)。
利用该 RC 时间常数以及包含 RC 的指数函数，可以求出电容器从开始充电起任意时刻
't' 的电压。这一关系同时适用于电容器的充电和放电过程。
"""

from math import exp  # exp 的值 = 2.718281828459…


def charging_capacitor(
    source_voltage: float,  # 电压，单位为 volts。
    resistance: float,  # 电阻，单位为 ohms。
    capacitance: float,  # 电容，单位为 farads。
    time_sec: float,  # 电容器开始充电后经过的时间，单位为 seconds。
) -> float:
    """
    求电容器开始充电后任意第 n 秒的电压。

    示例
    --------
    >>> charging_capacitor(source_voltage=.2,resistance=.9,capacitance=8.4,time_sec=.5)
    0.013

    >>> charging_capacitor(source_voltage=2.2,resistance=3.5,capacitance=2.4,time_sec=9)
    1.446

    >>> charging_capacitor(source_voltage=15,resistance=200,capacitance=20,time_sec=2)
    0.007

    >>> charging_capacitor(20, 2000, 30*pow(10,-5), 4)
    19.975

    >>> charging_capacitor(source_voltage=0,resistance=10.0,capacitance=.30,time_sec=3)
    Traceback (most recent call last):
        ...
    ValueError: Source voltage must be positive.

    >>> charging_capacitor(source_voltage=20,resistance=-2000,capacitance=30,time_sec=4)
    Traceback (most recent call last):
        ...
    ValueError: Resistance must be positive.

    >>> charging_capacitor(source_voltage=30,resistance=1500,capacitance=0,time_sec=4)
    Traceback (most recent call last):
        ...
    ValueError: Capacitance must be positive.
    """

    if source_voltage <= 0:
        raise ValueError("Source voltage must be positive.")
    if resistance <= 0:
        raise ValueError("Resistance must be positive.")
    if capacitance <= 0:
        raise ValueError("Capacitance must be positive.")
    return round(source_voltage * (1 - exp(-time_sec / (resistance * capacitance))), 3)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
