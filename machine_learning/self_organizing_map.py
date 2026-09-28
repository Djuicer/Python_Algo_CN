"""
https://en.wikipedia.org/wiki/Self-organizing_map
"""

import math


class SelfOrganizingMap:
    def get_winner(self, weights: list[list[float]], sample: list[int]) -> int:
        """
        使用欧几里得距离计算获胜向量

        >>> SelfOrganizingMap().get_winner([[1, 2, 3], [4, 5, 6]], [1, 2, 3])
        1
        """
        d0 = 0.0
        d1 = 0.0
        for i in range(len(sample)):
            d0 += math.pow((sample[i] - weights[0][i]), 2)
            d1 += math.pow((sample[i] - weights[1][i]), 2)
            return 0 if d0 > d1 else 1
        return 0

    def update(
        self, weights: list[list[int | float]], sample: list[int], j: int, alpha: float
    ) -> list[list[int | float]]:
        """
        更新获胜向量。

        >>> SelfOrganizingMap().update([[1, 2, 3], [4, 5, 6]], [1, 2, 3], 1, 0.1)
        [[1, 2, 3], [3.7, 4.7, 6]]
        """
        for i in range(len(weights)):
            weights[j][i] += alpha * (sample[i] - weights[j][i])
        return weights


# 驱动代码
def main() -> None:
    # 训练样本 (m, n)
    training_samples = [[1, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 0, 1, 1]]

    # 权重初始化 (n, C)
    weights = [[0.2, 0.6, 0.5, 0.9], [0.8, 0.4, 0.7, 0.3]]

    # 训练
    self_organizing_map = SelfOrganizingMap()
    epochs = 3
    alpha = 0.5

    for _ in range(epochs):
        for j in range(len(training_samples)):
            # 训练样本
            sample = training_samples[j]

            # 计算获胜向量
            winner = self_organizing_map.get_winner(weights, sample)

            # Update the winning vector
            weights = self_organizing_map.update(weights, sample, winner, alpha)

    # 对测试样本进行分类
    sample = [0, 0, 0, 1]
    winner = self_organizing_map.get_winner(weights, sample)

    # 结果
    print(f"Clusters that the test sample belongs to : {winner}")
    print(f"Weights that have been trained : {weights}")


# 运行 main() 函数
if __name__ == "__main__":
    main()
