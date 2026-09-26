# https://en.wikipedia.org/wiki/LC_circuit

"""LC 电路也称谐振电路、振荡回路或调谐电路，由字母 L 表示的电感器和字母 C
表示的电容器连接而成。该电路可用作电谐振器，是音叉的电气类比，其储存的
能量以电路的谐振频率振荡。
来源：https://en.wikipedia.org/wiki/LC_circuit
"""

from __future__ import annotations

from math import pi, sqrt


def resonant_frequency(inductance: float, capacitance: float) -> tuple:
    """
    根据给定的电感和电容值计算 LC 电路的谐振频率。

    示例如下：
    >>> resonant_frequency(inductance=10, capacitance=5)
    ('Resonant frequency', 0.022507907903927652)
    >>> resonant_frequency(inductance=0, capacitance=5)
    Traceback (most recent call last):
      ...
    ValueError: Inductance cannot be 0 or negative
    >>> resonant_frequency(inductance=10, capacitance=0)
    Traceback (most recent call last):
      ...
    ValueError: Capacitance cannot be 0 or negative
    """

    if inductance <= 0:
        raise ValueError("Inductance cannot be 0 or negative")

    if capacitance <= 0:
        raise ValueError("Capacitance cannot be 0 or negative")

    return (
        "Resonant frequency",
        float(1 / (2 * pi * (sqrt(inductance * capacitance)))),
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
