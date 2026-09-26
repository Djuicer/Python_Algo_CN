"""
胡克定律指出，拉伸或压缩弹簧所需的力与其伸长量或压缩量成正比。

    F = -k * x

其中：
    F = 施加的力（单位：牛顿）
    k = 弹簧常数（单位：牛顿每米，N/m）
    x = 相对于平衡位置的位移（单位：米）

负号表示该力为恢复力（方向与位移相反）。

参考资料：https://en.wikipedia.org/wiki/Hooke%27s_law
"""


def hookes_law(spring_constant: float, displacement: float) -> float:
    """
    使用胡克定律计算弹簧的恢复力。

    参数：
        spring_constant: 弹簧刚度，单位为 N/m（必须为正数）
        displacement: 伸长量或压缩量，单位为米

    返回：
        恢复力，单位为牛顿（负值表示方向与位移相反）

    >>> hookes_law(spring_constant=50, displacement=0.1)
    -5.0
    >>> hookes_law(spring_constant=100, displacement=0.5)
    -50.0
    >>> hookes_law(spring_constant=200, displacement=-0.2)
    40.0
    >>> hookes_law(spring_constant=0, displacement=0.1)
    Traceback (most recent call last):
        ...
    ValueError: Spring constant must be positive.
    >>> hookes_law(spring_constant=-10, displacement=0.1)
    Traceback (most recent call last):
        ...
    ValueError: Spring constant must be positive.
    """
    if spring_constant <= 0:
        raise ValueError("Spring constant must be positive.")
    return -spring_constant * displacement


if __name__ == "__main__":
    import doctest

    doctest.testmod()
