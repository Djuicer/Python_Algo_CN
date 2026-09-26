import math

"""
使用马吕斯定律，根据初始光强和偏振片与轴之间的夹角计算透过偏振片的光强。

说明：马吕斯定律以 Étienne-Louis Malus 命名。将理想偏振片置于偏振光束中时，
透射光的辐照度 I 为：
 I=I'cos²θ
其中 I' 为初始光强，θ 为光的初始偏振方向与偏振片轴之间的夹角。非偏振光束
可视为包含各个可能角度、均匀混合的线偏振光。由于 cos²θ 的平均值为 1/2，
透射系数为：
I/I' = 1/2
实际中，一部分光会在偏振片中损失，因此真实透射率略低；Polaroid 型偏振片
约为 38%，某些双折射棱镜型偏振片则明显更高（>49.9%）。若前后放置两个
偏振片（第二个通常称为检偏器），两偏振轴的夹角就是马吕斯定律中的 θ。
两轴正交时称为正交偏振，理论上没有光透过；但实际偏振片并不完美，透射率
不会恰好为零。若在正交偏振片之间放置透明物体，样品中的偏振效应（如双折射）
会表现为透射率增加，偏振测量法据此测量样品的旋光性。真实偏振片也不能完全
阻挡垂直于偏振轴的偏振分量；不需要分量与需要分量的透射率之比称为消光比，
Polaroid 约为 1:500，Glan-Taylor 棱镜偏振片约为 1:106。

参考资料："https://en.wikipedia.org/wiki/Polarizer#Malus's_law_and_other_properties"
"""


def malus_law(initial_intensity: float, angle: float) -> float:
    """
    >>> round(malus_law(10,45),2)
    5.0
    >>> round(malus_law(100,60),2)
    25.0
    >>> round(malus_law(50,150),2)
    37.5
    >>> round(malus_law(75,270),2)
    0.0
    >>> round(malus_law(10,-900),2)
    Traceback (most recent call last):
        ...
    ValueError: In Malus Law, the angle is in the range 0-360 degrees
    >>> round(malus_law(10,900),2)
    Traceback (most recent call last):
        ...
    ValueError: In Malus Law, the angle is in the range 0-360 degrees
    >>> round(malus_law(-100,900),2)
    Traceback (most recent call last):
        ...
    ValueError: The value of intensity cannot be negative
    >>> round(malus_law(100,180),2)
    100.0
    >>> round(malus_law(100,360),2)
    100.0
    """

    if initial_intensity < 0:
        raise ValueError("The value of intensity cannot be negative")
        # 处理初始光强为负值的情况
    if angle < 0 or angle > 360:
        raise ValueError("In Malus Law, the angle is in the range 0-360 degrees")
        # 处理超出允许范围的值
    return initial_intensity * (math.cos(math.radians(angle)) ** 2)


if __name__ == "__main__":
    import doctest

    doctest.testmod(name="malus_law")
