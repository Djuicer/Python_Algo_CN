"""
________________________________________________________________________________________
热力学第一定律指出，当能量以功、热或物质的形式进入或离开系统时，系统内能
依照能量守恒定律发生变化。由此也可知，在与外界隔离的系统中，即使内部发生
变化，各种形式的能量总和仍保持不变，因为能量既不会产生也不会消灭。

计算公式为：
 --------------
 | Q = ΔU + W |
 --------------

Q = 系统吸收或释放的热量。
ΔU = 系统内能的变化量。
W = 系统对外界所做的功。

注意：所有单位必须彼此一致。
（说明改编自 https://en.wikipedia.org/wiki/Laws_of_thermodynamics ）
"""


def __check_args(argument: float) -> None:
    """
    检查参数是否有效。
    >>> __check_args("50")
    Traceback (most recent call last):
        ...
    TypeError: Invalid argument. Should be an integer or float.
    """

    # 确保实例有效
    if not isinstance(argument, (int, float)):
        raise TypeError("Invalid argument. Should be an integer or float.")


def __categorize_system(argument_value: float, argument_name: str) -> None:
    """
    根据所做的功、吸收或释放的热量以及内能变化对系统进行分类。
    >>> __categorize_system(0, "work")
    The system is isochoric (constant volume).
    >>> __categorize_system(50, "heat")
    The system is endothermic (absorbing heat).
    >>> __categorize_system(-20, "internal_energy_variation")
    The internal energy of the system is decreasing. It cooling down.
    >>> __categorize_system(10, "invalid")
    Traceback (most recent call last):
        ...
    ValueError: Should be 'work', 'heat', or 'internal_energy_variation'.
    """

    if argument_name == "work":
        if argument_value == 0:
            print("The system is isochoric (constant volume).")
        elif argument_value > 0:
            print("The system is expanding.")
        elif argument_value < 0:
            print("The system is compressing.")

    elif argument_name == "heat":
        if argument_value == 0:
            print("The system is adiabatic (no heat exchange).")
        elif argument_value > 0:
            print("The system is endothermic (absorbing heat).")
        elif argument_value < 0:
            print("The system is exothermic (releasing heat).")

    elif argument_name == "internal_energy_variation":
        if argument_value == 0:
            print("The system is isothermic (constant internal energy)")
        elif argument_value > 0:
            print("The internal energy of the system is increasing. It heating up.")
        elif argument_value < 0:
            print("The internal energy of the system is decreasing. It cooling down.")

    else:
        raise ValueError("Should be 'work', 'heat', or 'internal_energy_variation'.")


def work(heat: float, internal_energy_variation: float) -> float:
    """
    >>> work(50.0, -20.0)
    The system is endothermic (absorbing heat).
    The internal energy of the system is decreasing. It cooling down.
    The system is expanding.
    70.0
    >>> work(50.0, 50.0)
    The system is endothermic (absorbing heat).
    The internal energy of the system is increasing. It heating up.
    The system is isochoric (constant volume).
    0.0
    >>> work(-50.0, 20.0)
    The system is exothermic (releasing heat).
    The internal energy of the system is increasing. It heating up.
    The system is compressing.
    -70.0
    """
    __check_args(heat)
    __check_args(internal_energy_variation)

    __categorize_system(heat, "heat")
    __categorize_system(internal_energy_variation, "internal_energy_variation")

    work = heat - internal_energy_variation
    __categorize_system(work, "work")
    return round(work, 1)


def heat(internal_energy_variation: float, work: float) -> float:
    """
    >>> heat(-20.0, 30.0)
    The internal energy of the system is decreasing. It cooling down.
    The system is expanding.
    The system is endothermic (absorbing heat).
    10.0
    >>> heat(50.0, 0.0)
    The internal energy of the system is increasing. It heating up.
    The system is isochoric (constant volume).
    The system is endothermic (absorbing heat).
    50.0
    >>> heat(20.0, -70.0)
    The internal energy of the system is increasing. It heating up.
    The system is compressing.
    The system is exothermic (releasing heat).
    -50.0
    """
    __check_args(internal_energy_variation)
    __check_args(work)

    __categorize_system(internal_energy_variation, "internal_energy_variation")
    __categorize_system(work, "work")

    heat = round(internal_energy_variation + work, 1)
    __categorize_system(heat, "heat")
    return heat


def internal_energy_variation(heat: float, work: float) -> float:
    """
    >>> internal_energy_variation(50.0, 30.0)
    The system is endothermic (absorbing heat).
    The system is expanding.
    The internal energy of the system is increasing. It heating up.
    20.0
    >>> internal_energy_variation(50.0, 0.0)
    The system is endothermic (absorbing heat).
    The system is isochoric (constant volume).
    The internal energy of the system is increasing. It heating up.
    50.0
    >>> internal_energy_variation(-50.0, -70.0)
    The system is exothermic (releasing heat).
    The system is compressing.
    The internal energy of the system is increasing. It heating up.
    20.0
    """
    __check_args(heat)
    __check_args(work)

    __categorize_system(heat, "heat")
    __categorize_system(work, "work")

    internal_energy_variation = round(heat - work, 1)
    __categorize_system(internal_energy_variation, "internal_energy_variation")
    return internal_energy_variation


if __name__ == "__main__":
    from doctest import testmod

    testmod()
