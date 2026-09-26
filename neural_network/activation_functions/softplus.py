"""
Softplus 激活函数

用途：Softplus 函数是 ReLU 函数的平滑近似。
更多详细信息请参阅以下链接：
https://en.wikipedia.org/wiki/Rectifier_(neural_networks)#Softplus
"""

import numpy as np


def softplus(vector: np.ndarray) -> np.ndarray:
    """
    实现 Softplus 激活函数。

    参数：
        vector (np.ndarray): Softplus 激活函数的输入数组。

    返回：
        np.ndarray: 应用 Softplus 激活函数后的输入数组。

    公式：f(x) = ln(1 + e^x)

    示例：
    >>> softplus(np.array([2.3, 0.6, -2, -3.8]))
    array([2.39554546, 1.03748795, 0.12692801, 0.02212422])

    >>> softplus(np.array([-9.2, -0.3, 0.45, -4.56]))
    array([1.01034298e-04, 5.54355244e-01, 9.43248946e-01, 1.04077103e-02])
    """
    return np.log(1 + np.exp(vector))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
