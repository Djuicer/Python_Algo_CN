"""
Horn-Schunck 方法估计图像序列中每个像素的光流（Optical Flow）。
它假设相邻两帧之间亮度恒定，且光流具有平滑性。

参考资料：
Wikipedia: https://en.wikipedia.org/wiki/Horn%E2%80%93Schunck_method
Paper: http://image.diku.dk/imagecanon/material/HornSchunckOptical_Flow.pdf
"""

from typing import SupportsIndex

import numpy as np
from scipy.ndimage import convolve


def warp(
    image: np.ndarray, horizontal_flow: np.ndarray, vertical_flow: np.ndarray
) -> np.ndarray:
    """
    使用水平和垂直光流场将图像像素变换到新图像中。
    从无效位置变换而来的像素设为 0。

    参数：
        image: 灰度图像
        horizontal_flow: 水平光流
        vertical_flow: 垂直光流

    返回：变换后的图像

    >>> warp(np.array([[0, 1, 2], [0, 3, 0], [2, 2, 2]]), \
    np.array([[0, 1, -1], [-1, 0, 0], [1, 1, 1]]), \
    np.array([[0, 0, 0], [0, 1, 0], [0, 0, 1]]))
    array([[0, 0, 0],
           [3, 1, 0],
           [0, 2, 3]])
    """
    flow = np.stack((horizontal_flow, vertical_flow), 2)

    # 创建所有像素坐标的网格，并减去光流以得到目标像素坐标
    grid = np.stack(
        np.meshgrid(np.arange(0, image.shape[1]), np.arange(0, image.shape[0])), 2
    )
    grid = np.round(grid - flow).astype(np.int32)

    # 找出位于原图之外的位置
    invalid = (grid < 0) | (grid >= np.array([image.shape[1], image.shape[0]]))
    grid[invalid] = 0

    warped = image[grid[:, :, 1], grid[:, :, 0]]

    # 将无效位置的像素设为 0
    warped[invalid[:, :, 0] | invalid[:, :, 1]] = 0

    return warped


def horn_schunck(
    image0: np.ndarray,
    image1: np.ndarray,
    num_iter: SupportsIndex,
    alpha: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    本函数执行 Horn-Schunck 算法并返回估计光流。
    假设输入图像为灰度图，且已归一化到 [0, 1]。

    参数：
        image0: 序列中的第一幅图像
        image1: 序列中的第二幅图像
        alpha: 正则化常数
        num_iter: 执行的迭代次数

    返回：估计的水平和垂直光流

    >>> np.round(horn_schunck(np.array([[0, 0, 2], [0, 0, 2]]), \
    np.array([[0, 2, 0], [0, 2, 0]]), alpha=0.1, num_iter=110)).\
    astype(np.int32)
    array([[[ 0, -1, -1],
            [ 0, -1, -1]],
    <BLANKLINE>
           [[ 0,  0,  0],
            [ 0,  0,  0]]], dtype=int32)
    """
    if alpha is None:
        alpha = 0.1

    # 初始化光流
    horizontal_flow = np.zeros_like(image0)
    vertical_flow = np.zeros_like(image0)

    # 准备用于计算导数和平均速度的卷积核
    kernel_x = np.array([[-1, 1], [-1, 1]]) * 0.25
    kernel_y = np.array([[-1, -1], [1, 1]]) * 0.25
    kernel_t = np.array([[1, 1], [1, 1]]) * 0.25
    kernel_laplacian = np.array(
        [[1 / 12, 1 / 6, 1 / 12], [1 / 6, 0, 1 / 6], [1 / 12, 1 / 6, 1 / 12]]
    )

    # 迭代细化光流
    for _ in range(num_iter):
        warped_image = warp(image0, horizontal_flow, vertical_flow)
        derivative_x = convolve(warped_image, kernel_x) + convolve(image1, kernel_x)
        derivative_y = convolve(warped_image, kernel_y) + convolve(image1, kernel_y)
        derivative_t = convolve(warped_image, kernel_t) + convolve(image1, -kernel_t)

        avg_horizontal_velocity = convolve(horizontal_flow, kernel_laplacian)
        avg_vertical_velocity = convolve(vertical_flow, kernel_laplacian)

        # 按论文提出的方法更新光流（步骤 12）
        update = (
            derivative_x * avg_horizontal_velocity
            + derivative_y * avg_vertical_velocity
            + derivative_t
        )
        update = update / (alpha**2 + derivative_x**2 + derivative_y**2)

        horizontal_flow = avg_horizontal_velocity - derivative_x * update
        vertical_flow = avg_vertical_velocity - derivative_y * update

    return horizontal_flow, vertical_flow


if __name__ == "__main__":
    import doctest

    doctest.testmod()
