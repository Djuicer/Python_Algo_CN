"""
* Author: Manuel Di Lullo (https://github.com/manueldilullo)
* 说明：转换数值，使其使用正确的 SI 或二进制单位前缀。

灵感来自本仓库中 lance-pyles 编写的 prefix_conversion.py 文件。

URL: https://en.wikipedia.org/wiki/Metric_prefix#List_of_SI_prefixes
URL: https://en.wikipedia.org/wiki/Binary_prefix
"""

from __future__ import annotations

from enum import Enum, unique
from typing import TypeVar

# 创建一个可表示 'Enum' 或其任意子类的泛型变量
T = TypeVar("T", bound="Enum")


@unique
class BinaryUnit(Enum):
    yotta = 80
    zetta = 70
    exa = 60
    peta = 50
    tera = 40
    giga = 30
    mega = 20
    kilo = 10


@unique
class SIUnit(Enum):
    yotta = 24
    zetta = 21
    exa = 18
    peta = 15
    tera = 12
    giga = 9
    mega = 6
    kilo = 3
    hecto = 2
    deca = 1
    deci = -1
    centi = -2
    milli = -3
    micro = -6
    nano = -9
    pico = -12
    femto = -15
    atto = -18
    zepto = -21
    yocto = -24

    @classmethod
    def get_positive(cls) -> dict:
        """
        返回一个仅包含此枚举中正值元素的字典。
        >>> from itertools import islice
        >>> positive = SIUnit.get_positive()
        >>> inc = iter(positive.items())
        >>> dict(islice(inc, len(positive) // 2))
        {'yotta': 24, 'zetta': 21, 'exa': 18, 'peta': 15, 'tera': 12}
        >>> dict(inc)
        {'giga': 9, 'mega': 6, 'kilo': 3, 'hecto': 2, 'deca': 1}
        """
        return {unit.name: unit.value for unit in cls if unit.value > 0}

    @classmethod
    def get_negative(cls) -> dict:
        """
        返回一个仅包含此枚举中负值元素的字典。
        @example
        >>> from itertools import islice
        >>> negative = SIUnit.get_negative()
        >>> inc = iter(negative.items())
        >>> dict(islice(inc, len(negative) // 2))
        {'deci': -1, 'centi': -2, 'milli': -3, 'micro': -6, 'nano': -9}
        >>> dict(inc)
        {'pico': -12, 'femto': -15, 'atto': -18, 'zepto': -21, 'yocto': -24}
        """
        return {unit.name: unit.value for unit in cls if unit.value < 0}


def add_si_prefix(value: float) -> str:
    """
    将数值转换为带 SI 前缀的形式。
    @input value（整数）
    @example:
    >>> add_si_prefix(10000)
    '10.0 kilo'
    """
    prefixes = SIUnit.get_positive() if value > 0 else SIUnit.get_negative()
    for name_prefix, value_prefix in prefixes.items():
        numerical_part = value / (10**value_prefix)
        if numerical_part > 1:
            return f"{numerical_part!s} {name_prefix}"
    return str(value)


def add_binary_prefix(value: float) -> str:
    """
    将数值转换为带二进制前缀的形式。
    @input value（整数）
    @example:
    >>> add_binary_prefix(65536)
    '64.0 kilo'
    """
    for prefix in BinaryUnit:
        numerical_part = value / (2**prefix.value)
        if numerical_part > 1:
            return f"{numerical_part!s} {prefix.name}"
    return str(value)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
