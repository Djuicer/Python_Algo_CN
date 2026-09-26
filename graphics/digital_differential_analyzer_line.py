# https://en.wikipedia.org/wiki/Digital_differential_analyzer_(graphics_algorithm)

import matplotlib.pyplot as plt


def digital_differential_analyzer_line(
    p1: tuple[int, int], p2: tuple[int, int]
) -> list[tuple[int, int]]:
    """
    数字微分分析器（Digital Differential Analyzer, DDA）直线绘制算法。

    通过计算两点的 x 坐标差 dx 和 y 坐标差 dy，在主轴上逐步移动，
    同时使用小数增量更新另一坐标轴，从而在两点之间绘制直线。

    DDA 算法的主要缺点之一是依赖浮点运算，这可能在每一步引入舍入误差。
    因此，它通常比仅使用整数运算的 Bresenham 直线绘制算法更慢且精度更低。

    尽管如此，DDA 易于理解，并能展示增量式生成直线的基本思想，适合教学使用。

    该算法计算 dx（x 的变化量）和 dy（y 的变化量），随后沿主轴迭代移动，
    并以小数增量（斜率）更新另一坐标轴。
    它结构简单，但也存在主要缺点：
    * 每一步都依赖浮点运算，计算速度较慢。
    * Bresenham 算法仅使用整数运算即可得到相同结果，性能通常优于该算法。

    参数：
      - p1：起点坐标。
      - p2：终点坐标。
    返回：
      - 构成直线的坐标点列表。

    >>> digital_differential_analyzer_line((1, 1), (4, 4))
    [(2, 2), (3, 3), (4, 4)]
    """
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / float(steps)
    y_increment = dy / float(steps)
    coordinates = []
    x: float = x1
    y: float = y1
    for _ in range(steps):
        x += x_increment
        y += y_increment
        coordinates.append((round(x), round(y)))
    return coordinates


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    x1 = int(input("Enter the x-coordinate of the starting point: "))
    y1 = int(input("Enter the y-coordinate of the starting point: "))
    x2 = int(input("Enter the x-coordinate of the ending point: "))
    y2 = int(input("Enter the y-coordinate of the ending point: "))
    coordinates = digital_differential_analyzer_line((x1, y1), (x2, y2))
    x_points, y_points = zip(*coordinates)
    plt.plot(x_points, y_points, marker="o")
    plt.title("Digital Differential Analyzer Line Drawing Algorithm")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid()
    plt.show()
