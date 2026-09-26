"""
本脚本演示修正线性单元（ReLU）函数的实现。

在神经网络中，该激活函数定义为参数的正值部分。
函数接收包含 K 个实数的向量，然后计算 argmax(x, 0)。
经过 ReLU 后，向量元素为 0 或实数。

本脚本受对应 Wikipedia 文章启发：
https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
"""

from __future__ import annotations

import numpy as np


def relu(vector: list[float]):
    """
    实现 ReLU 函数。

    参数：
        vector (np.array,list,tuple): 由实数组成、形状为 (1,n) 的 NumPy 数组，
        或类似的 list、tuple


    返回：
        relu_vec (np.array): 应用 ReLU 后的输入 NumPy 数组。

    >>> vec = np.array([-1, 0, 5])
    >>> relu(vec)
    array([0, 0, 5])
    """

    # 比较两个数组，并返回逐元素最大值
    return np.maximum(0, vector)


if __name__ == "__main__":
    print(np.array(relu([-1, 0, 5])))  # --> [0, 0, 5]
