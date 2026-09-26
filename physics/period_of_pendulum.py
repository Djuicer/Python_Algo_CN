"""
标题：计算单摆周期

单摆是一种摆动或振荡的机械系统。它由质量为 m 的小摆锤和长度为 L 的细线
组成，细线上端固定在支架上。摆锤在竖直平面内运动，主要受重力驱动。
摆动周期取决于细线长度和振幅（最大角度）。当振幅较小时，可以忽略振幅
的影响。需要注意，周期与摆锤质量无关。

对于小振幅，单摆周期可由以下近似式给出：
T ≈ 2π * √(L / g)

其中：
L = 悬挂摆锤的细线长度 (m)
g = 重力加速度（约为 9.8 m/s²）

参考资料：https://byjus.com/jee/simple-pendulum/
"""

from math import pi

from scipy.constants import g


def period_of_pendulum(length: float) -> float:
    """
    >>> period_of_pendulum(1.23)
    2.2252155506257845
    >>> period_of_pendulum(2.37)
    3.0888278441908574
    >>> period_of_pendulum(5.63)
    4.76073193364765
    >>> period_of_pendulum(-12)
    Traceback (most recent call last):
        ...
    ValueError: The length should be non-negative
    >>> period_of_pendulum(0)
    0.0
    """
    if length < 0:
        raise ValueError("The length should be non-negative")
    return 2 * pi * (length / g) ** 0.5


if __name__ == "__main__":
    import doctest

    doctest.testmod()
