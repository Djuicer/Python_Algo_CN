"""
隶属度向量上的 Zadeh 模糊集合运算符。

论域 ``X`` 上的模糊集合由*隶属函数* ``mu: X -> [0, 1]`` 描述。在网格上对论域
采样后，该函数便成为由隶属度组成的 NumPy 向量，经典集合运算也随之化为
逐元素运算。

本模块实现标准的 Zadeh 运算符及若干常见替代运算。与通过三个定义点存储
*三角模糊数*的 ``fuzzy_operations.FuzzySet`` 不同，此处函数直接处理采样后的
隶属度向量，因此适用于*任意*形状的隶属函数（三角形、梯形、高斯形等）。

参考资料：
  - https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations
  - https://en.wikipedia.org/wiki/Fuzzy_logic
  - https://en.wikipedia.org/wiki/T-norm

依赖：
  - numpy

最初由 Jigyasa Gandhi 以 ``scikit-fuzzy`` 演示程序的形式贡献；此处将其改写为
仅依赖 NumPy 的版本，并用 doctest 覆盖。
"""

import numpy as np
from numpy.typing import NDArray


def triangular_membership(
    grid: NDArray[np.float64], left: float, peak: float, right: float
) -> NDArray[np.float64]:
    """
    在 ``grid`` 上对三角隶属函数进行采样。

    隶属度从 ``left`` 处的 0 线性上升至 ``peak`` 处的 1，再下降至 ``right``
    处的 0。

    >>> grid = np.array([0.0, 25.0, 50.0])
    >>> triangular_membership(grid, 0, 25, 50)
    array([0., 1., 0.])
    >>> triangular_membership(np.array([10.0, 12.5]), 0, 25, 50)
    array([0.4, 0.5])
    """
    if not left <= peak <= right:
        msg = f"Expected left <= peak <= right, got {left}, {peak}, {right}"
        raise ValueError(msg)
    left_slope = (
        (grid - left) / (peak - left) if peak > left else np.where(grid < peak, 0, 1)
    )
    right_slope = (
        (right - grid) / (right - peak) if right > peak else np.where(grid > peak, 0, 1)
    )
    return np.clip(np.minimum(left_slope, right_slope), 0.0, 1.0)


def fuzzy_union(
    membership_a: NDArray[np.float64], membership_b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    并集（逻辑 OR）：``max(mu_A(x), mu_B(x))``。

    >>> fuzzy_union(np.array([0.2, 0.7]), np.array([0.5, 0.1]))
    array([0.5, 0.7])
    """
    return np.maximum(membership_a, membership_b)


def fuzzy_intersection(
    membership_a: NDArray[np.float64], membership_b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    交集（逻辑 AND）：``min(mu_A(x), mu_B(x))``。

    >>> fuzzy_intersection(np.array([0.2, 0.7]), np.array([0.5, 0.1]))
    array([0.2, 0.1])
    """
    return np.minimum(membership_a, membership_b)


def fuzzy_complement(membership: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    补集（逻辑 NOT）：``1 - mu_A(x)``。

    >>> fuzzy_complement(np.array([0.0, 0.3, 1.0]))
    array([1. , 0.7, 0. ])
    """
    return 1.0 - membership


def fuzzy_difference(
    membership_a: NDArray[np.float64], membership_b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    差集 ``A / B``：``min(mu_A(x), 1 - mu_B(x))``。

    >>> fuzzy_difference(np.array([0.6, 0.4]), np.array([0.2, 0.9]))
    array([0.6, 0.1])
    """
    return np.minimum(membership_a, 1.0 - membership_b)


def algebraic_sum(
    membership_a: NDArray[np.float64], membership_b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    代数和（概率和）：``mu_A + mu_B - mu_A * mu_B``。

    >>> algebraic_sum(np.array([0.5, 1.0]), np.array([0.5, 0.2]))
    array([0.75, 1.  ])
    """
    return membership_a + membership_b - membership_a * membership_b


def algebraic_product(
    membership_a: NDArray[np.float64], membership_b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    代数积：``mu_A * mu_B``。

    >>> algebraic_product(np.array([0.5, 1.0]), np.array([0.5, 0.2]))
    array([0.25, 0.2 ])
    """
    return membership_a * membership_b


def bounded_sum(
    membership_a: NDArray[np.float64], membership_b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    有界和（Lukasiewicz t-余范数）：``min(1, mu_A + mu_B)``。

    >>> bounded_sum(np.array([0.5, 0.8]), np.array([0.2, 0.7]))
    array([0.7, 1. ])
    """
    return np.minimum(1.0, membership_a + membership_b)


def bounded_difference(
    membership_a: NDArray[np.float64], membership_b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    有界差（Lukasiewicz t-范数）：``max(0, mu_A + mu_B - 1)``。

    >>> bounded_difference(np.array([0.5, 0.8]), np.array([0.2, 0.7]))
    array([0. , 0.5])
    """
    return np.maximum(0.0, membership_a + membership_b - 1.0)


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    # 在不依赖额外库的情况下复现原始的“年轻人与中年人”演示
    universe = np.linspace(start=0, stop=75, num=75)
    young = triangular_membership(universe, 0, 25, 50)
    middle_aged = triangular_membership(universe, 25, 50, 75)

    operations = {
        "young": young,
        "middle_aged": middle_aged,
        "union": fuzzy_union(young, middle_aged),
        "intersection": fuzzy_intersection(young, middle_aged),
        "complement(young)": fuzzy_complement(young),
        "difference young/middle": fuzzy_difference(young, middle_aged),
        "algebraic_sum": algebraic_sum(young, middle_aged),
        "algebraic_product": algebraic_product(young, middle_aged),
        "bounded_sum": bounded_sum(young, middle_aged),
        "bounded_difference": bounded_difference(young, middle_aged),
    }

    try:
        import matplotlib.pyplot as plt

        plt.figure()
        for index, (title, values) in enumerate(operations.items(), start=1):
            plt.subplot(4, 3, index)
            plt.plot(universe, values)
            plt.title(title)
            plt.grid(True)
        plt.subplots_adjust(hspace=0.5)
        plt.show()
    except ImportError:
        for title, values in operations.items():
            print(f"{title}: peak membership = {values.max():.3f}")
