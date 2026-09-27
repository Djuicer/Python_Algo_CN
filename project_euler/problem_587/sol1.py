"""
Project Euler Problem 587: https://projecteuler.net/problem=587

如下面左图所示，在一个圆的外面画一个正方形。
我们将蓝色阴影区域称为 L 形区域。
如右图所示，从正方形的左下角向右上角画一条直线。
我们将橙色阴影区域称为凹三角形。

显然，凹三角形恰好占 L 形区域的一半。

将两个圆水平相邻放置，在两个圆的外面画一个矩形，
并如图所示从左下角向右上角画一条直线。

此时凹三角形约占 L 形区域的 36.46%。

如果将 n 个圆水平相邻放置，在这 n 个圆的外面画一个矩形，
并从左下角向右上角画一条直线，
可以证明，使凹三角形占 L 形区域的比例小于 10% 的最小 n 值为 n = 15。

使凹三角形占 L 形区域的比例小于 0.1% 的最小 n 值是多少？
"""

from itertools import count
from math import asin, pi, sqrt


def circle_bottom_arc_integral(point: float) -> float:
    """
    返回圆的下圆弧 y = 1 / 2 - sqrt(1 / 4 - (x - 1 / 2) ^ 2) 的积分。

    >>> circle_bottom_arc_integral(0)
    0.39269908169872414

    >>> circle_bottom_arc_integral(1 / 2)
    0.44634954084936207

    >>> circle_bottom_arc_integral(1)
    0.5
    """

    return (
        (1 - 2 * point) * sqrt(point - point**2) + 2 * point + asin(sqrt(1 - point))
    ) / 4


def concave_triangle_area(circles_number: int) -> float:
    """
    返回凹三角形的面积。

    >>> concave_triangle_area(1)
    0.026825229575318944

    >>> concave_triangle_area(2)
    0.01956236140083944
    """

    intersection_y = (circles_number + 1 - sqrt(2 * circles_number)) / (
        2 * (circles_number**2 + 1)
    )
    intersection_x = circles_number * intersection_y

    triangle_area = intersection_x * intersection_y / 2
    concave_region_area = circle_bottom_arc_integral(
        1 / 2
    ) - circle_bottom_arc_integral(intersection_x)

    return triangle_area + concave_region_area


def solution(fraction: float = 1 / 1000) -> int:
    """
    返回使凹三角形占 L 形区域的比例小于 fraction 的最小 n 值。

    >>> solution(1 / 10)
    15
    """

    l_section_area = (1 - pi / 4) / 4

    for n in count(1):
        if concave_triangle_area(n) / l_section_area < fraction:
            return n

    return -1


if __name__ == "__main__":
    print(f"{solution() = }")
