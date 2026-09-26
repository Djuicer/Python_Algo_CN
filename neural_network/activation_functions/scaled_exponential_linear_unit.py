"""
实现缩放指数线性单元（Scaled Exponential Linear Unit，SELU）函数。
该函数接收包含 K 个实数的向量，以及两个实数 alpha（默认值为 1.6732）和
lambda（默认值为 1.0507），并对向量中的每个元素应用 SELU 函数。
SELU 是一种自归一化激活函数，也是 ELU 的变体。SELU 的主要优点是其
自归一化特性可以使输出始终保持标准化，因此无需加入批归一化层。
参考资料：
https://iq.opengenus.org/scaled-exponential-linear-unit/
"""

import numpy as np


def scaled_exponential_linear_unit(
    vector: np.ndarray, alpha: float = 1.6732, lambda_: float = 1.0507
) -> np.ndarray:
    """
    对向量中的每个元素应用缩放指数线性单元函数。
    参数：
        vector : np.ndarray
        alpha : float (default = 1.6732)
        lambda_ : float (default = 1.0507)

    返回：np.ndarray
    公式：f(x) = lambda_ * x if x > 0
                     lambda_ * alpha * (e**x - 1) if x <= 0
    示例：
    >>> scaled_exponential_linear_unit(vector=np.array([1.3, 3.7, 2.4]))
    array([1.36591, 3.88759, 2.52168])

    >>> scaled_exponential_linear_unit(vector=np.array([1.3, 4.7, 8.2]))
    array([1.36591, 4.93829, 8.61574])
    """
    return lambda_ * np.where(vector > 0, vector, alpha * (np.exp(vector) - 1))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
