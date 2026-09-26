"""
使用 Gram 矩阵重建图像风格。

https://en.wikipedia.org/wiki/Gram_matrix
https://en.wikipedia.org/wiki/Neural_style_transfer
https://arxiv.org/pdf/1603.08155#page=7&zoom=auto,-294,3
"""

import numpy as np


def gram_matrix(mat: np.ndarray) -> np.ndarray:
    """
    返回图像的 Gram 矩阵（Gramian Matrix）。

    :param mat: 形状为 (C, H, W) 的矩阵；C = 颜色通道数，H = 高度，W = 宽度。
    :type mat: np.ndarray
    :return: 形状为 (C, C) 的矩阵。
    :rtype: np.ndarray

    示例
    --------
    >>> gram_matrix(np.ones((2,5,5)))
    array([[0.5, 0.5],
           [0.5, 0.5]])
    >>> gram_matrix(np.ones((3,5,5)))
    array([[0.33333333, 0.33333333, 0.33333333],
           [0.33333333, 0.33333333, 0.33333333],
           [0.33333333, 0.33333333, 0.33333333]])
    >>> gram_matrix(np.ones((3,5,5))).shape
    (3, 3)
    """
    color, height, width = mat.shape
    vec = mat.reshape(color, height * width)
    gram = vec @ vec.T
    return gram / (color * height * width)


def gram_loss(input_features: np.ndarray, reference_features: np.ndarray) -> np.float64:
    """
    计算输入图像与参考图像 Gram 矩阵之差的 Frobenius 范数平方。

    :param input_features: 形状为 (C, H, W) 的特征图
    :type input_features: np.ndarray
    :param reference_features: 形状为 (C, H, W) 的特征图
    :type reference_features: np.ndarray
    :return: 两个特征图之间的 Gram 损失。
    :rtype: float64

    示例
    --------
    >>> a = np.random.randn(3,5,5)
    >>> gram_loss(a, a)
    np.float64(0.0)
    >>> a = np.zeros((3,5,5))
    >>> b = np.ones((3,5,5))
    >>> gram_loss(a, b)
    np.float64(1.0)
    """
    input_gram = gram_matrix(input_features)
    reference_gram = gram_matrix(reference_features)
    return np.sum(np.square(input_gram - reference_gram)).astype(np.float64)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
