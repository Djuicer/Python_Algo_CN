"""
标题：计算雷诺数以判断流动类型（层流或湍流）

雷诺数是用于判断管内流动属于层流还是湍流的无量纲量，定义为惯性力与黏性力
之比。

R = 惯性力 / 黏性力
R = (p * V * D)/μ

其中：
p = 流体密度 (Kg/m^3)
D = 流体所经管道的直径 (m)
V = 流体流速 (m/s)
μ = 流体黏度 (Ns/m^2)

计算出的雷诺数较高（大于 2000）时，管内流动称为湍流；雷诺数较低（小于
2000）时称为层流。这些数值可作为判据，不过通常按范围分类：雷诺数低于
1100 为层流，高于 2200 为湍流。层流中流体沿规则路径平稳流动；湍流则不
平稳，沿不规则路径运动并伴随大量混合。

参考资料：https://byjus.com/physics/reynolds-number/
"""


def reynolds_number(
    density: float, velocity: float, diameter: float, viscosity: float
) -> float:
    """
    >>> reynolds_number(900, 2.5, 0.05, 0.4)
    281.25
    >>> reynolds_number(450, 3.86, 0.078, 0.23)
    589.0695652173912
    >>> reynolds_number(234, -4.5, 0.3, 0.44)
    717.9545454545454
    >>> reynolds_number(-90, 2, 0.045, 1)
    Traceback (most recent call last):
        ...
    ValueError: please ensure that density, diameter and viscosity are positive
    >>> reynolds_number(0, 2, -0.4, -2)
    Traceback (most recent call last):
        ...
    ValueError: please ensure that density, diameter and viscosity are positive
    """

    if density <= 0 or diameter <= 0 or viscosity <= 0:
        raise ValueError(
            "please ensure that density, diameter and viscosity are positive"
        )
    return (density * abs(velocity) * diameter) / viscosity


if __name__ == "__main__":
    import doctest

    doctest.testmod()
