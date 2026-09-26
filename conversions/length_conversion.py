"""
长度单位转换。
可用单位：Metre,Kilometre,Feet,Inch,Centimeter,Yard,Foot,Mile,Millimeter

用法：
-> 将此文件导入相应项目。
-> 使用 length_conversion() 函数转换长度单位。
-> 参数：
    -> value：要转换的数值
    -> from_type：原单位类型
    -> to_type：目标单位类型

参考资料：
-> 维基百科参考资料：https://en.wikipedia.org/wiki/Meter
-> 维基百科参考资料：https://en.wikipedia.org/wiki/Kilometer
-> 维基百科参考资料：https://en.wikipedia.org/wiki/Feet
-> 维基百科参考资料：https://en.wikipedia.org/wiki/Inch
-> 维基百科参考资料：https://en.wikipedia.org/wiki/Centimeter
-> 维基百科参考资料：https://en.wikipedia.org/wiki/Yard
-> 维基百科参考资料：https://en.wikipedia.org/wiki/Foot
-> 维基百科参考资料：https://en.wikipedia.org/wiki/Mile
-> 维基百科参考资料：https://en.wikipedia.org/wiki/Millimeter
"""

from typing import NamedTuple


class FromTo(NamedTuple):
    from_factor: float
    to_factor: float


TYPE_CONVERSION = {
    "millimeter": "mm",
    "centimeter": "cm",
    "meter": "m",
    "kilometer": "km",
    "inch": "in",
    "inche": "in",  # 末尾的 's' 已被移除
    "feet": "ft",
    "foot": "ft",
    "yard": "yd",
    "mile": "mi",
}

METRIC_CONVERSION = {
    "mm": FromTo(0.001, 1000),
    "cm": FromTo(0.01, 100),
    "m": FromTo(1, 1),
    "km": FromTo(1000, 0.001),
    "in": FromTo(0.0254, 39.3701),
    "ft": FromTo(0.3048, 3.28084),
    "yd": FromTo(0.9144, 1.09361),
    "mi": FromTo(1609.34, 0.000621371),
}


def length_conversion(value: float, from_type: str, to_type: str) -> float:
    """
    长度单位之间的转换。

    >>> length_conversion(4, "METER", "FEET")
    13.12336
    >>> length_conversion(4, "M", "FT")
    13.12336
    >>> length_conversion(1, "meter", "kilometer")
    0.001
    >>> length_conversion(1, "kilometer", "inch")
    39370.1
    >>> length_conversion(3, "kilometer", "mile")
    1.8641130000000001
    >>> length_conversion(2, "feet", "meter")
    0.6096
    >>> length_conversion(4, "feet", "yard")
    1.333329312
    >>> length_conversion(1, "inch", "meter")
    0.0254
    >>> length_conversion(2, "inch", "mile")
    3.15656468e-05
    >>> length_conversion(2, "centimeter", "millimeter")
    20.0
    >>> length_conversion(2, "centimeter", "yard")
    0.0218722
    >>> length_conversion(4, "yard", "meter")
    3.6576
    >>> length_conversion(4, "yard", "kilometer")
    0.0036576
    >>> length_conversion(3, "foot", "meter")
    0.9144000000000001
    >>> length_conversion(3, "foot", "inch")
    36.00001944
    >>> length_conversion(4, "mile", "kilometer")
    6.43736
    >>> length_conversion(2, "miles", "InChEs")
    126719.753468
    >>> length_conversion(3, "millimeter", "centimeter")
    0.3
    >>> length_conversion(3, "mm", "in")
    0.1181103
    >>> length_conversion(4, "wrongUnit", "inch")
    Traceback (most recent call last):
      ...
    ValueError: Invalid 'from_type' value: 'wrongUnit'.
    Conversion abbreviations are: mm, cm, m, km, in, ft, yd, mi
    """
    new_from = from_type.lower().rstrip("s")
    new_from = TYPE_CONVERSION.get(new_from, new_from)
    new_to = to_type.lower().rstrip("s")
    new_to = TYPE_CONVERSION.get(new_to, new_to)
    if new_from not in METRIC_CONVERSION:
        msg = (
            f"Invalid 'from_type' value: {from_type!r}.\n"
            f"Conversion abbreviations are: {', '.join(METRIC_CONVERSION)}"
        )
        raise ValueError(msg)
    if new_to not in METRIC_CONVERSION:
        msg = (
            f"Invalid 'to_type' value: {to_type!r}.\n"
            f"Conversion abbreviations are: {', '.join(METRIC_CONVERSION)}"
        )
        raise ValueError(msg)
    return (
        value
        * METRIC_CONVERSION[new_from].from_factor
        * METRIC_CONVERSION[new_to].to_factor
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
