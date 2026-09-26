"""
中值滤波（Median Filter）算法的实现。
"""

from cv2 import COLOR_BGR2GRAY, cvtColor, imread, imshow, waitKey
from numpy import divide, int8, multiply, ravel, sort, zeros_like


def median_filter(gray_img, mask=3):
    """
    :param gray_img: 灰度图像
    :param mask: 掩码大小
    :return: 经中值滤波后的图像
    """
    # 设置图像边界
    bd = int(mask / 2)
    # 复制图像尺寸
    median_img = zeros_like(gray_img)
    for i in range(bd, gray_img.shape[0] - bd):
        for j in range(bd, gray_img.shape[1] - bd):
            # 根据 mask 获取掩码
            kernel = ravel(gray_img[i - bd : i + bd + 1, j - bd : j + bd + 1])
            # 计算掩码区域的中值
            median = sort(kernel)[int8(divide((multiply(mask, mask)), 2) + 1)]
            median_img[i, j] = median
    return median_img


if __name__ == "__main__":
    # 读取原始图像
    img = imread("../image_data/lena.jpg")
    # 将图像转换为灰度值
    gray = cvtColor(img, COLOR_BGR2GRAY)

    # 使用两种不同掩码大小获取结果
    median3x3 = median_filter(gray, 3)
    median5x5 = median_filter(gray, 5)

    # 显示结果图像
    imshow("median filter with 3x3 mask", median3x3)
    imshow("median filter with 5x5 mask", median5x5)
    waitKey(0)
