"""
Nesterov 加速梯度（NAG）优化器

使用 NumPy 实现用于神经网络训练的 Nesterov 动量。
NAG 进行前瞻，并在预期位置计算梯度。

Reference: https://cs231n.github.io/neural-networks-3/#sgd
Author: Adhithya Laxman Ravi Shankar Geetha
Date: 2025.10.21
"""

import numpy as np


class NesterovAcceleratedGradient:
    """
    Nesterov 加速梯度（NAG）优化器。

    使用 Nesterov 动量更新参数：
        velocity = momentum * velocity - learning_rate * gradient_at_lookahead
        param = param + velocity
    """

    def __init__(self, learning_rate: float = 0.01, momentum: float = 0.9) -> None:
        """
        初始化 NAG 优化器。

        参数：
            learning_rate (float): 权重更新的学习率。
            momentum (float): 动量因子。

        >>> optimizer = NesterovAcceleratedGradient(learning_rate=0.01, momentum=0.9)
        >>> optimizer.momentum
        0.9
        """
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.velocity: dict[int, np.ndarray] = {}

    def update(
        self, param_id: int, params: np.ndarray, gradients: np.ndarray
    ) -> np.ndarray:
        """
        使用 NAG 更新参数。

        参数：
            param_id (int): 参数组的唯一标识符。
            params (np.ndarray): 当前参数。
            gradients (np.ndarray): 前瞻位置处的梯度。

        返回：
            np.ndarray: 更新后的参数。

        >>> optimizer = NesterovAcceleratedGradient(learning_rate=0.1, momentum=0.9)
        >>> params = np.array([1.0, 2.0])
        >>> grads = np.array([0.1, 0.2])
        >>> updated = optimizer.update(0, params, grads)
        >>> updated.shape
        (2,)
        """
        if param_id not in self.velocity:
            self.velocity[param_id] = np.zeros_like(params)

        velocity_prev = self.velocity[param_id].copy()
        self.velocity[param_id] = (
            self.momentum * self.velocity[param_id] - self.learning_rate * gradients
        )
        return (
            params
            - self.momentum * velocity_prev
            + (1 + self.momentum) * self.velocity[param_id]
        )


# 使用示例
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("NAG Example: Minimizing f(x) = x^2")

    optimizer = NesterovAcceleratedGradient(learning_rate=0.1, momentum=0.9)
    x = np.array([5.0])

    for step in range(20):
        gradient = 2 * x
        x = optimizer.update(0, x, gradient)
        if step % 5 == 0:
            print(f"Step {step}: x = {x[0]:.4f}, f(x) = {x[0] ** 2:.4f}")

    print(f"Final: x = {x[0]:.4f}, f(x) = {x[0] ** 2:.4f}")
