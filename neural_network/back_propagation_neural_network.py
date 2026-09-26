#!/usr/bin/python

"""

反向传播神经网络（Back Propagation Neural Network，BP）模型框架

易于使用：
    * 可按需添加任意数量的层
    * 可清晰观察损失下降过程
易于扩展：
    * 更多激活函数
    * 更多损失函数
    * 更多优化方法

Author: Stephen Lee
Github : https://github.com/RiptideBo
Date: 2017.11.23

"""

import numpy as np
from matplotlib import pyplot as plt


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


class DenseLayer:
    """
    BP 神经网络的层
    """

    def __init__(
        self, units, activation=None, learning_rate=None, is_input_layer=False
    ) -> None:
        """
        BP 网络的普通全连接层
        :param units: 神经元数量
        :param activation: 激活函数
        :param learning_rate: 参数的学习率
        :param is_input_layer: 是否为输入层
        """
        self.units = units
        self.weight = None
        self.bias = None
        self.activation = activation
        if learning_rate is None:
            learning_rate = 0.3
        self.learn_rate = learning_rate
        self.is_input_layer = is_input_layer

    def initializer(self, back_units) -> None:
        rng = np.random.default_rng()
        self.weight = np.asmatrix(rng.normal(0, 0.5, (self.units, back_units)))
        self.bias = np.asmatrix(rng.normal(0, 0.5, self.units)).T
        if self.activation is None:
            self.activation = sigmoid

    def cal_gradient(self):
        # 激活函数可以是 sigmoid 或线性函数
        if self.activation == sigmoid:
            gradient_mat = np.dot(self.output, (1 - self.output).T)
            gradient_activation = np.diag(np.diag(gradient_mat))
        else:
            gradient_activation = 1
        return gradient_activation

    def forward_propagation(self, xdata):
        self.xdata = xdata
        if self.is_input_layer:
            # 输入层
            self.wx_plus_b = xdata
            self.output = xdata
            return xdata
        else:
            self.wx_plus_b = np.dot(self.weight, self.xdata) - self.bias
            self.output = self.activation(self.wx_plus_b)
            return self.output

    def back_propagation(self, gradient):
        gradient_activation = self.cal_gradient()  # i * i 维
        gradient = np.asmatrix(np.dot(gradient.T, gradient_activation))

        self._gradient_weight = np.asmatrix(self.xdata)
        self._gradient_bias = -1
        self._gradient_x = self.weight

        self.gradient_weight = np.dot(gradient.T, self._gradient_weight.T)
        self.gradient_bias = gradient * self._gradient_bias
        self.gradient = np.dot(gradient, self._gradient_x).T
        # 沿负梯度方向更新
        self.weight = self.weight - self.learn_rate * self.gradient_weight
        self.bias = self.bias - self.learn_rate * self.gradient_bias.T
        # 根据学习率更新权重和偏置（未定义时为 0.3）
        return self.gradient


class BPNN:
    """
    反向传播神经网络模型
    """

    def __init__(self) -> None:
        self.layers = []
        self.train_mse = []
        self.fig_loss = plt.figure()
        self.ax_loss = self.fig_loss.add_subplot(1, 1, 1)

    def add_layer(self, layer) -> None:
        self.layers.append(layer)

    def build(self) -> None:
        for i, layer in enumerate(self.layers[:]):
            if i < 1:
                layer.is_input_layer = True
            else:
                layer.initializer(self.layers[i - 1].units)

    def summary(self) -> None:
        for i, layer in enumerate(self.layers[:]):
            print(f"------- layer {i} -------")
            print("weight.shape ", np.shape(layer.weight))
            print("bias.shape ", np.shape(layer.bias))

    def train(self, xdata, ydata, train_round, accuracy):
        self.train_round = train_round
        self.accuracy = accuracy

        self.ax_loss.hlines(self.accuracy, 0, self.train_round * 1.1)

        x_shape = np.shape(xdata)
        for _ in range(train_round):
            all_loss = 0
            for row in range(x_shape[0]):
                _xdata = np.asmatrix(xdata[row, :]).T
                _ydata = np.asmatrix(ydata[row, :]).T

                # 前向传播
                for layer in self.layers:
                    _xdata = layer.forward_propagation(_xdata)

                loss, gradient = self.cal_loss(_ydata, _xdata)
                all_loss = all_loss + loss

                # 反向传播：输入层不更新
                for layer in self.layers[:0:-1]:
                    gradient = layer.back_propagation(gradient)

            mse = all_loss / x_shape[0]
            self.train_mse.append(mse)

            self.plot_loss()

            if mse < self.accuracy:
                print("----达到精度----")
                return mse
        return None

    def cal_loss(self, ydata, ydata_):
        self.loss = np.sum(np.power((ydata - ydata_), 2))
        self.loss_gradient = 2 * (ydata_ - ydata)
        # 向量（形状与 _ydata.shape 相同）
        return self.loss, self.loss_gradient

    def plot_loss(self) -> None:
        if self.ax_loss.lines:
            self.ax_loss.lines.remove(self.ax_loss.lines[0])
        self.ax_loss.plot(self.train_mse, "r-")
        plt.ion()
        plt.xlabel("step")
        plt.ylabel("loss")
        plt.show()
        plt.pause(0.1)


def example() -> None:
    rng = np.random.default_rng()
    x = rng.normal(size=(10, 10))
    y = np.asarray(
        [
            [0.8, 0.4],
            [0.4, 0.3],
            [0.34, 0.45],
            [0.67, 0.32],
            [0.88, 0.67],
            [0.78, 0.77],
            [0.55, 0.66],
            [0.55, 0.43],
            [0.54, 0.1],
            [0.1, 0.5],
        ]
    )
    model = BPNN()
    for i in (10, 20, 30, 2):
        model.add_layer(DenseLayer(i))
    model.build()
    model.summary()
    model.train(xdata=x, ydata=y, train_round=100, accuracy=0.01)


if __name__ == "__main__":
    example()
