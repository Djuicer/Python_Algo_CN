"""
降雨强度
==================
本模块包含根据给定持续时间和重现期计算降雨事件强度的函数。

本函数使用 Sherman 强度－历时－频率曲线。

参考资料
----------
- Aparicio, F. (1997): Fundamentos de Hidrología de Superficie.
    Balderas, México, Limusa. 303 p.
- https://en.wikipedia.org/wiki/Intensity-duration-frequency_curve
"""


def rainfall_intensity(
    coefficient_k: float,
    coefficient_a: float,
    coefficient_b: float,
    coefficient_c: float,
    return_period: float,
    duration: float,
) -> float:
    """
    根据给定持续时间和重现期计算降雨事件强度，计算基于 Sherman
    强度－历时－频率曲线：

    I = k * T^a / (D + b)^c

    其中：
        I = 降雨事件强度 [mm/h]
        k, a, b, c = 通过统计分布拟合得到的系数
        T = 重现期，单位为年
        D = 降雨事件持续时间，单位为分钟

    参数
    ----------
    coefficient_k : float
        通过统计分布拟合得到的系数。
    coefficient_a : float
        通过统计分布拟合得到的系数。
    coefficient_b : float
        通过统计分布拟合得到的系数。
    coefficient_c : float
        通过统计分布拟合得到的系数。
    return_period : float
        重现期，单位为年。
    duration : float
        降雨事件持续时间，单位为分钟。

    返回
    -------
    intensity : float
        降雨事件强度，单位为 mm/h。

    异常
    ------
    ValueError
        任一参数不是正数时抛出。

    示例
    --------

    >>> rainfall_intensity(1000, 0.2, 11.6, 0.81, 10, 60)
    49.83339231138578

    >>> rainfall_intensity(1000, 0.2, 11.6, 0.81, 10, 30)
    77.36319588106228

    >>> rainfall_intensity(1000, 0.2, 11.6, 0.81, 5, 60)
    43.382487747633625

    >>> rainfall_intensity(0, 0.2, 11.6, 0.81, 10, 60)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    >>> rainfall_intensity(1000, -0.2, 11.6, 0.81, 10, 60)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    >>> rainfall_intensity(1000, 0.2, -11.6, 0.81, 10, 60)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    >>> rainfall_intensity(1000, 0.2, 11.6, -0.81, 10, 60)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    >>> rainfall_intensity(1000, 0, 11.6, 0.81, 10, 60)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    >>> rainfall_intensity(1000, 0.2, 0, 0.81, 10, 60)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    >>> rainfall_intensity(1000, 0.2, 11.6, 0, 10, 60)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    >>> rainfall_intensity(0, 0.2, 11.6, 0.81, 10, 60)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    >>> rainfall_intensity(1000, 0.2, 11.6, 0.81, 0, 60)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    >>> rainfall_intensity(1000, 0.2, 11.6, 0.81, 10, 0)
    Traceback (most recent call last):
    ...
    ValueError: All parameters must be positive.

    """
    if (
        coefficient_k <= 0
        or coefficient_a <= 0
        or coefficient_b <= 0
        or coefficient_c <= 0
        or return_period <= 0
        or duration <= 0
    ):
        raise ValueError("All parameters must be positive.")
    intensity = (coefficient_k * (return_period**coefficient_a)) / (
        (duration + coefficient_b) ** coefficient_c
    )
    return intensity


if __name__ == "__main__":
    import doctest

    doctest.testmod()
