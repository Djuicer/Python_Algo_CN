"""
带泄漏修正线性单元（Leaky Rectified Linear Unit，Leaky ReLU）

用途：Leaky ReLU 用于缓解梯度消失问题。
更多详细信息请参阅以下链接：
https://en.wikipedia.org/wiki/Rectifier_(neural_networks)#Leaky_ReLU
"""

import numpy as np


def leaky_rectified_linear_unit(vector: np.ndarray, alpha: float) -> np.ndarray:
    """
        实现 Leaky ReLU 激活函数。

        参数：
            vector (np.ndarray): Leaky ReLU 激活函数的输入数组。
            alpha (float): 负值部分的斜率。

        返回：
            np.ndarray: 应用 Leaky ReLU 激活函数后的输入数组。

        公式：f(x) = x if x > 0 else f(x) = alpha * x

    示例：
    >>> leaky_rectified_linear_unit(vector=np.array([2.3,0.6,-2,-3.8]), alpha=0.3)
    array([ 2.3 ,  0.6 , -0.6 , -1.14])

    >>> leaky_rectified_linear_unit(np.array([-9.2, -0.3, 0.45, -4.56]), alpha=0.067)
    array([-0.6164 , -0.0201 ,  0.45   , -0.30552])

    """
    return np.where(vector > 0, vector, alpha * vector)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
