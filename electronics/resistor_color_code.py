"""
标题：使用色环计算 n 环电阻器的阻值

说明：
    电阻器会阻碍电流流动。每个电阻器都有一个表示其阻碍电流能力的阻值，
    单位为 ohm，常用希腊字母 omega 表示：Ω。

    掌握读取方法后，可以从电阻器的色环获知阻值和容差。颜色排列顺序非常重要，
    不同阻值的电阻器具有各自独特的颜色组合。

    电阻器色码是 IEC 60062 定义的国际标准。

    电阻器的色环数量为三至六个，分别表示有效数字、倍乘因子、容差、可靠性和温度
    系数。每类色环中的每种颜色都有对应值，并按从左到右的顺序读取。
    所有电阻器都有有效数字环和倍乘环。三环电阻器从左侧起前两个色环表示有效
    数字，第三个色环表示倍乘因子。

    有效数字 - 电阻器的有效数字环数量可以是两个或三个。
    有效数字环对应的颜色和值 -
    (Black = 0, Brown = 1, Red = 2, Orange = 3, Yellow = 4, Green = 5, Blue = 6,
    Violet = 7, Grey = 8, White = 9)

    倍乘因子 - 电阻器有一个倍乘环，其值与前面色环得到的有效数字相乘。
    倍乘环对应的颜色和值 -
    (Black = 100, Brown = 10^1, Red = 10^2, Orange = 10^3, Yellow = 10^4, Green = 10^5,
    Blue = 10^6, Violet = 10^7, Grey = 10^8, White = 10^9, Gold = 10^-1, Silver = 10^-2)
    注意，倍乘环会使用 Gold 和 Silver，而有效数字环不使用这两种颜色。

    容差 - 容差环并非始终存在，它出现在四环及更多色环的电阻器中，表示阻值可变
    动的百分比。
    容差环对应的颜色和值 -
    (Brown = 1%, Red = 2%, Orange = 0.05%, Yellow = 0.02%, Green = 0.5%,Blue = 0.25%,
    Violet = 0.1%, Grey = 0.01%, Gold = 5%, Silver = 10%)
    未指定颜色时，默认容差为 20%。
    注意，容差环不使用 Black 和 White。

    温度系数 - 以 ppm/K 表示元件阻值随环境温度的变化，存在于六环电阻器中。
    温度系数环对应的颜色和值 -
    (Black = 250 ppm/K, Brown = 100 ppm/K, Red = 50 ppm/K, Orange = 15 ppm/K,
    Yellow = 25 ppm/K, Green = 20 ppm/K, Blue = 10 ppm/K, Violet = 5 ppm/K,
    Grey = 1 ppm/K)
    注意，温度系数环不使用 White、Gold 和 Silver。

来源：
    https://www.calculator.net/resistor-calculator.html
    https://learn.parallax.com/support/reference/resistor-color-codes
    https://byjus.com/physics/resistor-colour-codes/
"""

valid_colors: list = [
    "Black",
    "Brown",
    "Red",
    "Orange",
    "Yellow",
    "Green",
    "Blue",
    "Violet",
    "Grey",
    "White",
    "Gold",
    "Silver",
]

significant_figures_color_values: dict[str, int] = {
    "Black": 0,
    "Brown": 1,
    "Red": 2,
    "Orange": 3,
    "Yellow": 4,
    "Green": 5,
    "Blue": 6,
    "Violet": 7,
    "Grey": 8,
    "White": 9,
}

multiplier_color_values: dict[str, float] = {
    "Black": 10**0,
    "Brown": 10**1,
    "Red": 10**2,
    "Orange": 10**3,
    "Yellow": 10**4,
    "Green": 10**5,
    "Blue": 10**6,
    "Violet": 10**7,
    "Grey": 10**8,
    "White": 10**9,
    "Gold": 10**-1,
    "Silver": 10**-2,
}

tolerance_color_values: dict[str, float] = {
    "Brown": 1,
    "Red": 2,
    "Orange": 0.05,
    "Yellow": 0.02,
    "Green": 0.5,
    "Blue": 0.25,
    "Violet": 0.1,
    "Grey": 0.01,
    "Gold": 5,
    "Silver": 10,
}

temperature_coeffecient_color_values: dict[str, int] = {
    "Black": 250,
    "Brown": 100,
    "Red": 50,
    "Orange": 15,
    "Yellow": 25,
    "Green": 20,
    "Blue": 10,
    "Violet": 5,
    "Grey": 1,
}

band_types: dict[int, dict[str, int]] = {
    3: {"significant": 2, "multiplier": 1},
    4: {"significant": 2, "multiplier": 1, "tolerance": 1},
    5: {"significant": 3, "multiplier": 1, "tolerance": 1},
    6: {"significant": 3, "multiplier": 1, "tolerance": 1, "temp_coeffecient": 1},
}


def get_significant_digits(colors: list) -> str:
    """
    返回颜色对应的数字。输入为包含颜色的列表，返回由数字组成的字符串。

    >>> get_significant_digits(['Black','Blue'])
    '06'

    >>> get_significant_digits(['Aqua','Blue'])
    Traceback (most recent call last):
      ...
    ValueError: Aqua is not a valid color for significant figure bands

    """
    digit = ""
    for color in colors:
        if color not in significant_figures_color_values:
            msg = f"{color} is not a valid color for significant figure bands"
            raise ValueError(msg)
        digit = digit + str(significant_figures_color_values[color])
    return str(digit)


def get_multiplier(color: str) -> float:
    """
    返回颜色对应的倍乘值。输入为颜色，返回倍乘值。

    >>> get_multiplier('Gold')
    0.1

    >>> get_multiplier('Ivory')
    Traceback (most recent call last):
      ...
    ValueError: Ivory is not a valid color for multiplier band

    """
    if color not in multiplier_color_values:
        msg = f"{color} is not a valid color for multiplier band"
        raise ValueError(msg)
    return multiplier_color_values[color]


def get_tolerance(color: str) -> float:
    """
    返回颜色对应的容差值。输入为颜色，返回容差值。

    >>> get_tolerance('Green')
    0.5

    >>> get_tolerance('Indigo')
    Traceback (most recent call last):
      ...
    ValueError: Indigo is not a valid color for tolerance band

    """
    if color not in tolerance_color_values:
        msg = f"{color} is not a valid color for tolerance band"
        raise ValueError(msg)
    return tolerance_color_values[color]


def get_temperature_coeffecient(color: str) -> int:
    """
    返回颜色对应的温度系数值。输入为颜色，返回温度系数值。

    >>> get_temperature_coeffecient('Yellow')
    25

    >>> get_temperature_coeffecient('Cyan')
    Traceback (most recent call last):
      ...
    ValueError: Cyan is not a valid color for temperature coeffecient band

    """
    if color not in temperature_coeffecient_color_values:
        msg = f"{color} is not a valid color for temperature coeffecient band"
        raise ValueError(msg)
    return temperature_coeffecient_color_values[color]


def get_band_type_count(total_number_of_bands: int, type_of_band: str) -> int:
    """
    返回 n 环电阻器中指定类型的色环数量。输入 total_number_of_bands 和
    type_of_band，返回该电阻器中属于指定类型的色环数量。

    >>> get_band_type_count(3,'significant')
    2

    >>> get_band_type_count(2,'significant')
    Traceback (most recent call last):
      ...
    ValueError: 2 is not a valid number of bands

    >>> get_band_type_count(3,'sign')
    Traceback (most recent call last):
      ...
    ValueError: sign is not valid for a 3 band resistor

    >>> get_band_type_count(3,'tolerance')
    Traceback (most recent call last):
      ...
    ValueError: tolerance is not valid for a 3 band resistor

    >>> get_band_type_count(5,'temp_coeffecient')
    Traceback (most recent call last):
      ...
    ValueError: temp_coeffecient is not valid for a 5 band resistor

    """
    if total_number_of_bands not in band_types:
        msg = f"{total_number_of_bands} is not a valid number of bands"
        raise ValueError(msg)
    if type_of_band not in band_types[total_number_of_bands]:
        msg = f"{type_of_band} is not valid for a {total_number_of_bands} band resistor"
        raise ValueError(msg)
    return band_types[total_number_of_bands][type_of_band]


def check_validity(number_of_bands: int, colors: list) -> bool:
    """
    检查给定输入是否有效。输入 number_of_bands 和 colors，有效时返回 True。

    >>> check_validity(3, ["Black","Blue","Orange"])
    True

    >>> check_validity(4, ["Black","Blue","Orange"])
    Traceback (most recent call last):
      ...
    ValueError: Expecting 4 colors, provided 3 colors

    >>> check_validity(3, ["Cyan","Red","Yellow"])
    Traceback (most recent call last):
      ...
    ValueError: Cyan is not a valid color

    """
    if number_of_bands >= 3 and number_of_bands <= 6:
        if number_of_bands == len(colors):
            for color in colors:
                if color not in valid_colors:
                    msg = f"{color} is not a valid color"
                    raise ValueError(msg)
            return True
        else:
            msg = f"Expecting {number_of_bands} colors, provided {len(colors)} colors"
            raise ValueError(msg)
    else:
        msg = "Invalid number of bands. Resistor bands must be 3 to 6"
        raise ValueError(msg)


def calculate_resistance(number_of_bands: int, color_code_list: list) -> dict:
    """
    使用色码计算电阻器的总阻值。输入 number_of_bands 和 color_code_list，
    返回 resistance。

    >>> calculate_resistance(3, ["Black","Blue","Orange"])
    {'resistance': '6000Ω ±20% '}

    >>> calculate_resistance(4, ["Orange","Green","Blue","Gold"])
    {'resistance': '35000000Ω ±5% '}

    >>> calculate_resistance(5, ["Violet","Brown","Grey","Silver","Green"])
    {'resistance': '7.18Ω ±0.5% '}

    >>> calculate_resistance(6, ["Red","Green","Blue","Yellow","Orange","Grey"])
    {'resistance': '2560000Ω ±0.05% 1 ppm/K'}

    >>> calculate_resistance(0, ["Violet","Brown","Grey","Silver","Green"])
    Traceback (most recent call last):
      ...
    ValueError: Invalid number of bands. Resistor bands must be 3 to 6

    >>> calculate_resistance(4, ["Violet","Brown","Grey","Silver","Green"])
    Traceback (most recent call last):
      ...
    ValueError: Expecting 4 colors, provided 5 colors

    >>> calculate_resistance(4, ["Violet","Silver","Brown","Grey"])
    Traceback (most recent call last):
      ...
    ValueError: Silver is not a valid color for significant figure bands

    >>> calculate_resistance(4, ["Violet","Blue","Lime","Grey"])
    Traceback (most recent call last):
      ...
    ValueError: Lime is not a valid color

    """
    is_valid = check_validity(number_of_bands, color_code_list)
    if is_valid:
        number_of_significant_bands = get_band_type_count(
            number_of_bands, "significant"
        )
        significant_colors = color_code_list[:number_of_significant_bands]
        significant_digits = int(get_significant_digits(significant_colors))
        multiplier_color = color_code_list[number_of_significant_bands]
        multiplier = get_multiplier(multiplier_color)
        if number_of_bands == 3:
            tolerance_color = None
        else:
            tolerance_color = color_code_list[number_of_significant_bands + 1]
        tolerance = (
            20 if tolerance_color is None else get_tolerance(str(tolerance_color))
        )
        if number_of_bands != 6:
            temperature_coeffecient_color = None
        else:
            temperature_coeffecient_color = color_code_list[
                number_of_significant_bands + 2
            ]
        temperature_coeffecient = (
            0
            if temperature_coeffecient_color is None
            else get_temperature_coeffecient(str(temperature_coeffecient_color))
        )
        resisitance = significant_digits * multiplier
        if temperature_coeffecient == 0:
            answer = f"{resisitance}Ω ±{tolerance}% "
        else:
            answer = f"{resisitance}Ω ±{tolerance}% {temperature_coeffecient} ppm/K"
        return {"resistance": answer}
    else:
        raise ValueError("Input is invalid")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
