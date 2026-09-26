import cv2
import numpy as np


def get_neighbors_pixel(
    image: np.ndarray, x_coordinate: int, y_coordinate: int, center: int
) -> int:
    """
    将局部邻域像素值与中心像素的阈值比较。
    当中心像素的邻域值为空（即位于边界）时，需要进行异常处理。

    :param image: 当前处理的图像
    :param x_coordinate: 像素的 x 坐标
    :param y_coordinate: 像素的 y 坐标
    :param center: 中心像素值
    :return: 像素值
    """

    try:
        return int(image[x_coordinate][y_coordinate] >= center)
    except IndexError, TypeError:
        return 0


def local_binary_value(image: np.ndarray, x_coordinate: int, y_coordinate: int) -> int:
    """
    接收图像及 x、y 坐标，返回该坐标处像素局部二值模式的十进制值。

    :param image: 待处理图像
    :param x_coordinate: 像素的 x 坐标
    :param y_coordinate: 像素的 y 坐标
    :return: 中心像素周围各像素二进制值对应的十进制值
    """
    center = image[x_coordinate][y_coordinate]
    powers = [1, 2, 4, 8, 16, 32, 64, 128]

    # 中心值为空时跳过 get_neighbors_pixel
    if center is None:
        return 0

    # 从右上角开始，按顺时针方向为像素赋值
    binary_values = [
        get_neighbors_pixel(image, x_coordinate - 1, y_coordinate + 1, center),
        get_neighbors_pixel(image, x_coordinate, y_coordinate + 1, center),
        get_neighbors_pixel(image, x_coordinate - 1, y_coordinate, center),
        get_neighbors_pixel(image, x_coordinate + 1, y_coordinate + 1, center),
        get_neighbors_pixel(image, x_coordinate + 1, y_coordinate, center),
        get_neighbors_pixel(image, x_coordinate + 1, y_coordinate - 1, center),
        get_neighbors_pixel(image, x_coordinate, y_coordinate - 1, center),
        get_neighbors_pixel(image, x_coordinate - 1, y_coordinate - 1, center),
    ]

    # 将二进制值转换为十进制
    return sum(
        binary_value * power for binary_value, power in zip(binary_values, powers)
    )


if __name__ == "__main__":
    # 读取图像并转换为灰度图
    image = cv2.imread(
        "digital_image_processing/image_data/lena.jpg", cv2.IMREAD_GRAYSCALE
    )

    # 创建与读取图像高度和宽度相同的 NumPy 数组
    lbp_image = np.zeros((image.shape[0], image.shape[1]))

    # 遍历图像并计算每个像素的局部二值模式值
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            lbp_image[i][j] = local_binary_value(image, i, j)

    cv2.imshow("local binary pattern", lbp_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
