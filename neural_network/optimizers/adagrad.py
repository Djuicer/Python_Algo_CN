"""
Adagrad 优化器

使用 NumPy 实现用于神经网络训练的 Adagrad（Adaptive Gradient）。
Adagrad 根据历史梯度分别调整每个参数的学习率。

Reference: https://en.wikipedia.org/wiki/Stochastic_gradient_descent#AdaGrad
Author: Adhithya Laxman Ravi Shankar Geetha
Date: 2025.10.22
"""

import numpy as np


class Adagrad:
    """
    Adagrad 优化器。

    分别调整每个参数的学习率：
        accumulated_grad += gradient^2
        param = param - (learning_rate / sqrt(accumulated_grad + epsilon)) * gradient
    """

    def __init__(self, learning_rate: float = 0.01, epsilon: float = 1e-8) -> None:
        """
        初始化 Adagrad 优化器。

        参数：
            learning_rate (float): 初始学习率。
            epsilon (float): 用于保证数值稳定性的小常数。

        >>> optimizer = Adagrad(learning_rate=0.01, epsilon=1e-8)
        >>> optimizer.learning_rate
        0.01
        """
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.accumulated_grad: dict[int, np.ndarray] = {}

    def update(
        self, param_id: int, params: np.ndarray, gradients: np.ndarray
    ) -> np.ndarray:
        """
        使用 Adagrad 更新参数。

        参数：
            param_id (int): 参数组的唯一标识符。
            params (np.ndarray): 当前参数。
            gradients (np.ndarray): 参数的梯度。

        返回：
            np.ndarray: 更新后的参数。

        >>> optimizer = Adagrad(learning_rate=0.1)
        >>> params = np.array([1.0, 2.0])
        >>> grads = np.array([0.1, 0.2])
        >>> updated = optimizer.update(0, params, grads)
        >>> updated.shape
        (2,)
        """
        if param_id not in self.accumulated_grad:
            self.accumulated_grad[param_id] = np.zeros_like(params)

        self.accumulated_grad[param_id] += gradients**2
        adjusted_lr = self.learning_rate / (
            np.sqrt(self.accumulated_grad[param_id]) + self.epsilon
        )
        return params - adjusted_lr * gradients


# 使用示例
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Adagrad Example: Minimizing f(x) = x^2")

    optimizer = Adagrad(learning_rate=1.0)
    x = np.array([5.0])

    for step in range(20):
        gradient = 2 * x
        x = optimizer.update(0, x, gradient)
        if step % 5 == 0:
            print(f"Step {step}: x = {x[0]:.4f}, f(x) = {x[0] ** 2:.4f}")

    print(f"Final: x = {x[0]:.4f}, f(x) = {x[0] ** 2:.4f}")
