"""
在激光物理学中，“白光腔”（white cell）是一种充当激光束延迟线的反射镜系统。
光束进入腔体，在反射镜之间多次反射，最终离开。

本题所考虑的白光腔是一个椭圆，其方程为
4x^2 + y^2 = 100

顶部对应 -0.01 ≤ x ≤ +0.01 的部分缺失，使光线可以通过该孔进入和离开。
￼￼
本题中的光束从白光腔外的点 (0.0,10.1) 出发，首次在 (1.4,-9.6) 处撞击反射镜。

激光束每次撞击椭圆表面时都遵循通常的反射定律：“入射角等于反射角”。也就是说，
入射光束和反射光束与入射点法线的夹角相同。

左图中的红线表示激光束与白光腔壁最初的两个接触点；蓝线表示第一次反射入射点处
椭圆的切线。

给定椭圆上任意点 (x,y) 处切线的斜率 m 为：m = -4x/y

入射点处的法线与该切线垂直。

右侧动画展示了光束最初的 10 次反射。

光束在离开前会撞击白光腔内表面多少次？
"""

from math import isclose, sqrt


def next_point(
    point_x: float, point_y: float, incoming_gradient: float
) -> tuple[float, float, float]:
    """
    给定激光束以斜率 incoming_gradient 在点 (point_x, point_y) 撞击白光腔内壁，
    返回元组 (x,y,m1)，其中下一接触点为 (x,y)，斜率为 m1。
    >>> next_point(5.0, 0.0, 0.0)
    (-5.0, 0.0, 0.0)
    >>> next_point(5.0, 0.0, -2.0)
    (0.0, -10.0, 2.0)
    """
    # normal_gradient = 光束反射所依据直线的斜率
    # outgoing_gradient = 反射线的斜率
    normal_gradient = point_y / 4 / point_x
    s2 = 2 * normal_gradient / (1 + normal_gradient * normal_gradient)
    c2 = (1 - normal_gradient * normal_gradient) / (
        1 + normal_gradient * normal_gradient
    )
    outgoing_gradient = (s2 - c2 * incoming_gradient) / (c2 + s2 * incoming_gradient)

    # 为找到下一点，求解联立方程：
    # y^2 + 4x^2 = 100
    # y - b = m * (x - a)
    # ==> A x^2 + B x + C = 0
    quadratic_term = outgoing_gradient**2 + 4
    linear_term = 2 * outgoing_gradient * (point_y - outgoing_gradient * point_x)
    constant_term = (point_y - outgoing_gradient * point_x) ** 2 - 100

    x_minus = (
        -linear_term - sqrt(linear_term**2 - 4 * quadratic_term * constant_term)
    ) / (2 * quadratic_term)
    x_plus = (
        -linear_term + sqrt(linear_term**2 - 4 * quadratic_term * constant_term)
    ) / (2 * quadratic_term)

    # 有两个解，其中一个是输入点
    next_x = x_minus if isclose(x_plus, point_x) else x_plus
    next_y = point_y + outgoing_gradient * (next_x - point_x)

    return next_x, next_y, outgoing_gradient


def solution(first_x_coord: float = 1.4, first_y_coord: float = -9.6) -> int:
    """
    返回光束离开前撞击腔体内壁的次数。
    >>> solution(0.00001,-10)
    1
    >>> solution(5, 0)
    287
    """
    num_reflections: int = 0
    point_x: float = first_x_coord
    point_y: float = first_y_coord
    gradient: float = (10.1 - point_y) / (0.0 - point_x)

    while not (-0.01 <= point_x <= 0.01 and point_y > 0):
        point_x, point_y, gradient = next_point(point_x, point_y, gradient)
        num_reflections += 1

    return num_reflections


if __name__ == "__main__":
    print(f"{solution() = }")
