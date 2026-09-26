"""
时间单位是用于度量或表示时长的特定时间间隔。在国际单位制（SI）以及多数西方国家中，
时间的基本单位是秒，其定义约为铯原子振荡 90 亿次所经历的时间。

https://en.wikipedia.org/wiki/Unit_of_time
"""

time_chart: dict[str, float] = {
    "seconds": 1.0,
    "minutes": 60.0,  # 1 分钟 = 60 秒
    "hours": 3600.0,  # 1 小时 = 60 分钟 = 3600 秒
    "days": 86400.0,  # 1 天 = 24 小时 = 1440 分钟 = 86400 秒
    "weeks": 604800.0,  # 1 周 = 7 天 = 168 小时 = 10080 分钟 = 604800 秒
    "months": 2629800.0,  # 一个月所含秒数的近似值
    "years": 31557600.0,  # 一年所含秒数的近似值
}

time_chart_inverse: dict[str, float] = {
    key: 1 / value for key, value in time_chart.items()
}


def convert_time(time_value: float, unit_from: str, unit_to: str) -> float:
    """
    使用上方的 time_chart 在不同时间单位之间转换。

    >>> convert_time(3600, "seconds", "hours")
    1.0
    >>> convert_time(3500, "Seconds", "Hours")
    0.972
    >>> convert_time(1, "DaYs", "hours")
    24.0
    >>> convert_time(120, "minutes", "SeCoNdS")
    7200.0
    >>> convert_time(2, "WEEKS", "days")
    14.0
    >>> convert_time(0.5, "hours", "MINUTES")
    30.0
    >>> convert_time(-3600, "seconds", "hours")
    Traceback (most recent call last):
        ...
    ValueError: 'time_value' must be a non-negative number.
    >>> convert_time("Hello", "hours", "minutes")
    Traceback (most recent call last):
        ...
    ValueError: 'time_value' must be a non-negative number.
    >>> convert_time([0, 1, 2], "weeks", "days")
    Traceback (most recent call last):
        ...
    ValueError: 'time_value' must be a non-negative number.
    >>> convert_time(1, "cool", "century")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit cool is not in seconds, minutes, hours, days, weeks, ...
    >>> convert_time(1, "seconds", "hot")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit hot is not in seconds, minutes, hours, days, weeks, ...
    """
    if not isinstance(time_value, (int, float)) or time_value < 0:
        msg = "'time_value' must be a non-negative number."
        raise ValueError(msg)

    unit_from = unit_from.lower()
    unit_to = unit_to.lower()
    if unit_from not in time_chart or unit_to not in time_chart:
        invalid_unit = unit_from if unit_from not in time_chart else unit_to
        msg = f"Invalid unit {invalid_unit} is not in {', '.join(time_chart)}."
        raise ValueError(msg)

    return round(
        time_value * time_chart[unit_from] * time_chart_inverse[unit_to],
        3,
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(f"{convert_time(3600,'seconds', 'hours') = :,}")
    print(f"{convert_time(360, 'days', 'months') = :,}")
    print(f"{convert_time(360, 'months', 'years') = :,}")
    print(f"{convert_time(1, 'years', 'seconds') = :,}")
