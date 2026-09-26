"""
本脚本演示 Sigmoid 线性单元（SiLU），即 Swish 函数的实现。
* https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
* https://en.wikipedia.org/wiki/Swish_function

该函数接收包含 K 个实数的向量 x，并返回 x * sigmoid(x)。
Swish 是一种平滑的非单调函数，定义为 f(x) = x * sigmoid(x)。
大量实验表明，在图像分类和机器翻译等多种具有挑战性的领域中，
Swish 在深度网络上的表现始终不逊于或优于 ReLU。

本脚本受相关研究论文启发。
* https://arxiv.org/abs/1710.05941
* https://blog.paperspace.com/swish-activation-function/
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


def sigmoid_linear_unit(vector: np.ndarray) -> np.ndarray:
    """
    实现 Sigmoid 线性单元（SiLU），即 Swish 函数。

    参数：
        vector (np.ndarray): 由实数组成的 NumPy 数组

    返回：
        swish_vec (np.ndarray): 应用 Swish 后的输入 NumPy 数组

    示例：
    >>> sigmoid_linear_unit(np.array([-1.0, 1.0, 2.0]))
    array([-0.26894142,  0.73105858,  1.76159416])

    >>> sigmoid_linear_unit(np.array([-2]))
    array([-0.23840584])
    """
    return vector * sigmoid(vector)


def swish(vector: np.ndarray, trainable_parameter: int) -> np.ndarray:
    """
    参数：
        vector (np.ndarray): 由实数组成的 NumPy 数组
        trainable_parameter: 用于实现不同的 Swish 激活函数

    返回：
        swish_vec (np.ndarray): 应用 Swish 后的输入 NumPy 数组

    示例：
    >>> swish(np.array([-1.0, 1.0, 2.0]), 2)
    array([-0.11920292,  0.88079708,  1.96402758])

    >>> swish(np.array([-2]), 1)
    array([-0.23840584])
    """
    return vector * sigmoid(trainable_parameter * vector)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
