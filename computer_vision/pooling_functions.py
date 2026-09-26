# Source : https://computersciencewiki.org/index.php/Max-pooling_/_Pooling
# 导入库
import numpy as np
from PIL import Image


# 最大池化函数
def maxpooling(arr: np.ndarray, size: int, stride: int) -> np.ndarray:
    """
    本函数用于对输入的二维矩阵（图像）数组执行最大池化（Max Pooling）。
    参数：
        arr: NumPy 数组
        size: 池化矩阵大小
        stride: 在输入矩阵上移动的像素数
    返回：
        最大池化矩阵的 NumPy 数组
    输入输出示例：
    >>> maxpooling([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], 2, 2)
    array([[ 6.,  8.],
           [14., 16.]])
    >>> maxpooling([[147, 180, 122],[241, 76, 32],[126, 13, 157]], 2, 1)
    array([[241., 180.],
           [241., 157.]])
    """
    arr = np.array(arr)
    if arr.shape[0] != arr.shape[1]:
        raise ValueError("The input array is not a square matrix")
    i = 0
    j = 0
    mat_i = 0
    mat_j = 0

    # 计算输出矩阵的形状
    maxpool_shape = (arr.shape[0] - size) // stride + 1
    # 使用形状为 maxpool_shape 的零矩阵初始化输出
    updated_arr = np.zeros((maxpool_shape, maxpool_shape))

    while i < arr.shape[0]:
        if i + size > arr.shape[0]:
            # 到达矩阵末端时退出
            break
        while j < arr.shape[1]:
            # 到达矩阵末端时退出
            if j + size > arr.shape[1]:
                break
            # 计算池化矩阵的最大值
            updated_arr[mat_i][mat_j] = np.max(arr[i : i + size, j : j + size])
            # 将池化矩阵沿列方向移动 stride 个像素
            j += stride
            mat_j += 1

        # 将池化矩阵沿行方向移动 stride 个像素
        i += stride
        mat_i += 1

        # 将列索引重置为 0
        j = 0
        mat_j = 0

    return updated_arr


# 平均池化函数
def avgpooling(arr: np.ndarray, size: int, stride: int) -> np.ndarray:
    """
    本函数用于对输入的二维矩阵（图像）数组执行平均池化（Average Pooling）。
    参数：
        arr: NumPy 数组
        size: 池化矩阵大小
        stride: 在输入矩阵上移动的像素数
    返回：
        平均池化矩阵的 NumPy 数组
    输入输出示例：
    >>> avgpooling([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], 2, 2)
    array([[ 3.,  5.],
           [11., 13.]])
    >>> avgpooling([[147, 180, 122],[241, 76, 32],[126, 13, 157]], 2, 1)
    array([[161., 102.],
           [114.,  69.]])
    """
    arr = np.array(arr)
    if arr.shape[0] != arr.shape[1]:
        raise ValueError("The input array is not a square matrix")
    i = 0
    j = 0
    mat_i = 0
    mat_j = 0

    # 计算输出矩阵的形状
    avgpool_shape = (arr.shape[0] - size) // stride + 1
    # 使用形状为 avgpool_shape 的零矩阵初始化输出
    updated_arr = np.zeros((avgpool_shape, avgpool_shape))

    while i < arr.shape[0]:
        # 到达矩阵末端时退出
        if i + size > arr.shape[0]:
            break
        while j < arr.shape[1]:
            # 到达矩阵末端时退出
            if j + size > arr.shape[1]:
                break
            # 计算池化矩阵的平均值
            updated_arr[mat_i][mat_j] = int(np.average(arr[i : i + size, j : j + size]))
            # 将池化矩阵沿列方向移动 stride 个像素
            j += stride
            mat_j += 1

        # 将池化矩阵沿行方向移动 stride 个像素
        i += stride
        mat_i += 1
        # 将列索引重置为 0
        j = 0
        mat_j = 0

    return updated_arr


# 主函数
if __name__ == "__main__":
    from doctest import testmod

    testmod(name="avgpooling", verbose=True)

    # 加载图像
    image = Image.open("path_to_image")

    # 将图像转换为 NumPy 数组并执行最大池化，然后显示结果
    # 确保图像为方阵

    Image.fromarray(maxpooling(np.array(image), size=3, stride=2)).show()

    # 将图像转换为 NumPy 数组并执行平均池化，然后显示结果
    # 确保图像为方阵

    Image.fromarray(avgpooling(np.array(image), size=3, stride=2)).show()
