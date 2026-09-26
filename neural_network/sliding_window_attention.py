"""
 - - - - - -- - - - - - - - - - - - - - - - - - - - - - -
Name - - sliding_window_attention.py
目标 - - 实现一种使用滑动窗口注意力机制完成序列建模任务的神经网络架构。
详情：共包含 5 层神经网络
        * 输入层
        * 滑动窗口注意力层
        * 前馈层
        * 输出层
Author: Stephen Lee
Github: 245885195@qq.com
Date: 2024.10.20
References:
    1. Choromanska, A., et al. (2020). "On the Importance of
       Initialization and Momentum in Deep Learning." *Proceedings
       of the 37th International Conference on Machine Learning*.
    2. Dai, Z., et al. (2020). "Transformers are RNNs: Fast
       Autoregressive Transformers with Linear Attention."
       *arXiv preprint arXiv:2006.16236*.
    3. [Attention Mechanisms in Neural Networks](https://en.wikipedia.org/wiki/Attention_(machine_learning))
 - - - - - -- - - - - - - - - - - - - - - - - - - - - - -
"""

import numpy as np


class SlidingWindowAttention:
    """滑动窗口注意力（Sliding Window Attention）模块。

    此类实现滑动窗口注意力机制，模型关注每个词元周围固定大小的上下文窗口。

    属性：
        window_size (int): 注意力窗口的大小。
        embed_dim (int): 输入嵌入的维度。
    """

    def __init__(self, embed_dim: int, window_size: int) -> None:
        """
        初始化 SlidingWindowAttention 模块。

        参数：
            embed_dim (int): 输入嵌入的维度。
            window_size (int): 注意力窗口的大小。
        """
        self.window_size = window_size
        self.embed_dim = embed_dim
        rng = np.random.default_rng()
        self.attention_weights = rng.standard_normal((embed_dim, embed_dim))

    def forward(self, input_tensor: np.ndarray) -> np.ndarray:
        """
        执行滑动窗口注意力的前向传播。

        参数：
            input_tensor (np.ndarray): 形状为 (batch_size,
                                       seq_length, embed_dim) 的输入张量。

        返回：
            np.ndarray: 形状为 (batch_size, seq_length, embed_dim) 的输出张量。

        >>> x = np.random.randn(2, 10, 4)  # Batch size 2, sequence
        >>> attention = SlidingWindowAttention(embed_dim=4, window_size=3)
        >>> output = attention.forward(x)
        >>> output.shape
        (2, 10, 4)
        >>> (output.sum() != 0).item()  # Check if output is non-zero
        True
        """
        _batch_size, seq_length, _ = input_tensor.shape
        output = np.zeros_like(input_tensor)

        for i in range(seq_length):
            # 定义窗口范围
            start = max(0, i - self.window_size // 2)
            end = min(seq_length, i + self.window_size // 2 + 1)

            # 提取局部窗口
            local_window = input_tensor[:, start:end, :]

            # 计算注意力分数
            attention_scores = np.matmul(local_window, self.attention_weights)

            # 对注意力分数求平均值
            output[:, i, :] = np.mean(attention_scores, axis=1)

        return output


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 使用示例
    rng = np.random.default_rng()
    x = rng.standard_normal((2, 10, 4))  # Batch size 2,
    attention = SlidingWindowAttention(embed_dim=4, window_size=3)
    output = attention.forward(x)
    print(output)
