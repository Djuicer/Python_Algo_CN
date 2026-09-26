"""
本脚本演示二值阶跃函数（Binary Step）的实现。

该激活函数在输入为正数或 0 时激活神经元，否则不激活。

这是一种简单的激活函数，以下 Wikipedia 文章中有所介绍：
https://en.wikipedia.org/wiki/Activation_function
"""

import numpy as np


def binary_step(vector: np.ndarray) -> np.ndarray:
    """
    实现二值阶跃函数。

    参数：
        vector (ndarray): 由数值组成的向量

    返回：
        vector (ndarray): 应用二值阶跃函数后的输入向量

    >>> vector = np.array([-1.2, 0, 2, 1.45, -3.7, 0.3])
    >>> binary_step(vector)
    array([0, 1, 1, 1, 0, 1])
    """

    return np.where(vector >= 0, 1, 0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
