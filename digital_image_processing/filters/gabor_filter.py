# Gabor 滤波器的实现
# https://en.wikipedia.org/wiki/Gabor_filter
import numpy as np
from cv2 import COLOR_BGR2GRAY, CV_8UC3, cvtColor, filter2D, imread, imshow, waitKey


def gabor_filter_kernel(
    ksize: int, sigma: int, theta: int, lambd: int, gamma: int, psi: int
) -> np.ndarray:
    """
    :param ksize:   卷积滤波器的核大小（ksize x ksize）
    :param sigma:   高斯钟形曲线的标准差
    :param theta:   Gabor 函数平行条纹法线的方向
    :param lambd:   正弦分量的波长
    :param gamma:   空间纵横比，用于指定 Gabor 函数支撑域的椭圆率
    :param psi:     正弦函数的相位偏移

    >>> gabor_filter_kernel(3, 8, 0, 10, 0, 0).tolist()
    [[0.8027212023735046, 1.0, 0.8027212023735046], [0.8027212023735046, 1.0, \
0.8027212023735046], [0.8027212023735046, 1.0, 0.8027212023735046]]

    """

    # 准备卷积核
    # 卷积核大小必须为奇数
    if (ksize % 2) == 0:
        ksize = ksize + 1
    gabor = np.zeros((ksize, ksize), dtype=np.float32)

    # 计算各元素
    for y in range(ksize):
        for x in range(ksize):
            # 到中心的距离
            px = x - ksize // 2
            py = y - ksize // 2

            # 角度转弧度
            _theta = theta / 180 * np.pi
            cos_theta = np.cos(_theta)
            sin_theta = np.sin(_theta)

            # 计算卷积核的 x 坐标
            _x = cos_theta * px + sin_theta * py

            # 计算卷积核的 y 坐标
            _y = -sin_theta * px + cos_theta * py

            # 填充卷积核
            gabor[y, x] = np.exp(-(_x**2 + gamma**2 * _y**2) / (2 * sigma**2)) * np.cos(
                2 * np.pi * _x / lambd + psi
            )

    return gabor


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # 读取原始图像
    img = imread("../image_data/lena.jpg")
    # 将图像转换为灰度值
    gray = cvtColor(img, COLOR_BGR2GRAY)

    # 应用多个卷积核检测边缘
    out = np.zeros(gray.shape[:2])
    for theta in [0, 30, 60, 90, 120, 150]:
        """
        ksize = 10
        sigma = 8
        lambd = 10
        gamma = 0
        psi = 0
        """
        kernel_10 = gabor_filter_kernel(10, 8, theta, 10, 0, 0)
        out += filter2D(gray, CV_8UC3, kernel_10)
    out = out / out.max() * 255
    out = out.astype(np.uint8)

    imshow("Original", gray)
    imshow("Gabor filter with 20x20 mask and 6 directions", out)

    waitKey(0)
