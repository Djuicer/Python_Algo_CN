from __future__ import annotations

"""
    计算无稳态 555 定时器的频率和/或占空比。
    * https://en.wikipedia.org/wiki/555_timer_IC#Astable

    这些函数接收外部电阻（单位为 ohms）和电容（单位为 Microfarad）的值，
    并计算以下内容：

    -------------------------------------
    | Freq = 1.44 /[( R1+ 2 x R2) x C1] |               ... in Hz
    -------------------------------------
    其中 Freq 为频率，
          R1 为第一个电阻，单位为 ohms，
          R2 为第二个电阻，单位为 ohms，
          C1 为电容，单位为 Microfarads。

    ------------------------------------------------
    | Duty Cycle = (R1 + R2) / (R1 + 2 x R2) x 100 |    ... in %
    ------------------------------------------------
    其中 R1 为第一个电阻，单位为 ohms，
          R2 为第二个电阻，单位为 ohms。
"""


def astable_frequency(
    resistance_1: float, resistance_2: float, capacitance: float
) -> float:
    """
    用法示例：
    >>> astable_frequency(resistance_1=45, resistance_2=45, capacitance=7)
    1523.8095238095239
    >>> astable_frequency(resistance_1=356, resistance_2=234, capacitance=976)
    1.7905459175553078
    >>> astable_frequency(resistance_1=2, resistance_2=-1, capacitance=2)
    Traceback (most recent call last):
        ...
    ValueError: All values must be positive
    >>> astable_frequency(resistance_1=45, resistance_2=45, capacitance=0)
    Traceback (most recent call last):
        ...
    ValueError: All values must be positive
    """

    if resistance_1 <= 0 or resistance_2 <= 0 or capacitance <= 0:
        raise ValueError("All values must be positive")
    return (1.44 / ((resistance_1 + 2 * resistance_2) * capacitance)) * 10**6


def astable_duty_cycle(resistance_1: float, resistance_2: float) -> float:
    """
    用法示例：
    >>> astable_duty_cycle(resistance_1=45, resistance_2=45)
    66.66666666666666
    >>> astable_duty_cycle(resistance_1=356, resistance_2=234)
    71.60194174757282
    >>> astable_duty_cycle(resistance_1=2, resistance_2=-1)
    Traceback (most recent call last):
        ...
    ValueError: All values must be positive
    >>> astable_duty_cycle(resistance_1=0, resistance_2=0)
    Traceback (most recent call last):
        ...
    ValueError: All values must be positive
    """

    if resistance_1 <= 0 or resistance_2 <= 0:
        raise ValueError("All values must be positive")
    return (resistance_1 + resistance_2) / (resistance_1 + 2 * resistance_2) * 100


if __name__ == "__main__":
    import doctest

    doctest.testmod()
