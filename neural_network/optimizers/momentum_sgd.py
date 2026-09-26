"""
动量 SGD 优化器

使用 NumPy 实现用于神经网络训练的动量 SGD。
动量有助于沿相关方向加速梯度并抑制振荡。

Reference: https://en.wikipedia.org/wiki/Stochastic_gradient_descent#Momentum
Author: Adhithya Laxman Ravi Shankar Geetha
Github: https://github.com/Adhithya-Laxman
Date: 2025.10.22
"""

import numpy as np


class MomentumSGD:
    """
    带动量的 SGD 优化器。

    使用动量更新参数：
        velocity = momentum * velocity - learning_rate * gradient
        param = param + velocity
    """

    def __init__(self, learning_rate: float = 0.01, momentum: float = 0.9) -> None:
        """
        初始化动量 SGD 优化器。

        参数：
            learning_rate (float): 权重更新的学习率。
            momentum (float): 动量因子。

        >>> optimizer = MomentumSGD(learning_rate=0.01, momentum=0.9)
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
        使用动量更新参数。

        参数：
            param_id (int): 参数组的唯一标识符。
            params (np.ndarray): 当前参数。
            gradients (np.ndarray): 参数的梯度。

        返回：
            np.ndarray: 更新后的参数。

        >>> optimizer = MomentumSGD(learning_rate=0.1, momentum=0.9)
        >>> params = np.array([1.0, 2.0])
        >>> grads = np.array([0.1, 0.2])
        >>> updated = optimizer.update(0, params, grads)
        >>> updated.shape
        (2,)
        """
        if param_id not in self.velocity:
            self.velocity[param_id] = np.zeros_like(params)

        self.velocity[param_id] = (
            self.momentum * self.velocity[param_id] - self.learning_rate * gradients
        )
        return params + self.velocity[param_id]


# 使用示例
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Momentum SGD Example: Minimizing f(x) = x^2")

    optimizer = MomentumSGD(learning_rate=0.1, momentum=0.9)
    x = np.array([5.0])

    for step in range(20):
        gradient = 2 * x
        x = optimizer.update(0, x, gradient)
        if step % 5 == 0:
            print(f"Step {step}: x = {x[0]:.4f}, f(x) = {x[0] ** 2:.4f}")

    print(f"Final: x = {x[0]:.4f}, f(x) = {x[0] ** 2:.4f}")
