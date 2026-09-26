"""
前向传播（Forward Propagation）说明：
https://en.wikipedia.org/wiki/Feedforward_neural_network
"""

import math
import random


# Sigmoid 激活函数
def sigmoid_function(value: float, deriv: bool = False) -> float:
    """返回浮点数的 sigmoid 函数值。

    >>> sigmoid_function(3.5)
    0.9706877692486436
    >>> sigmoid_function(3.5, True)
    -8.75
    """
    if deriv:
        return value * (1 - value)
    return 1 / (1 + math.exp(-value))


# 初始值
INITIAL_VALUE = 0.02


def forward_propagation(expected: int, number_propagations: int) -> float:
    """返回前向传播训练后得到的值。

    >>> res = forward_propagation(32, 450_000)  # Was 10_000_000
    >>> res > 31 and res < 33
    True

    >>> res = forward_propagation(32, 1000)
    >>> res > 31 and res < 33
    False
    """

    # 随机权重
    weight = float(2 * (random.randint(1, 100)) - 1)

    for _ in range(number_propagations):
        # 前向传播
        layer_1 = sigmoid_function(INITIAL_VALUE * weight)
        # 计算误差
        layer_1_error = (expected / 100) - layer_1
        # 误差增量
        layer_1_delta = layer_1_error * sigmoid_function(layer_1, True)
        # 更新权重
        weight += INITIAL_VALUE * layer_1_delta

    return layer_1 * 100


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    expected = int(input("Expected value: "))
    number_propagations = int(input("Number of propagations: "))
    print(forward_propagation(expected, number_propagations))
