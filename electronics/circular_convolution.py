# https://en.wikipedia.org/wiki/Circular_convolution

"""
圆周卷积（Circular Convolution）也称循环卷积，是周期卷积的一种特殊情况，
即两个具有相同周期的周期函数之间的卷积。例如，周期卷积会出现在离散时间
傅里叶变换（DTFT）中。具体而言，两个离散序列乘积的 DTFT，等于这两个序列
各自 DTFT 的周期卷积。每个 DTFT 又是连续傅里叶变换函数的周期求和。

来源：https://en.wikipedia.org/wiki/Circular_convolution
"""

import doctest
from collections import deque

import numpy as np


class CircularConvolution:
    """
    此类存储第一路和第二路信号，并执行圆周卷积。
    """

    def __init__(self) -> None:
        """
        第一路和第二路信号以一维数组形式存储。
        """

        self.first_signal = [2, 1, 2, -1]
        self.second_signal = [1, 2, 3, 4]

    def circular_convolution(self) -> list[float]:
        """
        使用矩阵法对第一路和第二路信号执行圆周卷积。

        用法：
        >>> convolution = CircularConvolution()
        >>> convolution.circular_convolution()
        [10.0, 10.0, 6.0, 14.0]

        >>> convolution.first_signal = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
        >>> convolution.second_signal = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
        >>> convolution.circular_convolution()
        [5.2, 6.0, 6.48, 6.64, 6.48, 6.0, 5.2, 4.08]

        >>> convolution.first_signal = [-1, 1, 2, -2]
        >>> convolution.second_signal = [0.5, 1, -1, 2, 0.75]
        >>> convolution.circular_convolution()
        [6.25, -3.0, 1.5, -2.0, -2.75]

        >>> convolution.first_signal = [1, -1, 2, 3, -1]
        >>> convolution.second_signal = [1, 2, 3]
        >>> convolution.circular_convolution()
        [8.0, -2.0, 3.0, 4.0, 11.0]

        """

        length_first_signal = len(self.first_signal)
        length_second_signal = len(self.second_signal)

        max_length = max(length_first_signal, length_second_signal)

        # 创建 max_length × max_length 的零矩阵
        matrix = [[0] * max_length for i in range(max_length)]

        # 用零填充较短的信号，使两路信号长度相同
        if length_first_signal < length_second_signal:
            self.first_signal += [0] * (max_length - length_first_signal)
        elif length_first_signal > length_second_signal:
            self.second_signal += [0] * (max_length - length_second_signal)

        """
        假设 'x' 是长度为 4 的信号，按以下方式填充矩阵：
        [
            [x[0], x[3], x[2], x[1]],
            [x[1], x[0], x[3], x[2]],
            [x[2], x[1], x[0], x[3]],
            [x[3], x[2], x[1], x[0]]
        ]
        """
        for i in range(max_length):
            rotated_signal = deque(self.second_signal)
            rotated_signal.rotate(i)
            for j, item in enumerate(rotated_signal):
                matrix[i][j] += item

        # 将矩阵与第一路信号相乘
        final_signal = np.matmul(np.transpose(matrix), np.transpose(self.first_signal))

        # 四舍五入到小数点后两位
        return [float(round(i, 2)) for i in final_signal]


if __name__ == "__main__":
    doctest.testmod()
