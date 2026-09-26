"""
Muon 优化器

使用 NumPy 实现用于神经网络隐藏层的 Muon 优化器。
Muon 使用 Newton-Schulz 正交化迭代来改善收敛效果。

Reference: https://kellerjordan.github.io/posts/muon/
Author: Adhithya Laxman Ravi Shankar Geetha
Date: 2025.10.21
"""

import numpy as np


class Muon:
    """
    用于隐藏层权重矩阵的 Muon 优化器。

    更新前对梯度应用 Newton-Schulz 正交化。
    """

    def __init__(
        self, learning_rate: float = 0.02, momentum: float = 0.95, ns_steps: int = 5
    ) -> None:
        """
        初始化 Muon 优化器。

        参数：
            learning_rate (float): 更新时使用的学习率。
            momentum (float): 动量因子。
            ns_steps (int): Newton-Schulz 迭代步数。

        >>> optimizer = Muon(learning_rate=0.02, momentum=0.95, ns_steps=5)
        >>> optimizer.momentum
        0.95
        """
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.ns_steps = ns_steps
        self.velocity: dict[int, np.ndarray] = {}

    def newton_schulz_orthogonalize(self, matrix: np.ndarray) -> np.ndarray:
        """
        使用 Newton-Schulz 迭代对矩阵进行正交化。

        参数：
            matrix (np.ndarray): 输入矩阵。

        返回：
            np.ndarray: 正交化后的矩阵。

        >>> optimizer = Muon()
        >>> mat = np.array([[1.0, 0.5], [0.5, 1.0]])
        >>> orth = optimizer.newton_schulz_orthogonalize(mat)
        >>> orth.shape
        (2, 2)
        """
        if matrix.shape[0] < matrix.shape[1]:
            matrix = matrix.T
            transposed = True
        else:
            transposed = False

        a = matrix.copy()
        for _ in range(self.ns_steps):
            a = 1.5 * a - 0.5 * a @ (a.T @ a)

        return a.T if transposed else a

    def update(
        self, param_id: int, params: np.ndarray, gradients: np.ndarray
    ) -> np.ndarray:
        """
        使用 Muon 更新参数。

        参数：
            param_id (int): 参数组的唯一标识符。
            params (np.ndarray): 当前参数。
            gradients (np.ndarray): 参数的梯度。

        返回：
            np.ndarray: 更新后的参数。

        >>> optimizer = Muon(learning_rate=0.1, momentum=0.9)
        >>> params = np.array([[1.0, 2.0], [3.0, 4.0]])
        >>> grads = np.array([[0.1, 0.2], [0.3, 0.4]])
        >>> updated = optimizer.update(0, params, grads)
        >>> updated.shape
        (2, 2)
        """
        if param_id not in self.velocity:
            self.velocity[param_id] = np.zeros_like(params)

        ortho_grad = self.newton_schulz_orthogonalize(gradients)
        self.velocity[param_id] = self.momentum * self.velocity[param_id] + ortho_grad

        return params - self.learning_rate * self.velocity[param_id]


# 使用示例
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Muon Example: Optimizing a 2x2 matrix")

    optimizer = Muon(learning_rate=0.05, momentum=0.9)
    weights = np.array([[1.0, 2.0], [3.0, 4.0]])

    for step in range(10):
        gradients = 0.1 * weights  # 简化后的梯度
        weights = optimizer.update(0, weights, gradients)
        if step % 3 == 0:
            print(f"Step {step}: weights =\n{weights}")

    print(f"Final weights:\n{weights}")
