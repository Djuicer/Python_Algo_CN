"""
实现指数线性单元（Exponential Linear Unit，ELU）函数。

该函数接收一个包含 K 个实数的向量和一个实数 alpha，并对向量中的每个元素应用 ELU 函数。

本脚本受对应 Wikipedia 文章启发：
https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
"""

import numpy as np


def exponential_linear_unit(vector: np.ndarray, alpha: float) -> np.ndarray:
    """
         实现 ELU 激活函数。
         参数：
             vector: 包含 ELU 激活函数输入的数组
             alpha: 超参数
         返回：
         elu (np.array): 应用 ELU 后的输入 NumPy 数组。

         数学定义：f(x) = x, x>0 else (alpha * (e^x -1)), x<=0, alpha >=0

    示例：
    >>> exponential_linear_unit(vector=np.array([2.3,0.6,-2,-3.8]), alpha=0.3)
    array([ 2.3       ,  0.6       , -0.25939942, -0.29328877])

    >>> exponential_linear_unit(vector=np.array([-9.2,-0.3,0.45,-4.56]), alpha=0.067)
    array([-0.06699323, -0.01736518,  0.45      , -0.06629904])


    """
    return np.where(vector > 0, vector, (alpha * (np.exp(vector) - 1)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
