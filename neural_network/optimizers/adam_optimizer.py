"""
Adam 优化器

使用 NumPy 实现用于神经网络训练的 Adam（Adaptive Moment Estimation）。
Adam 利用一阶矩和二阶矩估计，将动量与自适应学习率相结合。

Reference: https://arxiv.org/abs/1412.6980
Author: Adhithya Laxman Ravi Shankar Geetha
Date: 2025.10.21
"""

import numpy as np


class Adam:
    """
    Adam 优化器。

    将动量与 RMSProp 相结合：
        m = beta1 * m + (1 - beta1) * gradient
        v = beta2 * v + (1 - beta2) * gradient^2
        m_hat = m / (1 - beta1^t)
        v_hat = v / (1 - beta2^t)
        param = param - learning_rate * m_hat / (sqrt(v_hat) + epsilon)
    """

    def __init__(
        self,
        learning_rate: float = 0.001,
        beta1: float = 0.9,
        beta2: float = 0.999,
        epsilon: float = 1e-8,
    ) -> None:
        """
        初始化 Adam 优化器。

        参数：
            learning_rate (float): 学习率。
            beta1 (float): 一阶矩的指数衰减率。
            beta2 (float): 二阶矩的指数衰减率。
            epsilon (float): 用于保证数值稳定性的小常数。

        >>> optimizer = Adam(learning_rate=0.001, beta1=0.9, beta2=0.999)
        >>> optimizer.beta1
        0.9
        """
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m: dict[int, np.ndarray] = {}
        self.v: dict[int, np.ndarray] = {}
        self.t: dict[int, int] = {}

    def update(
        self, param_id: int, params: np.ndarray, gradients: np.ndarray
    ) -> np.ndarray:
        """
        使用 Adam 更新参数。

        参数：
            param_id (int): 参数组的唯一标识符。
            params (np.ndarray): 当前参数。
            gradients (np.ndarray): 参数的梯度。

        返回：
            np.ndarray: 更新后的参数。

        >>> optimizer = Adam(learning_rate=0.1)
        >>> params = np.array([1.0, 2.0])
        >>> grads = np.array([0.1, 0.2])
        >>> updated = optimizer.update(0, params, grads)
        >>> updated.shape
        (2,)
        """
        if param_id not in self.m:
            self.m[param_id] = np.zeros_like(params)
            self.v[param_id] = np.zeros_like(params)
            self.t[param_id] = 0

        self.t[param_id] += 1

        self.m[param_id] = self.beta1 * self.m[param_id] + (1 - self.beta1) * gradients
        self.v[param_id] = self.beta2 * self.v[param_id] + (1 - self.beta2) * (
            gradients**2
        )

        m_hat = self.m[param_id] / (1 - self.beta1 ** self.t[param_id])
        v_hat = self.v[param_id] / (1 - self.beta2 ** self.t[param_id])

        return params - self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)


# 使用示例
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Adam Example: Minimizing f(x) = x^2")

    optimizer = Adam(learning_rate=0.1)
    x = np.array([5.0])

    for step in range(20):
        gradient = 2 * x
        x = optimizer.update(0, x, gradient)
        if step % 5 == 0:
            print(f"Step {step}: x = {x[0]:.4f}, f(x) = {x[0] ** 2:.4f}")

    print(f"Final: x = {x[0]:.4f}, f(x) = {x[0] ** 2:.4f}")
