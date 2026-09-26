"""
库仑定律指出，两个点电荷之间静电吸引力或排斥力的大小与电荷量绝对值的
乘积成正比，与它们之间距离的平方成反比。

F = k * q1 * q2 / r^2

k 为库仑常数，等于 1/(4π*ε0)
q1 为第一个物体的电荷量 (C)
q2 为第二个物体的电荷量 (C)
r 为两个带电物体之间的距离 (m)

参考资料：https://en.wikipedia.org/wiki/Coulomb%27s_law
"""


def coulombs_law(q1: float, q2: float, radius: float) -> float:
    """
    计算两个点电荷之间的静电吸引力或排斥力。

    >>> coulombs_law(15.5, 20, 15)
    12382849136.06
    >>> coulombs_law(1, 15, 5)
    5392531075.38
    >>> coulombs_law(20, -50, 15)
    -39944674632.44
    >>> coulombs_law(-5, -8, 10)
    3595020716.92
    >>> coulombs_law(50, 100, 50)
    17975103584.6
    """
    if radius <= 0:
        raise ValueError("The radius is always a positive number")
    return round(((8.9875517923 * 10**9) * q1 * q2) / (radius**2), 2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
