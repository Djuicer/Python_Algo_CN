"""
Burkes 抖动算法的实现。
"""

import numpy as np
from cv2 import destroyAllWindows, imread, imshow, waitKey


class Burkes:
    """
    Burkes 算法用于将灰度图像转换为黑白图像。
    来源：https://en.wikipedia.org/wiki/Dither

    注意：
        * threshold= ~1/2 * 最大灰度值时效果最佳。
        * 本实现接收 RGB 图像，并在运行时将其转换为灰度图。
    """

    def __init__(self, input_img, threshold: int) -> None:
        self.min_threshold = 0
        # #FFFFFF 对应的最大灰度值
        self.max_threshold = int(self.get_greyscale(255, 255, 255))

        if not self.min_threshold < threshold < self.max_threshold:
            msg = f"Factor value should be from 0 to {self.max_threshold}"
            raise ValueError(msg)

        self.input_img = input_img
        self.threshold = threshold
        self.width, self.height = self.input_img.shape[1], self.input_img.shape[0]

        # 误差表比输入图像多 4 列和 1 行，从而无需使用条件语句
        self.error_table = [
            [0 for _ in range(self.height + 4)] for __ in range(self.width + 1)
        ]
        self.output_img = np.ones((self.width, self.height, 3), np.uint8) * 255

    @classmethod
    def get_greyscale(cls, blue: int, green: int, red: int) -> float:
        """
        >>> Burkes.get_greyscale(3, 4, 5)
        4.185
        >>> Burkes.get_greyscale(0, 0, 0)
        0.0
        >>> Burkes.get_greyscale(255, 255, 255)
        255.0
        """
        """
        公式来源：https://en.wikipedia.org/wiki/HSL_and_HSV
        参见 Lightness 一节和图 13c。此处采用四种可选公式中的第一种。
        """
        return 0.114 * blue + 0.587 * green + 0.299 * red

    def process(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                greyscale = int(self.get_greyscale(*self.input_img[y][x]))
                if self.threshold > greyscale + self.error_table[y][x]:
                    self.output_img[y][x] = (0, 0, 0)
                    current_error = greyscale + self.error_table[y][x]
                else:
                    self.output_img[y][x] = (255, 255, 255)
                    current_error = greyscale + self.error_table[y][x] - 255
                """
                Burkes 误差传播（`*` 表示当前像素）：

                                 *          8/32        4/32
                2/32    4/32    8/32    4/32    2/32
                """
                self.error_table[y][x + 1] += int(8 / 32 * current_error)
                self.error_table[y][x + 2] += int(4 / 32 * current_error)
                self.error_table[y + 1][x] += int(8 / 32 * current_error)
                self.error_table[y + 1][x + 1] += int(4 / 32 * current_error)
                self.error_table[y + 1][x + 2] += int(2 / 32 * current_error)
                self.error_table[y + 1][x - 1] += int(4 / 32 * current_error)
                self.error_table[y + 1][x - 2] += int(2 / 32 * current_error)


if __name__ == "__main__":
    # 使用原始图像的灰度版本创建 Burkes 实例
    burkes_instances = [
        Burkes(imread("image_data/lena.jpg", 1), threshold)
        for threshold in (1, 126, 130, 140)
    ]

    for burkes in burkes_instances:
        burkes.process()

    for burkes in burkes_instances:
        imshow(
            f"Original image with dithering threshold: {burkes.threshold}",
            burkes.output_img,
        )

    waitKey(0)
    destroyAllWindows()
