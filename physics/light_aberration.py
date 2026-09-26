"""
标题：计算光行差（天文学）

说明：
    以下算法使用狭义相对论计算天文光行差。

"""

from math import atan, sqrt, tan


def get_aberration_angle(angle_rest: float, velocity_over_c: float) -> float:
    """
    本方法计算天文光行差。
    静止参考系中的角度 'angle_rest' 以弧度 [rad] 给出，范围为 (-pi, pi)。
    观察者相对于发光物体的速度用 'velocity_over_c' 表示，即该速度与光速 c
    的比值，范围为 (0, 1)。

    https://en.wikipedia.org/wiki/Aberration_(astronomy)

    tan(phi/2) = sqrt((1 - v/c)/(1 + v/c)) * tan(theta/2)

    其中 v 为相对速度，phi 为相对于速度矢量的观测角（受光行差影响），
    theta 为速度趋于 0 时的观测角。

    示例：
    >>> get_aberration_angle(0.2, 0.1)
    0.18102
    >>> get_aberration_angle(0.2, 0)
    0.2
    >>> get_aberration_angle(0, 0.2)
    0.0
    >>> get_aberration_angle(-1.5707963267948966, 0.7)
    -0.7954
    """

    factor = sqrt((1 - velocity_over_c) / (1 + velocity_over_c))
    angle_ab = 2 * atan(factor * tan(angle_rest / 2))

    return round(angle_ab, 5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
