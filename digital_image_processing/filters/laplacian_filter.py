# @Author  : ojas-wani
# @File    : laplacian_filter.py
# @Date    : 10/04/2023

import numpy as np
from cv2 import (
    BORDER_DEFAULT,
    COLOR_BGR2GRAY,
    CV_64F,
    cvtColor,
    filter2D,
    imread,
    imshow,
    waitKey,
)

from digital_image_processing.filters.gaussian_filter import gaussian_filter


def my_laplacian(src: np.ndarray, ksize: int) -> np.ndarray:
    """
    :param src: 源图像，应为灰度或彩色图像。
    :param ksize: 用于计算 Laplacian 滤波的卷积核大小，可取 1、3、5 或 7。

    >>> my_laplacian(src=np.array([]), ksize=0)
    Traceback (most recent call last):
        ...
    ValueError: ksize must be in (1, 3, 5, 7)
    """
    kernels = {
        1: np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]),
        3: np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]]),
        5: np.array(
            [
                [0, 0, -1, 0, 0],
                [0, -1, -2, -1, 0],
                [-1, -2, 16, -2, -1],
                [0, -1, -2, -1, 0],
                [0, 0, -1, 0, 0],
            ]
        ),
        7: np.array(
            [
                [0, 0, 0, -1, 0, 0, 0],
                [0, 0, -2, -3, -2, 0, 0],
                [0, -2, -7, -10, -7, -2, 0],
                [-1, -3, -10, 68, -10, -3, -1],
                [0, -2, -7, -10, -7, -2, 0],
                [0, 0, -2, -3, -2, 0, 0],
                [0, 0, 0, -1, 0, 0, 0],
            ]
        ),
    }
    if ksize not in kernels:
        msg = f"ksize must be in {tuple(kernels)}"
        raise ValueError(msg)

    # 使用卷积应用 Laplacian 卷积核
    return filter2D(
        src, CV_64F, kernels[ksize], 0, borderType=BORDER_DEFAULT, anchor=(0, 0)
    )


if __name__ == "__main__":
    # 读取原始图像
    img = imread(r"../image_data/lena.jpg")

    # 将图像转换为灰度值
    gray = cvtColor(img, COLOR_BGR2GRAY)

    # 应用高斯滤波
    blur_image = gaussian_filter(gray, 3, sigma=1)

    # 应用多个卷积核检测边缘
    laplacian_image = my_laplacian(ksize=3, src=blur_image)

    imshow("Original image", img)
    imshow("Detected edges using laplacian filter", laplacian_image)

    waitKey(0)
