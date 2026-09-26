"""
标题：利用气压计算海拔

说明：
    以下算法使用气压公式估算海拔。


"""


def get_altitude_at_pressure(pressure: float) -> float:
    """
    本方法以海平面气压为基准，根据气压计算海拔。气压单位为 Pa。
    https://en.wikipedia.org/wiki/Pressure_altitude
    https://community.bosch-sensortec.com/t5/Question-and-answers/How-to-calculate-the-altitude-from-the-pressure-sensor-data/qaq-p/5702

    H = 44330 * [1 - (P/p0)^(1/5.255) ]

    其中：
    H = 海拔 (m)
    P = 测得的气压
    p0 = 海平面参考气压 101325 Pa

    示例：
    >>> get_altitude_at_pressure(pressure=100_000)
    105.47836610778828
    >>> get_altitude_at_pressure(pressure=101_325)
    0.0
    >>> get_altitude_at_pressure(pressure=80_000)
    1855.873388064995
    >>> get_altitude_at_pressure(pressure=201_325)
    Traceback (most recent call last):
      ...
    ValueError: Value Higher than Pressure at Sea Level !
    >>> get_altitude_at_pressure(pressure=-80_000)
    Traceback (most recent call last):
      ...
    ValueError: Atmospheric Pressure can not be negative !
    """

    if pressure > 101325:
        raise ValueError("Value Higher than Pressure at Sea Level !")
    if pressure < 0:
        raise ValueError("Atmospheric Pressure can not be negative !")
    return 44_330 * (1 - (pressure / 101_325) ** (1 / 5.5255))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
