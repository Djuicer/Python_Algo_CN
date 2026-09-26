"""
根据法拉第定律，电流的产生取决于磁通量的变化。因此，磁通量随时间的变化
等价于以伏特 (V) 为单位的电势，历史上称为感应电动势 (ε)。关系式为：

---------------
| ε = ΔΦ / Δt |
---------------

ε --> 感应电动势（V - 伏特）

ΔΦ = ΦF - Φi - 磁通量变化 (Wb)

Δt - 时间间隔 (s)

此外，根据能量守恒原理，法拉第定律中需要加入负号。该符号由楞次定律引入，
可用于确定电流方向：

感应电流的方向总使其产生的磁通量反抗引起该电流的磁通量变化。

综合以上信息得到法拉第－楞次定律：

-----------------
| ε = - ΔΦ / Δt |
-----------------

（说明改编自 https://en.wikipedia.org/wiki/Faraday%27s_law_of_induction ）
"""


def __check_args(final_flux: float, initinal_flux: float, time_interval: float) -> None:
    """
    检查参数是否有效。
    >>> __check_args(50, 10, -10)
    Traceback (most recent call last):
        ...
    ValueError: Invalid time interval. Should be a positive number.
    >>> __check_args("50", 10, 10)
    Traceback (most recent call last):
        ...
    TypeError: Invalid final flux. Should be an integer or float.
    """

    # 确保实例有效
    if not isinstance(final_flux, (int, float)):
        raise TypeError("Invalid final flux. Should be an integer or float.")

    if not isinstance(initinal_flux, (int, float)):
        raise TypeError("Invalid final flux. Should be an integer or float.")

    if not isinstance(time_interval, (int, float)):
        raise TypeError("Invalid time interval. Should be an integer or float.")

    # 确保时间间隔有效
    if time_interval < 0:
        raise ValueError("Invalid time interval. Should be a positive number.")


def induced_electromotive_force(
    final_flux: float, initinal_flux: float, time_interval: float
) -> float:
    """
    >>> induced_electromotive_force(50.0, 20, 3.0)
    -10.0
    >>> induced_electromotive_force(40, 30, 10.0)
    -1.0
    >>> induced_electromotive_force(30.0, 50.0, 10)
    2.0
    >>> induced_electromotive_force(100, 100.0, 20.0)
    -0.0
    >>> induced_electromotive_force(10.0, 2.0, -2.0)
    Traceback (most recent call last):
        ...
    ValueError: Invalid time interval. Should be a positive number.
    >>> induced_electromotive_force(11.0, 'a', 5.0)
    Traceback (most recent call last):
        ...
    TypeError: Invalid final flux. Should be an integer or float.
    """
    __check_args(final_flux, initinal_flux, time_interval)
    flux_variation = final_flux - initinal_flux
    return round(-flux_variation / time_interval, 1)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
