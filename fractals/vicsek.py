"""Authors Bastien Capiaux & Mehdi Oudghiri

维切克分形（Vicsek Fractal）算法是一种递归算法，用于创建称为维切克分形或维切克
方形的图案。它基于自相似概念，每一递归层级的图案都与整体图案相似。该算法将
正方形分为 9 个相等的小正方形，移除中心正方形，然后对剩余 8 个正方形重复此
过程，最终得到具有自相似性的方形轮廓，其中包含更小的正方形。

来源：https://en.wikipedia.org/wiki/Vicsek_fractal
"""

import turtle


def draw_cross(x: float, y: float, length: float) -> None:
    """
    在指定位置绘制指定长度的十字形。
    """
    turtle.up()
    turtle.goto(x - length / 2, y - length / 6)
    turtle.down()
    turtle.seth(0)
    turtle.begin_fill()
    for _ in range(4):
        turtle.fd(length / 3)
        turtle.right(90)
        turtle.fd(length / 3)
        turtle.left(90)
        turtle.fd(length / 3)
        turtle.left(90)
    turtle.end_fill()


def draw_fractal_recursive(x: float, y: float, length: float, depth: float) -> None:
    """
    在指定位置以指定长度和深度递归绘制维切克分形。
    """
    if depth == 0:
        draw_cross(x, y, length)
        return

    draw_fractal_recursive(x, y, length / 3, depth - 1)
    draw_fractal_recursive(x + length / 3, y, length / 3, depth - 1)
    draw_fractal_recursive(x - length / 3, y, length / 3, depth - 1)
    draw_fractal_recursive(x, y + length / 3, length / 3, depth - 1)
    draw_fractal_recursive(x, y - length / 3, length / 3, depth - 1)


def set_color(rgb: str) -> None:
    turtle.color(rgb)


def draw_vicsek_fractal(
    x: float, y: float, length: float, depth: float, color="blue"
) -> None:
    """
    在指定位置以指定长度和深度绘制维切克分形。
    """
    turtle.speed(0)
    turtle.hideturtle()
    set_color(color)
    draw_fractal_recursive(x, y, length, depth)
    turtle.Screen().update()


def main() -> None:
    draw_vicsek_fractal(0, 0, 800, 4)

    turtle.done()


if __name__ == "__main__":
    main()
