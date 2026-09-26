"""多种图像缩放技术"""

import numpy as np
from cv2 import destroyAllWindows, imread, imshow, waitKey


class NearestNeighbour:
    """
    最简单、最快的图像缩放方法。
    来源：https://en.wikipedia.org/wiki/Nearest-neighbor_interpolation
    """

    def __init__(self, img, dst_width: int, dst_height: int) -> None:
        if dst_width < 0 or dst_height < 0:
            raise ValueError("Destination width/height should be > 0")

        self.img = img
        self.src_w = img.shape[1]
        self.src_h = img.shape[0]
        self.dst_w = dst_width
        self.dst_h = dst_height

        self.ratio_x = self.src_w / self.dst_w
        self.ratio_y = self.src_h / self.dst_h

        self.output = self.output_img = (
            np.ones((self.dst_h, self.dst_w, 3), np.uint8) * 255
        )

    def process(self) -> None:
        for i in range(self.dst_h):
            for j in range(self.dst_w):
                self.output[i][j] = self.img[self.get_y(i)][self.get_x(j)]

    def get_x(self, x: int) -> int:
        """
        获取目标 X 坐标对应的原图 X 坐标
        :param x: 目标 X 坐标
        :return: 根据 `x ratio` 计算的原图 X 坐标
        >>> nn = NearestNeighbour(imread("digital_image_processing/image_data/lena.jpg",
        ...                              1), 100, 100)
        >>> nn.ratio_x = 0.5
        >>> nn.get_x(4)
        2
        """
        return int(self.ratio_x * x)

    def get_y(self, y: int) -> int:
        """
        获取目标 Y 坐标对应的原图 Y 坐标
        :param y: 目标 Y 坐标
        :return: 根据 `y ratio` 计算的原图 Y 坐标
        >>> nn = NearestNeighbour(imread("digital_image_processing/image_data/lena.jpg",
        ...                              1), 100, 100)
        >>> nn.ratio_y = 0.5
        >>> nn.get_y(4)
        2
        """
        return int(self.ratio_y * y)


if __name__ == "__main__":
    dst_w, dst_h = 800, 600
    im = imread("image_data/lena.jpg", 1)
    n = NearestNeighbour(im, dst_w, dst_h)
    n.process()

    imshow(
        f"Image resized from: {im.shape[1]}x{im.shape[0]} to {dst_w}x{dst_h}", n.output
    )
    waitKey(0)
    destroyAllWindows()
