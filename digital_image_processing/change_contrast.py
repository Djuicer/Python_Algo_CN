"""
使用 PIL 调整对比度

此算法用于
https://noivce.pythonanywhere.com/ Python web app.

psf/black: True
ruff : True
"""

from PIL import Image


def change_contrast(img: Image.Image, level: int) -> Image.Image:
    """
    调整对比度的函数。
    """
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(c: int) -> int:
        """
        对每一位执行的基本图像变换/操作。
        """
        return int(128 + factor * (c - 128))

    return img.point(contrast)


if __name__ == "__main__":
    # 加载图像
    with Image.open("image_data/lena.jpg") as img:
        # 将对比度调整为 170
        cont_img = change_contrast(img, 170)
        cont_img.save("image_data/lena_high_contrast.png", format="png")
