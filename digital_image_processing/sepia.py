"""
使用 OpenCV 实现棕褐色调图像处理算法
"""

from cv2 import destroyAllWindows, imread, imshow, waitKey


def make_sepia(img, factor: int):
    """
    为图像添加棕褐色调。
    来源：https://en.wikipedia.org/wiki/Sepia_(color)
    """
    pixel_h, pixel_v = img.shape[0], img.shape[1]

    def to_grayscale(blue, green, red):
        """
        生成像素灰度表示的辅助函数
        来源：https://pl.wikipedia.org/wiki/YUV
        """
        return 0.2126 * red + 0.587 * green + 0.114 * blue

    def normalize(value):
        """归一化 R/G/B 值的辅助函数：当值大于 255 时返回 255"""
        return min(value, 255)

    for i in range(pixel_h):
        for j in range(pixel_v):
            greyscale = int(to_grayscale(*img[i][j]))
            img[i][j] = [
                normalize(greyscale),
                normalize(greyscale + factor),
                normalize(greyscale + 2 * factor),
            ]

    return img


if __name__ == "__main__":
    # 读取原始图像
    images = {
        percentage: imread("image_data/lena.jpg", 1) for percentage in (10, 20, 30, 40)
    }

    for percentage, img in images.items():
        make_sepia(img, percentage)

    for percentage, img in images.items():
        imshow(f"Original image with sepia (factor: {percentage})", img)

    waitKey(0)
    destroyAllWindows()
