"""
说明：向心力是作用于曲线运动物体、方向指向旋转轴或曲率中心的力。

向心力的单位是牛顿。

向心力的方向始终与物体位移方向垂直。根据牛顿第二定律，沿圆周运动的物体
所受向心力始终指向圆心。向心力等于质量（kg）与切向速度（m/s）平方的
乘积除以半径（m），因此切向速度加倍时，向心力变为四倍。数学表达式为：
F = mv²/r
其中 F 为向心力，m 为物体质量，v 为物体速度，r 为半径。

参考资料：https://byjus.com/physics/centripetal-and-centrifugal-force/
"""


def centripetal(mass: float, velocity: float, radius: float) -> float:
    """
    向心力公式为：(m*v*v)/r

    >>> round(centripetal(15.5,-30,10),2)
    1395.0
    >>> round(centripetal(10,15,5),2)
    450.0
    >>> round(centripetal(20,-50,15),2)
    3333.33
    >>> round(centripetal(12.25,40,25),2)
    784.0
    >>> round(centripetal(50,100,50),2)
    10000.0
    """
    if mass < 0:
        raise ValueError("The mass of the body cannot be negative")
    if radius <= 0:
        raise ValueError("The radius is always a positive non zero integer")
    return (mass * (velocity) ** 2) / radius


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
