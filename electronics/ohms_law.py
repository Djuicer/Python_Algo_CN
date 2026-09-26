# https://en.wikipedia.org/wiki/Ohm%27s_law
from __future__ import annotations


def ohms_law(voltage: float, current: float, resistance: float) -> dict[str, float]:
    """
    对 voltage、current 和 resistance 中任意两个给定电气量应用欧姆定律，并在
    Python 字典中返回取零参数的名称/数值对。

    >>> ohms_law(voltage=10, resistance=5, current=0)
    {'current': 2.0}
    >>> ohms_law(voltage=0, current=0, resistance=10)
    Traceback (most recent call last):
      ...
    ValueError: One and only one argument must be 0
    >>> ohms_law(voltage=0, current=1, resistance=-2)
    Traceback (most recent call last):
      ...
    ValueError: Resistance cannot be negative
    >>> ohms_law(resistance=0, voltage=-10, current=1)
    {'resistance': -10.0}
    >>> ohms_law(voltage=0, current=-1.5, resistance=2)
    {'voltage': -3.0}
    """
    if (voltage, current, resistance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if resistance < 0:
        raise ValueError("Resistance cannot be negative")
    if voltage == 0:
        return {"voltage": float(current * resistance)}
    elif current == 0:
        return {"current": voltage / resistance}
    elif resistance == 0:
        return {"resistance": voltage / current}
    else:
        raise ValueError("Exactly one argument must be 0")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
