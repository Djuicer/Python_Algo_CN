"""
Squareplus 激活函数

用途：Squareplus 旨在增强正值并抑制负值。
更多详细信息请参阅以下链接：
https://en.wikipedia.org/wiki/Rectifier_(neural_networks)#Squareplus
"""

import numpy as np


def squareplus(vector: np.ndarray, beta: float) -> np.ndarray:
    """
    实现 Squareplus 激活函数。

    参数：
        vector (np.ndarray): Squareplus 激活函数的输入数组。
        beta (float): 曲线区域的大小

    返回：
        np.ndarray: 应用 Squareplus 激活函数后的输入数组。

    公式：f(x) = ( x + sqrt(x^2 + b) ) / 2

    示例：
    >>> squareplus(np.array([2.3, 0.6, -2, -3.8]), beta=2)
    array([2.5       , 1.06811457, 0.22474487, 0.12731349])

    >>> squareplus(np.array([-9.2, -0.3, 0.45, -4.56]), beta=3)
    array([0.0808119 , 0.72891979, 1.11977651, 0.15893419])
    """
    return (vector + np.sqrt(vector**2 + beta)) / 2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
