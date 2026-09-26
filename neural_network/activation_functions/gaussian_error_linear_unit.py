"""
本脚本演示高斯误差线性单元（Gaussian Error Linear Unit，GELU）函数的实现。
* https://en.wikipedia.org/wiki/Activation_function#Comparison_of_activation_functions

该函数接收包含 K 个实数的向量，并返回 x * sigmoid(1.702*x)。
GELU 是一种性能优异的神经网络激活函数。

本脚本受相关研究论文启发。
* https://arxiv.org/abs/1606.08415
"""

import numpy as np


def sigmoid(vector: np.ndarray) -> np.ndarray:
    """
    数学函数 sigmoid 接收包含 K 个实数的向量 x，并返回 1/ (1 + e^-x)。
    https://en.wikipedia.org/wiki/Sigmoid_function

    >>> sigmoid(np.array([-1.0, 1.0, 2.0]))
    array([0.26894142, 0.73105858, 0.88079708])
    """
    return 1 / (1 + np.exp(-vector))


def gaussian_error_linear_unit(vector: np.ndarray) -> np.ndarray:
    """
    实现高斯误差线性单元（GELU）函数。

    参数：
        vector (np.ndarray): 由实数组成、形状为 (1, n) 的 NumPy 数组

    返回：
        gelu_vec (np.ndarray): 应用 GELU 后的输入 NumPy 数组

    示例：
    >>> gaussian_error_linear_unit(np.array([-1.0, 1.0, 2.0]))
    array([-0.15420423,  0.84579577,  1.93565862])

    >>> gaussian_error_linear_unit(np.array([-3]))
    array([-0.01807131])
    """
    return vector * sigmoid(1.702 * vector)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
