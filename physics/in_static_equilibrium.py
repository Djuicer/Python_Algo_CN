"""
检查力系是否处于静力平衡状态。
"""

from __future__ import annotations

from numpy import array, cos, float64, radians, sin
from numpy.typing import NDArray


def polar_force(
    magnitude: float, angle: float, radian_mode: bool = False
) -> list[float]:
    """
    将力分解为直角坐标分量。
    (force, angle) => (force_x, force_y)
    >>> import math
    >>> force = polar_force(10, 45)
    >>> math.isclose(force[0], 7.071067811865477)
    True
    >>> math.isclose(force[1], 7.0710678118654755)
    True
    >>> force = polar_force(10, 3.14, radian_mode=True)
    >>> math.isclose(force[0], -9.999987317275396)
    True
    >>> math.isclose(force[1], 0.01592652916486828)
    True
    """
    if radian_mode:
        return [magnitude * cos(angle), magnitude * sin(angle)]
    return [magnitude * cos(radians(angle)), magnitude * sin(radians(angle))]


def in_static_equilibrium(
    forces: NDArray[float64], location: NDArray[float64], eps: float = 10**-1
) -> bool:
    """
    检查系统是否处于平衡状态。
    接收两个 numpy.array 对象。
    forces ==>  [
                        [force1_x, force1_y],
                        [force2_x, force2_y],
                        ....]
    location ==>  [
                        [x1, y1],
                        [x2, y2],
                        ....]
    >>> force = array([[1, 1], [-1, 2]])
    >>> location = array([[1, 0], [10, 0]])
    >>> in_static_equilibrium(force, location)
    False
    """
    # 力矩之和为零
    # NumPy 2.x 移除了二维叉积，因此直接计算每一行的标量（z 轴）力矩：
    # x_i * Fy_i - y_i * Fx_i。
    moments: NDArray[float64] = (
        location[:, 0] * forces[:, 1] - location[:, 1] * forces[:, 0]
    )
    sum_moments: float = sum(moments)
    return bool(abs(sum_moments) < eps)


if __name__ == "__main__":
    # 测试其能否正常工作
    forces = array(
        [
            polar_force(718.4, 180 - 30),
            polar_force(879.54, 45),
            polar_force(100, -90),
        ]
    )

    location: NDArray[float64] = array([[0, 0], [0, 0], [0, 0]])

    assert in_static_equilibrium(forces, location)

    # image_data/2D_problems.jpg 中的问题 1
    forces = array(
        [
            polar_force(30 * 9.81, 15),
            polar_force(215, 180 - 45),
            polar_force(264, 90 - 30),
        ]
    )

    location = array([[0, 0], [0, 0], [0, 0]])

    assert in_static_equilibrium(forces, location)

    # image_data/2D_problems_1.jpg 中的问题
    forces = array([[0, -2000], [0, -1200], [0, 15600], [0, -12400]])

    location = array([[0, 0], [6, 0], [10, 0], [12, 0]])

    assert in_static_equilibrium(forces, location)

    import doctest

    doctest.testmod()
