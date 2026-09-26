"""
Mish 激活函数

用途：用于计算机视觉的 ReLU 激活函数改进版本。
更多详细信息请参阅以下链接：
https://en.wikipedia.org/wiki/Rectifier_(neural_networks)#Mish
"""

import numpy as np

from .softplus import softplus


def mish(vector: np.ndarray) -> np.ndarray:
    """
        实现 Mish 激活函数。

        参数：
            vector (np.ndarray): Mish 激活函数的输入数组。

        返回：
            np.ndarray: 应用 Mish 激活函数后的输入数组。

        公式：
            f(x) = x * tanh(softplus(x)) = x * tanh(ln(1 + e^x))

    示例：
    >>> mish(vector=np.array([2.3,0.6,-2,-3.8]))
    array([ 2.26211893,  0.46613649, -0.25250148, -0.08405831])

    >>> mish(np.array([-9.2, -0.3, 0.45, -4.56]))
    array([-0.00092952, -0.15113318,  0.33152014, -0.04745745])

    """
    return vector * np.tanh(softplus(vector))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
