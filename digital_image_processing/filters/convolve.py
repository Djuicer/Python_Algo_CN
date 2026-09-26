# @Author  : lightXu
# @File    : convolve.py
# @Time    : 2019/7/8 0008 下午 16:13
from cv2 import COLOR_BGR2GRAY, cvtColor, imread, imshow, waitKey
from numpy import array, dot, pad, ravel, uint8, zeros


def im2col(image, block_size):
    rows, cols = image.shape
    dst_height = cols - block_size[1] + 1
    dst_width = rows - block_size[0] + 1
    image_array = zeros((dst_height * dst_width, block_size[1] * block_size[0]))
    row = 0
    for i in range(dst_height):
        for j in range(dst_width):
            window = ravel(image[i : i + block_size[0], j : j + block_size[1]])
            image_array[row, :] = window
            row += 1

    return image_array


def img_convolve(image, filter_kernel):
    height, width = image.shape[0], image.shape[1]
    k_size = filter_kernel.shape[0]
    pad_size = k_size // 2
    # 使用数组边缘值填充图像
    image_tmp = pad(image, pad_size, mode="edge")

    # im2col：将 k_size*k_size 个像素转为一行，再用 np.vstack 堆叠所有行
    image_array = im2col(image_tmp, (k_size, k_size))

    # 将卷积核转换为形状 (k*k, 1)
    kernel_array = ravel(filter_kernel)
    # 重塑并得到目标图像
    dst = dot(image_array, kernel_array).reshape(height, width)
    return dst


if __name__ == "__main__":
    # 读取原始图像
    img = imread(r"../image_data/lena.jpg")
    # 将图像转换为灰度值
    gray = cvtColor(img, COLOR_BGR2GRAY)
    # Laplace 算子
    Laplace_kernel = array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    out = img_convolve(gray, Laplace_kernel).astype(uint8)
    imshow("Laplacian", out)
    waitKey(0)
