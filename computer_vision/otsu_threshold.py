import numpy as np
from PIL import Image

"""
用于图像处理的 Otsu 阈值算法。
https://en.wikipedia.org/wiki/Otsu%27s_method
"""


def otsu_threshold(image: Image.Image) -> Image.Image:
    """
    对灰度图像应用 Otsu 阈值处理方法。

    参数：
    image (PIL.Image.Image)：PIL 灰度图像对象。

    返回：
    PIL.Image.Image：应用 Otsu 阈值处理后的二值图像。

    示例：
    >>> from PIL import Image
    >>> import numpy as np
    >>> image_array = np.array(
    ...     [[0, 0, 0, 0], [255, 255, 255, 255], [0, 0, 0, 0], [255, 255, 255, 255]],
    ...     dtype=np.uint8
    ... )
    >>> image = Image.fromarray(image_array)
    >>> binary_image = otsu_threshold(image)
    >>> np.array(binary_image)
    array([[  0,   0,   0,   0],
           [255, 255, 255, 255],
           [  0,   0,   0,   0],
           [255, 255, 255, 255]], dtype=uint8)
    """
    # 将图像转换为 NumPy 数组
    pixel_array = np.array(image)

    # 计算直方图
    hist, _ = np.histogram(pixel_array, bins=256, range=(0, 256))

    # 计算类间方差
    total_pixels = pixel_array.size
    current_max, threshold = 0.0, 0  # 确保 current_max 为浮点数
    sum_total, sum_foreground = 0.0, 0.0  # 确保这些值为浮点数
    weight_background, weight_foreground = 0.0, 0.0  # 确保这些值为浮点数

    for i in range(256):
        sum_total += i * hist[i]

    for i in range(256):
        weight_background += hist[i]
        if weight_background == 0:
            continue
        weight_foreground = total_pixels - weight_background
        if weight_foreground == 0:
            break
        sum_foreground += i * hist[i]

        mean_background = sum_foreground / weight_background
        mean_foreground = (sum_total - sum_foreground) / weight_foreground

        between_class_variance = (
            weight_background
            * weight_foreground
            * (mean_background - mean_foreground) ** 2
        )

        if between_class_variance > current_max:
            current_max = between_class_variance
            threshold = i

    # 对图像应用阈值
    binary_image = pixel_array > threshold
    binary_image = binary_image.astype(np.uint8) * 255

    # 将 NumPy 数组转换回 PIL 图像
    return Image.fromarray(binary_image)
