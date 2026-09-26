from pathlib import Path

import cv2
import numpy as np
from matplotlib import pyplot as plt


def get_rotation(
    img: np.ndarray, pt1: np.ndarray, pt2: np.ndarray, rows: int, cols: int
) -> np.ndarray:
    """
    获取旋转后的图像
    :param img: np.ndarray
    :param pt1: 3x2 list
    :param pt2: 3x2 list
    :param rows: 图像列数
    :param cols: 图像行数
    :return: np.ndarray
    """
    matrix = cv2.getAffineTransform(pt1, pt2)
    return cv2.warpAffine(img, matrix, (rows, cols))


if __name__ == "__main__":
    # 读取原始图像
    image = cv2.imread(
        str(Path(__file__).resolve().parent.parent / "image_data" / "lena.jpg")
    )
    # 将图像转换为灰度值
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 获取图像形状
    img_rows, img_cols = gray_img.shape

    # 设置不同的点以旋转图像
    pts1 = np.array([[50, 50], [200, 50], [50, 200]], np.float32)
    pts2 = np.array([[10, 100], [200, 50], [100, 250]], np.float32)
    pts3 = np.array([[50, 50], [150, 50], [120, 200]], np.float32)
    pts4 = np.array([[10, 100], [80, 50], [180, 250]], np.float32)

    # 将所有旋转后的图像加入列表
    images = [
        gray_img,
        get_rotation(gray_img, pts1, pts2, img_rows, img_cols),
        get_rotation(gray_img, pts2, pts3, img_rows, img_cols),
        get_rotation(gray_img, pts2, pts4, img_rows, img_cols),
    ]

    # 绘制不同的图像旋转结果
    fig = plt.figure(1)
    titles = ["Original", "Rotation 1", "Rotation 2", "Rotation 3"]
    for i, image in enumerate(images):
        plt.subplot(2, 2, i + 1), plt.imshow(image, "gray")
        plt.title(titles[i])
        plt.axis("off")
        plt.subplots_adjust(left=0.0, bottom=0.05, right=1.0, top=0.95)
    plt.show()
