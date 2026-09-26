"""
斯涅尔定律——折射角计算。

使用斯涅尔定律 n1 * sin(theta1) = n2 * sin(theta2)，计算光在两种介质之间
传播时的折射角。

参考资料：https://en.wikipedia.org/wiki/Snell%27s_law
"""

import math


def calculate_refraction_angle(
    index_of_refraction_1: float,
    index_of_refraction_2: float,
    incident_angle_degrees: float,
) -> float:
    """
    计算光从一种介质进入另一种介质时的折射角。对于给定的两种介质，入射角
    与折射角的正弦之比等于第二种介质相对于第一种介质的折射率，即两种介质
    的折射率之比；等价地，也等于两种介质中相速度之比。


    公式：n1 * sin(theta1) = n2 * sin(theta2)
    或    ：(sin(theta1) / sin(theta2)) = (n2 / n1)
    其中：
        n1 = 第一种介质的折射率
        n2 = 第二种介质的折射率
        theta1 = 入射角
        theta2 = 折射角

    注意：当光从光密介质进入光疏介质，且入射角超过临界角时，会发生全反射
    （Total Internal Reflection, TIR），此时无法发生折射。

    来源：
        - https://en.wikipedia.org/wiki/Snell%27s_law

    -----------------------------------------------------------------------------

    >>> calculate_refraction_angle(1.0, 1.33, 60.0)
    40.63
    >>> calculate_refraction_angle(2.0, 1.0, 30.0)
    90.0
    >>> calculate_refraction_angle(1.33, 1.0, 60.0)
    Traceback (most recent call last):
        ...
    ValueError: Invalid physical inputs: ratio cannot be outside [-1, 1].
    >>> calculate_refraction_angle(-1.33, 1.0, 60.0)
    Traceback (most recent call last):
        ...
    ValueError: Invalid physical inputs: ratio cannot be outside [-1, 1].
    >>>
    """

    incident_angle_radians = math.radians(incident_angle_degrees)
    refraction_sine = (index_of_refraction_1 / index_of_refraction_2) * math.sin(
        incident_angle_radians
    )

    # 若正弦值近似为 1.0 或 -1.0，则处于临界角
    # 使用 math.isclose 处理浮点精度误差
    if math.isclose(refraction_sine, 1.0):
        return 90.0
    if math.isclose(refraction_sine, -1.0):
        return -90.0

    if not -1 <= refraction_sine <= 1:
        raise ValueError("Invalid physical inputs: ratio cannot be outside [-1, 1].")

    refraction_angle = round(math.degrees(math.asin(refraction_sine)), 2)
    return refraction_angle
