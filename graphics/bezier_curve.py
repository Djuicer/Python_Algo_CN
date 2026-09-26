# https://en.wikipedia.org/wiki/B%C3%A9zier_curve
# https://www.tutorialspoint.com/computer_graphics/computer_graphics_curves.htm
from __future__ import annotations

from scipy.special import comb


class BezierCurve:
    """
    贝塞尔曲线（Bezier Curve）是一组控制点的加权和。
    根据给定的控制点集生成贝塞尔曲线。
    此实现仅适用于 xy 平面上的二维坐标。
    """

    def __init__(self, list_of_points: list[tuple[float, float]]) -> None:
        """
        list_of_points：xy 平面上用于插值的控制点。这些点控制贝塞尔曲线的行为（形状）。
        """
        self.list_of_points = list_of_points
        # 次数决定曲线的灵活程度。
        # 次数为 1 时将生成直线。
        self.degree = len(list_of_points) - 1

    def basis_function(self, t: float) -> list[float]:
        """
        基函数决定参数 t 处各控制点的权重。
            t：用于计算曲线基函数的参数值，范围为闭区间 [0, 1]。
        返回参数 t 处基函数的 x、y 值。

        >>> curve = BezierCurve([(1,1), (1,2)])
        >>> [float(x) for x in curve.basis_function(0)]
        [1.0, 0.0]
        >>> [float(x) for x in curve.basis_function(1)]
        [0.0, 1.0]
        """
        assert 0 <= t <= 1, "Time t must be between 0 and 1."
        output_values: list[float] = []
        for i in range(len(self.list_of_points)):
            # 每个 i 对应的基函数
            output_values.append(
                comb(self.degree, i) * ((1 - t) ** (self.degree - i)) * (t**i)
            )
        # 要生成有效的贝塞尔曲线，各基函数之和必须为 1。
        assert round(sum(output_values), 5) == 1
        return output_values

    def bezier_curve_function(self, t: float) -> tuple[float, float]:
        """
        计算贝塞尔曲线在参数 t 处取值的函数。
            t：用于计算贝塞尔函数的参数值
        返回贝塞尔曲线在参数 t 处的 x、y 坐标。
            t = 0 时得到曲线的第一个点。
            t = 1 时得到曲线的最后一个点。

        >>> curve = BezierCurve([(1,1), (1,2)])
        >>> tuple(float(x) for x in curve.bezier_curve_function(0))
        (1.0, 1.0)
        >>> tuple(float(x) for x in curve.bezier_curve_function(1))
        (1.0, 2.0)
        """

        assert 0 <= t <= 1, "Time t must be between 0 and 1."

        basis_function = self.basis_function(t)
        x = 0.0
        y = 0.0
        for i in range(len(self.list_of_points)):
            # 对所有点累加第 i 个基函数与第 i 个点的乘积。
            x += basis_function[i] * self.list_of_points[i][0]
            y += basis_function[i] * self.list_of_points[i][1]
        return (x, y)

    def derivative(self, t: float) -> tuple[float, float]:
        """
        计算贝塞尔曲线在参数 t 处的导数（切向量）。
        t：0 到 1 之间的参数
        返回表示曲线在 t 处方向的 (dx, dy) 向量。
        """
        if not 0 <= t <= 1:
            raise ValueError("Time t must be between 0 and 1.")

        n = self.degree
        dx = 0.0
        dy = 0.0
        for i in range(n):
            coeff = comb(n - 1, i) * ((1 - t) ** (n - 1 - i)) * (t**i)
            delta_x = self.list_of_points[i + 1][0] - self.list_of_points[i][0]
            delta_y = self.list_of_points[i + 1][1] - self.list_of_points[i][1]
            dx += coeff * delta_x * n
            dy += coeff * delta_y * n
        return (dx, dy)

    def plot_curve(self, step_size: float = 0.01) -> None:
        """
        使用 matplotlib 的绘图功能绘制贝塞尔曲线。
            step_size：定义计算贝塞尔曲线时的步长。
            步长越小，生成的曲线越精细。
        """
        from matplotlib import pyplot as plt

        to_plot_x: list[float] = []  # 待绘制点的 x 坐标
        to_plot_y: list[float] = []  # 待绘制点的 y 坐标

        t = 0.0
        while t <= 1:
            value = self.bezier_curve_function(t)
            to_plot_x.append(value[0])
            to_plot_y.append(value[1])
            t += step_size

        x = [i[0] for i in self.list_of_points]
        y = [i[1] for i in self.list_of_points]

        plt.plot(
            to_plot_x,
            to_plot_y,
            color="blue",
            label="Curve of Degree " + str(self.degree),
        )
        plt.scatter(x, y, color="red", label="Control Points")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    BezierCurve([(1, 2), (3, 5)]).plot_curve()  # 1 次曲线
    BezierCurve([(0, 0), (5, 5), (5, 0)]).plot_curve()  # 2 次曲线
    BezierCurve([(0, 0), (5, 5), (5, 0), (2.5, -2.5)]).plot_curve()  # 3 次曲线

    # 测试导数方法
    curve = BezierCurve([(0, 0), (5, 5), (5, 0)])
    print("Derivative at t=0.0:", curve.derivative(0.0))
    print("Derivative at t=0.5:", curve.derivative(0.5))
    print("Derivative at t=1.0:", curve.derivative(1.0))
