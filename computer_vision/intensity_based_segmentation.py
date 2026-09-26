# Source: "https://www.ijcse.com/docs/IJCSE11-02-03-117.pdf"

# 导入必要的库
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def segment_image(image: np.ndarray, thresholds: list[int]) -> np.ndarray:
    """
    根据强度阈值执行图像分割（Image Segmentation）。

    参数：
        image: 以二维数组表示的输入灰度图像。
        thresholds: 用于定义分割区域的强度阈值。

    返回：
        带标签的二维数组，其中每个区域对应一个阈值范围。

    示例：
        >>> img = np.array([[80, 120, 180], [40, 90, 150], [20, 60, 100]])
        >>> segment_image(img, [50, 100, 150])
        array([[1, 2, 3],
               [0, 1, 2],
               [0, 1, 1]], dtype=int32)
    """
    # 使用零初始化分割结果数组
    segmented = np.zeros_like(image, dtype=np.int32)

    # 根据阈值分配标签
    for i, threshold in enumerate(thresholds):
        segmented[image > threshold] = i + 1

    return segmented


if __name__ == "__main__":
    # 加载图像
    image_path = "path_to_image"  # 替换为实际图像路径
    original_image = Image.open(image_path).convert("L")
    image_array = np.array(original_image)

    # 定义阈值
    thresholds = [50, 100, 150, 200]

    # 执行图像分割
    segmented_image = segment_image(image_array, thresholds)

    # 显示结果
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(image_array, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Segmented Image")
    plt.imshow(segmented_image, cmap="tab20")
    plt.axis("off")

    plt.show()
