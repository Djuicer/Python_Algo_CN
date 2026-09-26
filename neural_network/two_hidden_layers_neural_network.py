"""
参考资料：
    - http://neuralnetworksanddeeplearning.com/chap2.html （反向传播）
    - https://en.wikipedia.org/wiki/Sigmoid_function （Sigmoid 激活函数）
    - https://en.wikipedia.org/wiki/Feedforward_neural_network （前馈网络）
"""

import numpy as np


class TwoHiddenLayerNeuralNetwork:
    def __init__(self, input_array: np.ndarray, output_array: np.ndarray) -> None:
        """
        此函数使用各层的随机权重初始化 TwoHiddenLayerNeuralNetwork 类，
        并将预测输出初始化为零。

        input_array：用于训练神经网络的输入值，即训练数据。
        output_array：给定输入的预期输出值。
        """

        # 用于训练模型的输入值
        self.input_array = input_array

        # 分配随机初始权重，其中第一个参数是前一层的节点数，
        # 第二个参数是后一层的节点数。

        # 分配随机初始权重
        # self.input_array.shape[1] 表示输入层的节点数
        # 第一个隐藏层包含 4 个节点
        rng = np.random.default_rng()
        self.input_layer_and_first_hidden_layer_weights = rng.random(
            (self.input_array.shape[1], 4)
        )

        # 第一个隐藏层的随机初始值
        # 第一个隐藏层有 4 个节点
        # 第二个隐藏层有 3 个节点
        self.first_hidden_layer_and_second_hidden_layer_weights = rng.random((4, 3))

        # 第二个隐藏层的随机初始值
        # 第二个隐藏层有 3 个节点
        # 输出层有 1 个节点
        self.second_hidden_layer_and_output_layer_weights = rng.random((3, 1))

        # 给定的真实输出值
        self.output_array = output_array

        # 神经网络的预测输出值
        # predicted_output 数组初始时全部为零
        self.predicted_output = np.zeros(output_array.shape)

    def feedforward(self) -> np.ndarray:
        """
        信息仅沿一个方向传递，即从输入节点向前经过两个隐藏层到达输出节点。
        网络中不存在环或循环。

        返回 layer_between_second_hidden_layer_and_output，
            即神经网络的最后一层。

        >>> input_val = np.array(([0, 0, 0], [0, 0, 0], [0, 0, 0]), dtype=float)
        >>> output_val = np.array(([0], [0], [0]), dtype=float)
        >>> nn = TwoHiddenLayerNeuralNetwork(input_val, output_val)
        >>> res = nn.feedforward()
        >>> array_sum = np.sum(res)
        >>> bool(np.isnan(array_sum))
        False
        """
        # layer_between_input_and_first_hidden_layer 是连接输入节点与
        # 第一个隐藏层节点的层
        self.layer_between_input_and_first_hidden_layer = sigmoid(
            np.dot(self.input_array, self.input_layer_and_first_hidden_layer_weights)
        )

        # layer_between_first_hidden_layer_and_second_hidden_layer 是连接
        # 第一组隐藏节点与第二组隐藏节点的层
        self.layer_between_first_hidden_layer_and_second_hidden_layer = sigmoid(
            np.dot(
                self.layer_between_input_and_first_hidden_layer,
                self.first_hidden_layer_and_second_hidden_layer_weights,
            )
        )

        # layer_between_second_hidden_layer_and_output 是连接第二个隐藏层与
        # 输出节点的层
        self.layer_between_second_hidden_layer_and_output = sigmoid(
            np.dot(
                self.layer_between_first_hidden_layer_and_second_hidden_layer,
                self.second_hidden_layer_and_output_layer_weights,
            )
        )

        return self.layer_between_second_hidden_layer_and_output

    def back_propagation(self) -> None:
        """
        根据上一轮（即上一次迭代）得到的误差率微调神经网络权重。
        使用 sigmoid 激活函数的导数执行更新。

        >>> input_val = np.array(([0, 0, 0], [0, 0, 0], [0, 0, 0]), dtype=float)
        >>> output_val = np.array(([0], [0], [0]), dtype=float)
        >>> nn = TwoHiddenLayerNeuralNetwork(input_val, output_val)
        >>> res = nn.feedforward()
        >>> nn.back_propagation()
        >>> updated_weights = nn.second_hidden_layer_and_output_layer_weights
        >>> bool((res == updated_weights).all())
        False
        """

        updated_second_hidden_layer_and_output_layer_weights = np.dot(
            self.layer_between_first_hidden_layer_and_second_hidden_layer.T,
            2
            * (self.output_array - self.predicted_output)
            * sigmoid_derivative(self.predicted_output),
        )
        updated_first_hidden_layer_and_second_hidden_layer_weights = np.dot(
            self.layer_between_input_and_first_hidden_layer.T,
            np.dot(
                2
                * (self.output_array - self.predicted_output)
                * sigmoid_derivative(self.predicted_output),
                self.second_hidden_layer_and_output_layer_weights.T,
            )
            * sigmoid_derivative(
                self.layer_between_first_hidden_layer_and_second_hidden_layer
            ),
        )
        updated_input_layer_and_first_hidden_layer_weights = np.dot(
            self.input_array.T,
            np.dot(
                np.dot(
                    2
                    * (self.output_array - self.predicted_output)
                    * sigmoid_derivative(self.predicted_output),
                    self.second_hidden_layer_and_output_layer_weights.T,
                )
                * sigmoid_derivative(
                    self.layer_between_first_hidden_layer_and_second_hidden_layer
                ),
                self.first_hidden_layer_and_second_hidden_layer_weights.T,
            )
            * sigmoid_derivative(self.layer_between_input_and_first_hidden_layer),
        )

        self.input_layer_and_first_hidden_layer_weights += (
            updated_input_layer_and_first_hidden_layer_weights
        )
        self.first_hidden_layer_and_second_hidden_layer_weights += (
            updated_first_hidden_layer_and_second_hidden_layer_weights
        )
        self.second_hidden_layer_and_output_layer_weights += (
            updated_second_hidden_layer_and_output_layer_weights
        )

    def train(self, output: np.ndarray, iterations: int, give_loss: bool) -> None:
        """
        按给定迭代次数执行前馈和反向传播过程。
        每次迭代都会更新神经网络的权重。

        output：用于计算损失的真实输出值。
        iterations：权重更新次数。
        give_loss：布尔值；为 True 时打印每次迭代的损失，
                   为 False 时不打印。

        >>> input_val = np.array(([0, 0, 0], [0, 1, 0], [0, 0, 1]), dtype=float)
        >>> output_val = np.array(([0], [1], [1]), dtype=float)
        >>> nn = TwoHiddenLayerNeuralNetwork(input_val, output_val)
        >>> first_iteration_weights = nn.feedforward()
        >>> nn.back_propagation()
        >>> updated_weights = nn.second_hidden_layer_and_output_layer_weights
        >>> bool((first_iteration_weights == updated_weights).all())
        False
        """
        for iteration in range(1, iterations + 1):
            self.output = self.feedforward()
            self.back_propagation()
            if give_loss:
                loss = np.mean(np.square(output - self.feedforward()))
                print(f"Iteration {iteration} Loss: {loss}")

    def predict(self, input_arr: np.ndarray) -> int:
        """
        使用训练后的神经网络预测给定输入值的输出。

        模型给出的输出值位于 0 和 1 之间。由于真实输出值为二值，
        当模型值大于阈值时，predict 函数返回 1，否则返回 0。

        >>> input_val = np.array(([0, 0, 0], [0, 1, 0], [0, 0, 1]), dtype=float)
        >>> output_val = np.array(([0], [1], [1]), dtype=float)
        >>> nn = TwoHiddenLayerNeuralNetwork(input_val, output_val)
        >>> nn.train(output_val, 1000, False)
        >>> nn.predict([0, 1, 0]) in (0, 1)
        True
        """

        # 要进行预测的输入值
        self.array = input_arr

        self.layer_between_input_and_first_hidden_layer = sigmoid(
            np.dot(self.array, self.input_layer_and_first_hidden_layer_weights)
        )

        self.layer_between_first_hidden_layer_and_second_hidden_layer = sigmoid(
            np.dot(
                self.layer_between_input_and_first_hidden_layer,
                self.first_hidden_layer_and_second_hidden_layer_weights,
            )
        )

        self.layer_between_second_hidden_layer_and_output = sigmoid(
            np.dot(
                self.layer_between_first_hidden_layer_and_second_hidden_layer,
                self.second_hidden_layer_and_output_layer_weights,
            )
        )

        return int((self.layer_between_second_hidden_layer_and_output > 0.6)[0])


def sigmoid(value: np.ndarray) -> np.ndarray:
    """
    应用 sigmoid 激活函数。

    返回归一化后的值

    >>> sigmoid(np.array(([1, 0, 2], [1, 0, 0]), dtype=np.float64))
    array([[0.73105858, 0.5       , 0.88079708],
           [0.73105858, 0.5       , 0.5       ]])
    """
    return 1 / (1 + np.exp(-value))


def sigmoid_derivative(value: np.ndarray) -> np.ndarray:
    """
    计算 sigmoid 函数的导数值。

    返回 sigmoid 值的导数

    >>> sigmoid_derivative(np.array(([1, 0, 2], [1, 0, 0]), dtype=np.float64))
    array([[ 0.,  0., -2.],
           [ 0.,  0.,  0.]])
    """
    return (value) * (1 - (value))


def example() -> int:
    """
    演示如何使用神经网络类及相应方法获得所需输出。
    调用 TwoHiddenLayerNeuralNetwork 类，并向模型提供固定的输入和输出值。
    模型训练固定次数后调用 predict 方法。
    本示例执行二分类，两个类别分别由 '0' 和 '1' 表示。

    >>> example() in (0, 1)
    True
    """
    # 输入值
    test_input = np.array(
        (
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1],
        ),
        dtype=np.float64,
    )

    # 给定输入值对应的真实输出值
    output = np.array(([0], [1], [1], [0], [1], [0], [0], [1]), dtype=np.float64)

    # 调用神经网络类
    neural_network = TwoHiddenLayerNeuralNetwork(
        input_array=test_input, output_array=output
    )

    # 调用训练函数
    # 如需查看每次迭代的损失，请将 give_loss 设置为 True
    neural_network.train(output=output, iterations=10, give_loss=False)

    return neural_network.predict(np.array(([1, 1, 1]), dtype=np.float64))


if __name__ == "__main__":
    example()
