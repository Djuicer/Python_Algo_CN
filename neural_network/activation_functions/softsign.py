"""
本脚本演示 Softsign 激活函数的实现。

Softsign 是一种平滑激活函数，定义如下：

    f(x) = x / (1 + |x|)

它将输入值映射到 (-1, 1) 范围内，与双曲正切（tanh）函数类似，
但使用多项式衰减而非指数衰减。

https://en.wikipedia.org/wiki/Activation_function
https://www.gabormelli.com/RKB/Softsign_Activation_Function
"""

import numpy as np


def softsign(vector: np.ndarray) -> np.ndarray:
    """
    实现 Softsign 激活函数。

    参数：
        vector (ndarray): 由数值组成的向量

    返回：
        vector (ndarray): 应用 Softsign 函数后的输入向量

    >>> vector = np.array([-5, -1, 0, 1, 5])
    >>> softsign(vector)
    array([-0.83333333, -0.5       ,  0.        ,  0.5       ,  0.83333333])
    """
    return vector / (1 + np.abs(vector))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
