"""
理想气体定律又称通用气体方程，是假想理想气体的状态方程。尽管存在一些
局限，它在许多条件下都能很好地近似多种气体的行为。Benoît Paul Émile
Clapeyron 于 1834 年首次将经验性的 Boyle 定律、Charles 定律、Avogadro
定律和 Gay-Lussac 定律结合起来表述该定律。[1] 理想气体定律通常写作：
 ------------
 | PV = nRT |
 ------------
P	=	压强 (Pa)
V	=	体积 (m^3)
n	=	物质的量 (mol)
R	=	通用气体常数
T	=	绝对温度 (Kelvin)

（说明改编自 https://en.wikipedia.org/wiki/Ideal_gas_law ）
"""

UNIVERSAL_GAS_CONSTANT = 8.314462  # 单位 - J mol-1 K-1


def pressure_of_gas_system(moles: float, kelvin: float, volume: float) -> float:
    """
    >>> pressure_of_gas_system(2, 100, 5)
    332.57848
    >>> pressure_of_gas_system(0.5, 273, 0.004)
    283731.01575
    >>> pressure_of_gas_system(3, -0.46, 23.5)
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter positive value.
    """
    if moles < 0 or kelvin < 0 or volume < 0:
        raise ValueError("Invalid inputs. Enter positive value.")
    return moles * kelvin * UNIVERSAL_GAS_CONSTANT / volume


def volume_of_gas_system(moles: float, kelvin: float, pressure: float) -> float:
    """
    >>> volume_of_gas_system(2, 100, 5)
    332.57848
    >>> volume_of_gas_system(0.5, 273, 0.004)
    283731.01575
    >>> volume_of_gas_system(3, -0.46, 23.5)
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter positive value.
    """
    if moles < 0 or kelvin < 0 or pressure < 0:
        raise ValueError("Invalid inputs. Enter positive value.")
    return moles * kelvin * UNIVERSAL_GAS_CONSTANT / pressure


def temperature_of_gas_system(moles: float, volume: float, pressure: float) -> float:
    """
    >>> temperature_of_gas_system(2, 100, 5)
    30.068090996146232
    >>> temperature_of_gas_system(11, 5009, 1000)
    54767.66101807144
    >>> temperature_of_gas_system(3, -0.46, 23.5)
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter positive value.
    """
    if moles < 0 or volume < 0 or pressure < 0:
        raise ValueError("Invalid inputs. Enter positive value.")

    return pressure * volume / (moles * UNIVERSAL_GAS_CONSTANT)


def moles_of_gas_system(kelvin: float, volume: float, pressure: float) -> float:
    """
    >>> moles_of_gas_system(100, 5, 10)
    0.06013618199229246
    >>> moles_of_gas_system(110, 5009, 1000)
    5476.766101807144
    >>> moles_of_gas_system(3, -0.46, 23.5)
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter positive value.
    """
    if kelvin < 0 or volume < 0 or pressure < 0:
        raise ValueError("Invalid inputs. Enter positive value.")

    return pressure * volume / (kelvin * UNIVERSAL_GAS_CONSTANT)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
