"""
本脚本实现 Soboleva 修正双曲正切函数。

该函数对向量中的每个元素应用 Soboleva 修正双曲正切函数。

有关该激活函数的更多详细信息，请参阅：
https://en.wikipedia.org/wiki/Soboleva_modified_hyperbolic_tangent
"""

import numpy as np


def soboleva_modified_hyperbolic_tangent(
    vector: np.ndarray, a_value: float, b_value: float, c_value: float, d_value: float
) -> np.ndarray:
    """
    实现 Soboleva 修正双曲正切函数。

    参数：
        vector (ndarray): 由数值组成的向量
        a_value (float): 方程中的参数 a
        b_value (float): 方程中的参数 b
        c_value (float): 方程中的参数 c
        d_value (float): 方程中的参数 d

    返回：
        vector (ndarray): 应用 SMHT 函数后的输入数组

    >>> vector = np.array([5.4, -2.4, 6.3, -5.23, 3.27, 0.56])
    >>> soboleva_modified_hyperbolic_tangent(vector, 0.2, 0.4, 0.6, 0.8)
    array([ 0.11075085, -0.28236685,  0.07861169, -0.1180085 ,  0.22999056,
            0.1566043 ])
    """

    # 为简化计算，将分子和分母分开
    # 逐元素计算分子和分母
    numerator = np.exp(a_value * vector) - np.exp(-b_value * vector)
    denominator = np.exp(c_value * vector) + np.exp(-d_value * vector)

    # 逐元素计算并返回最终结果
    return numerator / denominator


if __name__ == "__main__":
    import doctest

    doctest.testmod()
