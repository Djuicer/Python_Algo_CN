"""
Author Anurag Kumar | anuragkumarak95@gmail.com | git/anuragkumarak95

使用递归生成分形的简单示例。

什么是谢尔宾斯基三角形？
    谢尔宾斯基三角形（Sierpiński Triangle，有时拼作 Sierpinski）也称谢尔宾斯基
垫片或谢尔宾斯基筛，是整体呈等边三角形、递归细分为更小等边三角形的分形吸引
不动集。它最初被构造为曲线，是自相似集的基本示例之一；也就是说，这种数学
生成的图案在任意放大或缩小尺度下都可以重现。它以波兰数学家 Wacław Sierpiński
命名，但早在其研究前数百年就已作为装饰图案出现。


Usage: python sierpinski_triangle.py <int:depth_for_fractal>

致谢：
    上述说明取自
    https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle
    此代码改编自
    https://www.riannetrujillo.com/blog/python-fractal/
"""

import sys
import turtle


def get_mid(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """
    求两点的中点。

    >>> get_mid((0, 0), (2, 2))
    (1.0, 1.0)
    >>> get_mid((-3, -3), (3, 3))
    (0.0, 0.0)
    >>> get_mid((1, 0), (3, 2))
    (2.0, 1.0)
    >>> get_mid((0, 0), (1, 1))
    (0.5, 0.5)
    >>> get_mid((0, 0), (0, 0))
    (0.0, 0.0)
    """
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2


def triangle(
    vertex1: tuple[float, float],
    vertex2: tuple[float, float],
    vertex3: tuple[float, float],
    depth: int,
) -> None:
    """
    根据三角形顶点和递归深度递归绘制谢尔宾斯基三角形。
    """
    my_pen.up()
    my_pen.goto(vertex1[0], vertex1[1])
    my_pen.down()
    my_pen.goto(vertex2[0], vertex2[1])
    my_pen.goto(vertex3[0], vertex3[1])
    my_pen.goto(vertex1[0], vertex1[1])

    if depth == 0:
        return

    triangle(vertex1, get_mid(vertex1, vertex2), get_mid(vertex1, vertex3), depth - 1)
    triangle(vertex2, get_mid(vertex1, vertex2), get_mid(vertex2, vertex3), depth - 1)
    triangle(vertex3, get_mid(vertex3, vertex2), get_mid(vertex1, vertex3), depth - 1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError(
            "Correct format for using this script: "
            "python fractals.py <int:depth_for_fractal>"
        )
    my_pen = turtle.Turtle()
    my_pen.ht()
    my_pen.speed(5)
    my_pen.pencolor("red")

    vertices = [(-175, -125), (0, 175), (175, -125)]  # 三角形的顶点
    triangle(vertices[0], vertices[1], vertices[2], int(sys.argv[1]))
    turtle.Screen().exitonclick()
