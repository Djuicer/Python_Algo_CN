from typing import NamedTuple


class Result(NamedTuple):
    name: str
    value: float


def max_load_current(rf: float, rs: float, rl: float, vm: float) -> tuple:
    """
    计算全波整流电路中的最大负载电流（Im）。
    Im = 最大负载电流
    rf = 二极管正向电阻
    rs = 变压器次级绕组电阻
    rl = 负载电阻
    vm = 最大电压或峰值电压
    情形：
    >>> max_load_current(rf=2 , rs=4 , rl=6 , vm=15 )
    Result(name='max_load_current', value=1.25)
    >>> max_load_current(rf=2 , rs=4 , rl=6 , vm=0 )
    Result(name='max_load_current', value=0.0)
    >>> max_load_current(rf=2 , rs=-4 , rl=6 , vm=15 )
    Traceback (most recent call last):
        ...
    ValueError: Resistance cannot be negative
    >>> max_load_current(rf=0 , rs=0 , rl=0 , vm=15 )
    Traceback (most recent call last):
        ...
    ValueError: At least one Resistance must be non-zero
    """
    if (rf, rs, rl).count(0) == 3:
        raise ValueError("At least one Resistance must be non-zero")
    if rf < 0 or rs < 0 or rl < 0:
        raise ValueError("Resistance cannot be negative")
    if vm == 0:
        return Result("max_load_current", vm / (rf + rs + rl))
    else:
        return Result("max_load_current", vm / (rf + rs + rl))


def dc_current(im: float) -> tuple:
    """
    计算电路中的平均直流电流（Idc）。
    在所有情形下，负号表示电流或电压方向相反。
    Idc = 平均直流电流（DC）
    im = 最大电流或峰值电流
    情形：
    >>> dc_current(im=2)
    Result(name='Idc', value=1.272)
    >>> dc_current(im=0)
    Result(name='Idc', value=0.0)
    """
    return Result("Idc", 2 * im * 0.318)


def dc_voltage(vm: float) -> tuple:
    """
    计算电路中的平均直流电压（Vdc）。
    在所有情形下，负号表示电流或电压方向相反。
    Vdc = 平均直流电压（DC）
    vm = 最大电压或峰值电压
    情形：
    >>> dc_voltage(vm=2)
    Result(name='Vdc', value=1.272)
    >>> dc_voltage(vm=0)
    Result(name='Vdc', value=0.0)
    """
    return Result("Vdc", 2 * 0.318 * vm)


def max_current(vm: float, rl: float) -> tuple:
    """
    计算电路中的最大电流（Im）。
    在所有情形下，负号表示电流或电压方向相反。
    vm = 最大电压或峰值电压
    rl = 负载电阻
    情形：
    >>> max_current(vm=2, rl=5)
    Result(name='Max_current_Im', value=0.4)
    >>> max_current(vm=2, rl=-5)
    Traceback (most recent call last):
        ...
    ValueError: Resistance cannot be negative or equal to zero

    """
    if rl <= 0:
        raise ValueError("Resistance cannot be negative or equal to zero")
    return Result("Max_current_Im", vm / rl)


def rms_current(im: float) -> tuple:
    """
    计算电流的均方根（RMS）值（Irms）。
    在所有情形下，负号表示电流或电压方向相反。
    Irms = 电流的均方根值
    im = 最大电流或峰值电流
    情形：
    >>> rms_current(im=10)
    Result(name='Irms', value=7.069999999999999)
    >>> rms_current(im=0)
    Result(name='Irms', value=0.0)
    """
    return Result("Irms", im * 0.707)


def rms_voltage(vm: float) -> tuple:
    """
    计算电压的均方根（RMS）值（Vrms）。
    在所有情形下，负号表示电流或电压方向相反。
    Vrms = 电压的均方根值
    vm = 最大电压或峰值电压
    情形：
    >>> rms_voltage(vm=20)
    Result(name='Vrms', value=14.139999999999999)
    >>> rms_voltage(vm=0)
    Result(name='Vrms', value=0.0)
    """
    return Result("Vrms", vm * 0.707)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
