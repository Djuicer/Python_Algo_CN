"""
标题：格雷厄姆逸出定律

说明：格雷厄姆逸出定律指出，气体逸出速率与其粒子摩尔质量的平方根成反比：

r1/r2 = sqrt(m2/m1)

r1 = 第一种气体的逸出速率。
r2 = 第二种气体的逸出速率。
m1 = 第一种气体的摩尔质量。
m2 = 第二种气体的摩尔质量。

（说明改编自 https://en.wikipedia.org/wiki/Graham%27s_law）
"""

from math import pow, sqrt  # noqa: A004


def validate(*values: float) -> bool:
    """
    输入参数：
    -----------------
    effusion_rate_1: 第一种气体的逸出速率 (m^2/s、mm^2/s 等)
    effusion_rate_2: 第二种气体的逸出速率 (m^2/s、mm^2/s 等)
    molar_mass_1: 第一种气体的摩尔质量 (g/mol、kg/kmol 等)
    molar_mass_2: 第二种气体的摩尔质量 (g/mol、kg/kmol 等)

    返回：
    --------
    >>> validate(2.016, 4.002)
    True
    >>> validate(-2.016, 4.002)
    False
    >>> validate()
    False
    """
    result = len(values) > 0 and all(value > 0.0 for value in values)
    return result


def effusion_ratio(molar_mass_1: float, molar_mass_2: float) -> float | ValueError:
    """
    输入参数：
    -----------------
    molar_mass_1: 第一种气体的摩尔质量 (g/mol、kg/kmol 等)
    molar_mass_2: 第二种气体的摩尔质量 (g/mol、kg/kmol 等)

    返回：
    --------
    >>> effusion_ratio(2.016, 4.002)
    1.408943
    >>> effusion_ratio(-2.016, 4.002)
    ValueError('Input Error: Molar mass values must greater than 0.')
    >>> effusion_ratio(2.016)
    Traceback (most recent call last):
      ...
    TypeError: effusion_ratio() missing 1 required positional argument: 'molar_mass_2'
    """
    return (
        round(sqrt(molar_mass_2 / molar_mass_1), 6)
        if validate(molar_mass_1, molar_mass_2)
        else ValueError("Input Error: Molar mass values must greater than 0.")
    )


def first_effusion_rate(
    effusion_rate: float, molar_mass_1: float, molar_mass_2: float
) -> float | ValueError:
    """
    输入参数：
    -----------------
    effusion_rate: 第二种气体的逸出速率 (m^2/s、mm^2/s 等)
    molar_mass_1: 第一种气体的摩尔质量 (g/mol、kg/kmol 等)
    molar_mass_2: 第二种气体的摩尔质量 (g/mol、kg/kmol 等)

    返回：
    --------
    >>> first_effusion_rate(1, 2.016, 4.002)
    1.408943
    >>> first_effusion_rate(-1, 2.016, 4.002)
    ValueError('Input Error: Molar mass and effusion rate values must greater than 0.')
    >>> first_effusion_rate(1)
    Traceback (most recent call last):
      ...
    TypeError: first_effusion_rate() missing 2 required positional arguments: \
'molar_mass_1' and 'molar_mass_2'
    >>> first_effusion_rate(1, 2.016)
    Traceback (most recent call last):
      ...
    TypeError: first_effusion_rate() missing 1 required positional argument: \
'molar_mass_2'
    """
    return (
        round(effusion_rate * sqrt(molar_mass_2 / molar_mass_1), 6)
        if validate(effusion_rate, molar_mass_1, molar_mass_2)
        else ValueError(
            "Input Error: Molar mass and effusion rate values must greater than 0."
        )
    )


def second_effusion_rate(
    effusion_rate: float, molar_mass_1: float, molar_mass_2: float
) -> float | ValueError:
    """
    输入参数：
    -----------------
    effusion_rate: 第二种气体的逸出速率 (m^2/s、mm^2/s 等)
    molar_mass_1: 第一种气体的摩尔质量 (g/mol、kg/kmol 等)
    molar_mass_2: 第二种气体的摩尔质量 (g/mol、kg/kmol 等)

    返回：
    --------
    >>> second_effusion_rate(1, 2.016, 4.002)
    0.709752
    >>> second_effusion_rate(-1, 2.016, 4.002)
    ValueError('Input Error: Molar mass and effusion rate values must greater than 0.')
    >>> second_effusion_rate(1)
    Traceback (most recent call last):
      ...
    TypeError: second_effusion_rate() missing 2 required positional arguments: \
'molar_mass_1' and 'molar_mass_2'
    >>> second_effusion_rate(1, 2.016)
    Traceback (most recent call last):
      ...
    TypeError: second_effusion_rate() missing 1 required positional argument: \
'molar_mass_2'
    """
    return (
        round(effusion_rate / sqrt(molar_mass_2 / molar_mass_1), 6)
        if validate(effusion_rate, molar_mass_1, molar_mass_2)
        else ValueError(
            "Input Error: Molar mass and effusion rate values must greater than 0."
        )
    )


def first_molar_mass(
    molar_mass: float, effusion_rate_1: float, effusion_rate_2: float
) -> float | ValueError:
    """
    输入参数：
    -----------------
    molar_mass: 第一种气体的摩尔质量 (g/mol、kg/kmol 等)
    effusion_rate_1: 第一种气体的逸出速率 (m^2/s、mm^2/s 等)
    effusion_rate_2: 第二种气体的逸出速率 (m^2/s、mm^2/s 等)

    返回：
    --------
    >>> first_molar_mass(2, 1.408943, 0.709752)
    0.507524
    >>> first_molar_mass(-1, 2.016, 4.002)
    ValueError('Input Error: Molar mass and effusion rate values must greater than 0.')
    >>> first_molar_mass(1)
    Traceback (most recent call last):
      ...
    TypeError: first_molar_mass() missing 2 required positional arguments: \
'effusion_rate_1' and 'effusion_rate_2'
    >>> first_molar_mass(1, 2.016)
    Traceback (most recent call last):
      ...
    TypeError: first_molar_mass() missing 1 required positional argument: \
'effusion_rate_2'
    """
    return (
        round(molar_mass / pow(effusion_rate_1 / effusion_rate_2, 2), 6)
        if validate(molar_mass, effusion_rate_1, effusion_rate_2)
        else ValueError(
            "Input Error: Molar mass and effusion rate values must greater than 0."
        )
    )


def second_molar_mass(
    molar_mass: float, effusion_rate_1: float, effusion_rate_2: float
) -> float | ValueError:
    """
    输入参数：
    -----------------
    molar_mass: 第一种气体的摩尔质量 (g/mol、kg/kmol 等)
    effusion_rate_1: 第一种气体的逸出速率 (m^2/s、mm^2/s 等)
    effusion_rate_2: 第二种气体的逸出速率 (m^2/s、mm^2/s 等)

    返回：
    --------
    >>> second_molar_mass(2, 1.408943, 0.709752)
    1.970351
    >>> second_molar_mass(-2, 1.408943, 0.709752)
    ValueError('Input Error: Molar mass and effusion rate values must greater than 0.')
    >>> second_molar_mass(1)
    Traceback (most recent call last):
      ...
    TypeError: second_molar_mass() missing 2 required positional arguments: \
'effusion_rate_1' and 'effusion_rate_2'
    >>> second_molar_mass(1, 2.016)
    Traceback (most recent call last):
      ...
    TypeError: second_molar_mass() missing 1 required positional argument: \
'effusion_rate_2'
    """
    return (
        round(pow(effusion_rate_1 / effusion_rate_2, 2) / molar_mass, 6)
        if validate(molar_mass, effusion_rate_1, effusion_rate_2)
        else ValueError(
            "Input Error: Molar mass and effusion rate values must greater than 0."
        )
    )
