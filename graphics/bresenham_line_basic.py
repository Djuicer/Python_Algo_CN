"""
经典 Bresenham 直线绘制算法
------------------------------------------

在点 (x1, y1) 与 (x2, y2) 之间绘制斜率满足 0 ≤ m ≤ 1 的直线，
且不使用浮点运算。

参考资料：https://www.geeksforgeeks.org/dsa/bresenhams-line-generation-algorithm/

>>> classic_bresenham_line((0, 0), (5, 3))
[(0, 0), (1, 1), (2, 1), (3, 2), (4, 2), (5, 3)]
"""

import matplotlib.pyplot as plt


def classic_bresenham_line(
    p1: tuple[int, int], p2: tuple[int, int]
) -> list[tuple[int, int]]:
    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1
    p = 2 * dy - dx
    y = y1
    points = []

    for x in range(x1, x2 + 1):
        points.append((x, y))
        if p < 0:
            p += 2 * dy
        else:
            y += 1
            p += 2 * (dy - dx)
    return points


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    x1 = int(input("Enter x1: "))
    y1 = int(input("Enter y1: "))
    x2 = int(input("Enter x2: "))
    y2 = int(input("Enter y2: "))

    points = classic_bresenham_line((x1, y1), (x2, y2))
    print("Generated points:", points)

    xs, ys = zip(*points)
    plt.plot(xs, ys, marker="o")
    plt.title("Classic Bresenham's Line Algorithm")
    plt.grid()
    plt.show()
