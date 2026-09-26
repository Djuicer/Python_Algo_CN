import cv2
import numpy as np

from digital_image_processing.filters.convolve import img_convolve
from digital_image_processing.filters.sobel_filter import sobel_filter

PI = 180


def gen_gaussian_kernel(k_size, sigma):
    center = k_size // 2
    x, y = np.mgrid[0 - center : k_size - center, 0 - center : k_size - center]
    g = (
        1
        / (2 * np.pi * sigma)
        * np.exp(-(np.square(x) + np.square(y)) / (2 * np.square(sigma)))
    )
    return g


def suppress_non_maximum(image_shape, gradient_direction, sobel_grad):
    """
    非极大值抑制：若当前像素的边缘强度在掩码内同方向像素中最大，
    则保留该值；否则抑制该值。
    """
    destination = np.zeros(image_shape)

    for row in range(1, image_shape[0] - 1):
        for col in range(1, image_shape[1] - 1):
            direction = gradient_direction[row, col]

            if (
                0 <= direction < PI / 8
                or 15 * PI / 8 <= direction <= 2 * PI
                or 7 * PI / 8 <= direction <= 9 * PI / 8
            ):
                w = sobel_grad[row, col - 1]
                e = sobel_grad[row, col + 1]
                if sobel_grad[row, col] >= w and sobel_grad[row, col] >= e:
                    destination[row, col] = sobel_grad[row, col]

            elif (
                PI / 8 <= direction < 3 * PI / 8
                or 9 * PI / 8 <= direction < 11 * PI / 8
            ):
                sw = sobel_grad[row + 1, col - 1]
                ne = sobel_grad[row - 1, col + 1]
                if sobel_grad[row, col] >= sw and sobel_grad[row, col] >= ne:
                    destination[row, col] = sobel_grad[row, col]

            elif (
                3 * PI / 8 <= direction < 5 * PI / 8
                or 11 * PI / 8 <= direction < 13 * PI / 8
            ):
                n = sobel_grad[row - 1, col]
                s = sobel_grad[row + 1, col]
                if sobel_grad[row, col] >= n and sobel_grad[row, col] >= s:
                    destination[row, col] = sobel_grad[row, col]

            elif (
                5 * PI / 8 <= direction < 7 * PI / 8
                or 13 * PI / 8 <= direction < 15 * PI / 8
            ):
                nw = sobel_grad[row - 1, col - 1]
                se = sobel_grad[row + 1, col + 1]
                if sobel_grad[row, col] >= nw and sobel_grad[row, col] >= se:
                    destination[row, col] = sobel_grad[row, col]

    return destination


def detect_high_low_threshold(
    image_shape, destination, threshold_low, threshold_high, weak, strong
) -> None:
    """
    高低阈值检测：若边缘像素的梯度值高于高阈值，则标记为强边缘像素；
    若低于高阈值且高于低阈值，则标记为弱边缘像素；
    若低于低阈值，则抑制该像素。
    """
    for row in range(1, image_shape[0] - 1):
        for col in range(1, image_shape[1] - 1):
            if destination[row, col] >= threshold_high:
                destination[row, col] = strong
            elif destination[row, col] <= threshold_low:
                destination[row, col] = 0
            else:
                destination[row, col] = weak


def track_edge(image_shape, destination, weak, strong) -> None:
    """
    边缘跟踪：真实边缘产生的弱边缘像素通常与强边缘像素相连，而噪声响应
    通常不相连。只要弱边缘像素的八连通邻域中存在强边缘像素，就应保留该点。
    """
    for row in range(1, image_shape[0]):
        for col in range(1, image_shape[1]):
            if destination[row, col] == weak:
                if 255 in (
                    destination[row, col + 1],
                    destination[row, col - 1],
                    destination[row - 1, col],
                    destination[row + 1, col],
                    destination[row - 1, col - 1],
                    destination[row + 1, col - 1],
                    destination[row - 1, col + 1],
                    destination[row + 1, col + 1],
                ):
                    destination[row, col] = strong
                else:
                    destination[row, col] = 0


def canny(image, threshold_low=15, threshold_high=30, weak=128, strong=255):
    # gaussian_filter
    gaussian_out = img_convolve(image, gen_gaussian_kernel(9, sigma=1.4))
    # 使用 sobel_filter 获取梯度和角度
    sobel_grad, sobel_theta = sobel_filter(gaussian_out)
    gradient_direction = PI + np.rad2deg(sobel_theta)

    destination = suppress_non_maximum(image.shape, gradient_direction, sobel_grad)

    detect_high_low_threshold(
        image.shape, destination, threshold_low, threshold_high, weak, strong
    )

    track_edge(image.shape, destination, weak, strong)

    return destination


if __name__ == "__main__":
    # 以灰度模式读取原始图像
    lena = cv2.imread(r"../image_data/lena.jpg", 0)
    # Canny 边缘检测
    canny_destination = canny(lena)
    cv2.imshow("canny", canny_destination)
    cv2.waitKey(0)
