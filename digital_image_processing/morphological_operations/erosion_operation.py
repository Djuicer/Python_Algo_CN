from pathlib import Path

import numpy as np
from PIL import Image


def rgb_to_gray(rgb: np.ndarray) -> np.ndarray:
    """
    将 RGB 图像转换为灰度图像

    >>> rgb_to_gray(np.array([[[127, 255, 0]]]))
    array([[187.6453]])
    >>> rgb_to_gray(np.array([[[0, 0, 0]]]))
    array([[0.]])
    >>> rgb_to_gray(np.array([[[2, 4, 1]]]))
    array([[3.0598]])
    >>> rgb_to_gray(np.array([[[26, 255, 14], [5, 147, 20], [1, 200, 0]]]))
    array([[159.0524,  90.0635, 117.6989]])
    """
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    return 0.2989 * r + 0.5870 * g + 0.1140 * b


def gray_to_binary(gray: np.ndarray) -> np.ndarray:
    """
    将灰度图像转换为二值图像

    >>> gray_to_binary(np.array([[127, 255, 0]]))
    array([[False,  True, False]])
    >>> gray_to_binary(np.array([[0]]))
    array([[False]])
    >>> gray_to_binary(np.array([[26.2409, 4.9315, 1.4729]]))
    array([[False, False, False]])
    >>> gray_to_binary(np.array([[26, 255, 14], [5, 147, 20], [1, 200, 0]]))
    array([[False,  True, False],
           [False,  True, False],
           [False,  True, False]])
    """
    return (gray > 127) & (gray <= 255)


def erosion(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    返回腐蚀后的图像

    >>> erosion(np.array([[True, True, False]]), np.array([[0, 1, 0]]))
    array([[False, False, False]])
    >>> erosion(np.array([[True, False, False]]), np.array([[1, 1, 0]]))
    array([[False, False, False]])
    """
    output = np.zeros_like(image)
    image_padded = np.zeros(
        (image.shape[0] + kernel.shape[0] - 1, image.shape[1] + kernel.shape[1] - 1)
    )

    # 将图像复制到填充后的图像中
    image_padded[kernel.shape[0] - 2 : -1 :, kernel.shape[1] - 2 : -1 :] = image

    # 遍历图像并应用卷积核
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            summation = (
                kernel * image_padded[y : y + kernel.shape[0], x : x + kernel.shape[1]]
            ).sum()
            output[y, x] = int(summation == 5)
    return output


if __name__ == "__main__":
    # 读取原始图像
    lena_path = Path(__file__).resolve().parent / "image_data" / "lena.jpg"
    lena = np.array(Image.open(lena_path))

    # 待应用的结构元素
    structuring_element = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

    # 对二值图像执行腐蚀操作
    output = erosion(gray_to_binary(rgb_to_gray(lena)), structuring_element)

    # 保存输出图像
    pil_img = Image.fromarray(output).convert("RGB")
    pil_img.save("result_erosion.png")
