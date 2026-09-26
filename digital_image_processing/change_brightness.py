from PIL import Image


def change_brightness(img: Image.Image, level: float) -> Image.Image:
    """
    将 PIL 图像的亮度调整到给定级别。

    参数：
        img: 待调整的 PIL 图像
        level: 亮度调整级别（-255.0 到 255.0）
               负值使图像变暗，正值使图像变亮

    返回：
        调整亮度后的新 PIL 图像

    异常：
        ValueError: level 不在 [-255.0, 255.0] 范围内时抛出

    >>> from PIL import Image
    >>> import numpy as np
    >>> img = Image.new('RGB', (2, 2), color=(100, 100, 100))
    >>> bright = change_brightness(img, 50)
    >>> px = bright.load()
    >>> px[0, 0]
    (150, 150, 150)
    >>> dark = change_brightness(img, -50)
    >>> px_dark = dark.load()
    >>> px_dark[0, 0]
    (50, 50, 50)
    >>> change_brightness(img, 300)
    Traceback (most recent call last):
        ...
    ValueError: level must be between -255.0 (black) and 255.0 (white)
    """

    def brightness(c: int) -> float:
        """
        对每一位执行的基本图像变换/操作。
        """
        return 128 + level + (c - 128)

    if not -255.0 <= level <= 255.0:
        raise ValueError("level must be between -255.0 (black) and 255.0 (white)")
    return img.point(brightness)


if __name__ == "__main__":
    # 加载图像
    with Image.open("image_data/lena.jpg") as img:
        # 将亮度调整为 100
        brigt_img = change_brightness(img, 100)
        brigt_img.save("image_data/lena_brightness.png", format="png")
