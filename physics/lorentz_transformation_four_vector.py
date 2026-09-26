"""
洛伦兹变换描述两个彼此相对运动的惯性参考系 F 和 F' 之间的转换。本代码仅
计算沿 x 方向运动且无空间旋转的洛伦兹变换（即 x 方向的洛伦兹推进）。
这里将洛伦兹变换计算为 Minkowski 空间四维矢量 [ct, x, y, z] 的线性变换。
注意，每个四维矢量的首项中，t（时间）要乘以 c（光速）。

若 X = [ct; x; y; z] 和 X' = [ct'; x'; y'; z'] 是两个惯性参考系的四维矢量，
且 X' 相对于 X 以速度 v 沿 x 方向运动，则从 X 到 X' 的洛伦兹变换为 X' = BX，
其中：

    | y  -γβ  0  0|
B = |-γβ  y   0  0|
    | 0   0   1  0|
    | 0   0   0  1|

该矩阵描述 X 与 X' 之间的洛伦兹推进；y = 1 / √(1 - v²/c²) 为洛伦兹因子，
β = v/c 为速度与 c 的比值。

参考资料：https://en.wikipedia.org/wiki/Lorentz_transformation
"""

from math import sqrt

import numpy as np
from sympy import symbols

# 系数
# 光速 (m/s)
c = 299792458

# 符号
ct, x, y, z = symbols("ct x y z")


# 物体速度除以光速（无量纲）
def beta(velocity: float) -> float:
    """
    计算 β = v/c，即给定速度与 c 的比值。
    >>> beta(c)
    1.0
    >>> beta(199792458)
    0.666435904801848
    >>> beta(1e5)
    0.00033356409519815205
    >>> beta(0.2)
    Traceback (most recent call last):
      ...
    ValueError: Speed must be greater than or equal to 1!
    """
    if velocity > c:
        raise ValueError("Speed must not exceed light speed 299,792,458 [m/s]!")
    if velocity < 1:
        # 通常速度应远大于 1（与 c 同一数量级）
        raise ValueError("Speed must be greater than or equal to 1!")

    return velocity / c


def gamma(velocity: float) -> float:
    """
    计算给定速度对应的洛伦兹因子 y = 1 / √(1 - v²/c²)。
    >>> gamma(4)
    1.0000000000000002
    >>> gamma(1e5)
    1.0000000556325075
    >>> gamma(3e7)
    1.005044845777813
    >>> gamma(2.8e8)
    2.7985595722318277
    >>> gamma(299792451)
    4627.49902669495
    >>> gamma(0.3)
    Traceback (most recent call last):
      ...
    ValueError: Speed must be greater than or equal to 1!
    >>> gamma(2 * c)
    Traceback (most recent call last):
      ...
    ValueError: Speed must not exceed light speed 299,792,458 [m/s]!
    """
    return 1 / sqrt(1 - beta(velocity) ** 2)


def transformation_matrix(velocity: float) -> np.ndarray:
    """
    计算沿 x 方向运动的洛伦兹变换矩阵：

    | y  -γβ  0  0|
    |-γβ  y   0  0|
    | 0   0   1  0|
    | 0   0   0  1|

    其中 y 为洛伦兹因子，β 为速度与 c 的比值。
    >>> transformation_matrix(29979245)
    array([[ 1.00503781, -0.10050378,  0.        ,  0.        ],
           [-0.10050378,  1.00503781,  0.        ,  0.        ],
           [ 0.        ,  0.        ,  1.        ,  0.        ],
           [ 0.        ,  0.        ,  0.        ,  1.        ]])
    >>> transformation_matrix(19979245.2)
    array([[ 1.00222811, -0.06679208,  0.        ,  0.        ],
           [-0.06679208,  1.00222811,  0.        ,  0.        ],
           [ 0.        ,  0.        ,  1.        ,  0.        ],
           [ 0.        ,  0.        ,  0.        ,  1.        ]])
    >>> transformation_matrix(1)
    array([[ 1.00000000e+00, -3.33564095e-09,  0.00000000e+00,
             0.00000000e+00],
           [-3.33564095e-09,  1.00000000e+00,  0.00000000e+00,
             0.00000000e+00],
           [ 0.00000000e+00,  0.00000000e+00,  1.00000000e+00,
             0.00000000e+00],
           [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
             1.00000000e+00]])
    >>> transformation_matrix(0)
    Traceback (most recent call last):
      ...
    ValueError: Speed must be greater than or equal to 1!
    >>> transformation_matrix(c * 1.5)
    Traceback (most recent call last):
      ...
    ValueError: Speed must not exceed light speed 299,792,458 [m/s]!
    """
    return np.array(
        [
            [gamma(velocity), -gamma(velocity) * beta(velocity), 0, 0],
            [-gamma(velocity) * beta(velocity), gamma(velocity), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


def transform(velocity: float, event: np.ndarray | None = None) -> np.ndarray:
    """
    根据速度和惯性参考系的四维矢量，计算沿 x 方向运动的洛伦兹变换。

    若未给出四维矢量，则使用变量进行符号变换。
    >>> transform(29979245, np.array([1, 2, 3, 4]))
    array([ 3.01302757e+08, -3.01302729e+07,  3.00000000e+00,  4.00000000e+00])
    >>> transform(29979245)
    array([1.00503781498831*ct - 0.100503778816875*x,
           -0.100503778816875*ct + 1.00503781498831*x, 1.0*y, 1.0*z],
          dtype=object)
    >>> transform(19879210.2)
    array([1.0022057787097*ct - 0.066456172618675*x,
           -0.066456172618675*ct + 1.0022057787097*x, 1.0*y, 1.0*z],
          dtype=object)
    >>> transform(299792459, np.array([1, 1, 1, 1]))
    Traceback (most recent call last):
      ...
    ValueError: Speed must not exceed light speed 299,792,458 [m/s]!
    >>> transform(-1, np.array([1, 1, 1, 1]))
    Traceback (most recent call last):
      ...
    ValueError: Speed must be greater than or equal to 1!
    """
    # 确保 event 非空
    if event is None:
        event = np.array([ct, x, y, z])  # 符号四维矢量
    else:
        event[0] *= c  # x0 为 ct（光速 * 时间）

    return transformation_matrix(velocity) @ event


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 符号矢量示例：
    four_vector = transform(29979245)
    print("Example of four vector: ")
    print(f"ct' = {four_vector[0]}")
    print(f"x' = {four_vector[1]}")
    print(f"y' = {four_vector[2]}")
    print(f"z' = {four_vector[3]}")

    # 用数值替换符号
    sub_dict = {ct: c, x: 1, y: 1, z: 1}
    numerical_vector = [four_vector[i].subs(sub_dict) for i in range(4)]

    print(f"\n{numerical_vector}")
