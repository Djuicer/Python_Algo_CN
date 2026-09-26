"""
https://en.wikipedia.org/wiki/Image_texture
https://en.wikipedia.org/wiki/Co-occurrence_matrix#Application_to_image_analysis
"""

import imageio.v2 as imageio
import numpy as np
import numpy.typing as npt


def root_mean_square_error(original: np.ndarray, reference: np.ndarray) -> float:
    """计算两个 N 维 NumPy 数组均方根误差的简单实现。

    示例：
        >>> root_mean_square_error(np.array([1, 2, 3]), np.array([1, 2, 3]))
        0.0
        >>> root_mean_square_error(np.array([1, 2, 3]), np.array([2, 2, 2]))
        0.816496580927726
        >>> root_mean_square_error(np.array([1, 2, 3]), np.array([6, 4, 2]))
        3.1622776601683795
    """
    return float(np.sqrt(((original - reference) ** 2).mean()))


def normalize_image(
    image: np.ndarray, cap: float = 255.0, data_type: npt.DTypeLike = np.uint8
) -> np.ndarray:
    """
    将 NumPy 二维数组格式的图像归一化到 0-cap 范围，以适配 uint8 类型。

    参数：
        image: 以矩阵表示图像的二维 NumPy 数组，值可处于任意范围
        cap: 归一化的最大上限
        data_type: 输出变量使用的 NumPy 数据类型
    返回：
        返回 uint8 类型的二维 NumPy 数组，对应范围受限的矩阵

    示例：
        >>> normalize_image(np.array([[1, 2, 3], [4, 5, 10]]),
        ...                 cap=1.0, data_type=np.float64)
        array([[0.        , 0.11111111, 0.22222222],
               [0.33333333, 0.44444444, 1.        ]])
        >>> normalize_image(np.array([[4, 4, 3], [1, 7, 2]]))
        array([[127, 127,  85],
               [  0, 255,  42]], dtype=uint8)
    """
    normalized = (image - np.min(image)) / (np.max(image) - np.min(image)) * cap
    return normalized.astype(data_type)


def normalize_array(array: np.ndarray, cap: float = 1) -> np.ndarray:
    """将一维数组归一化到 0-cap 范围。

    参数：
        array: 包含待归一化到上限范围内数值的列表。
        cap: 归一化的最大上限。
    返回：
        返回一维 NumPy 数组，对应范围受限的数组

    示例：
        >>> normalize_array(np.array([2, 3, 5, 7]))
        array([0. , 0.2, 0.6, 1. ])
        >>> normalize_array(np.array([[5], [7], [11], [13]]))
        array([[0.  ],
               [0.25],
               [0.75],
               [1.  ]])
    """
    diff = np.max(array) - np.min(array)
    return (array - np.min(array)) / (1 if diff == 0 else diff) * cap


def grayscale(image: np.ndarray) -> np.ndarray:
    """
    通过计算通道与亮度权重的点积，将 RGB 通道转换为灰度图。

    示例：
        >>> grayscale(np.array([[[108, 201, 72], [255, 11,  127]],
        ...                     [[56,  56,  56], [128, 255, 107]]]))
        array([[158,  97],
               [ 56, 200]], dtype=uint8)
    """
    return np.dot(image[:, :, 0:3], [0.299, 0.587, 0.114]).astype(np.uint8)


def binarize(image: np.ndarray, threshold: float = 127.0) -> np.ndarray:
    """
    根据给定阈值对灰度图像进行二值化，将数值相应设为 1 或 0。

    示例：
        >>> binarize(np.array([[128, 255], [101, 156]]))
        array([[1, 1],
               [0, 1]])
        >>> binarize(np.array([[0.07, 1], [0.51, 0.3]]), threshold=0.5)
        array([[0, 1],
               [1, 0]])
    """
    return np.where(image > threshold, 1, 0)


def transform(
    image: np.ndarray, kind: str, kernel: np.ndarray | None = None
) -> np.ndarray:
    """
    使用腐蚀（Erosion）或膨胀（Dilation）两种滤波函数之一进行简单图像变换。

    参数：
        image: 要应用变换的二值化输入图像
        kind: 可以是 'erosion'，此时调用 :func:np.max；也可以是
              'dilation'，此时改用 :func:np.min。
        kernel: 形状小于 :attr:image.shape 的 n x n 卷积核，
              用于对原始图像应用卷积

    返回：
        返回与输入图像形状相同的 NumPy 数组，对应所应用的二值变换。

    示例：
        >>> img = np.array([[1, 0.5], [0.2, 0.7]])
        >>> img = binarize(img, threshold=0.5)
        >>> transform(img, 'erosion')
        array([[1, 1],
               [1, 1]], dtype=uint8)
        >>> transform(img, 'dilation')
        array([[0, 0],
               [0, 0]], dtype=uint8)
    """
    if kernel is None:
        kernel = np.ones((3, 3))

    if kind == "erosion":
        constant = 1
        apply = np.max
    else:
        constant = 0
        apply = np.min

    center_x, center_y = (x // 2 for x in kernel.shape)

    # 应用卷积时使用填充图像，避免越过原图边界
    transformed = np.zeros(image.shape, dtype=np.uint8)
    padded = np.pad(image, 1, "constant", constant_values=constant)

    for x in range(center_x, padded.shape[0] - center_x):
        for y in range(center_y, padded.shape[1] - center_y):
            center = padded[
                x - center_x : x + center_x + 1, y - center_y : y + center_y + 1
            ]
            # 对图像的中心区域应用变换方法
            transformed[x - center_x, y - center_y] = apply(center[kernel == 1])

    return transformed


def opening_filter(image: np.ndarray, kernel: np.ndarray | None = None) -> np.ndarray:
    """
    开运算滤波器：依次对同一图像执行腐蚀和膨胀滤波。

    示例：
        >>> img = np.array([[1, 0.5], [0.2, 0.7]])
        >>> img = binarize(img, threshold=0.5)
        >>> opening_filter(img)
        array([[1, 1],
               [1, 1]], dtype=uint8)
    """
    if kernel is None:
        np.ones((3, 3))

    return transform(transform(image, "dilation", kernel), "erosion", kernel)


def closing_filter(image: np.ndarray, kernel: np.ndarray | None = None) -> np.ndarray:
    """
    闭运算滤波器：依次对同一图像执行膨胀和腐蚀滤波。

    示例：
        >>> img = np.array([[1, 0.5], [0.2, 0.7]])
        >>> img = binarize(img, threshold=0.5)
        >>> closing_filter(img)
        array([[0, 0],
               [0, 0]], dtype=uint8)
    """
    if kernel is None:
        kernel = np.ones((3, 3))
    return transform(transform(image, "erosion", kernel), "dilation", kernel)


def binary_mask(
    image_gray: np.ndarray, image_map: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    应用二值掩码，或根据位掩码值执行阈值处理（映射掩码为二值）。

    返回映射后的真值掩码及其互补的假值掩码。

    示例：
        >>> img = np.array([[[108, 201, 72], [255, 11,  127]],
        ...                 [[56,  56,  56], [128, 255, 107]]])
        >>> gray = grayscale(img)
        >>> binary = binarize(gray)
        >>> morphological = opening_filter(binary)
        >>> binary_mask(gray, morphological)
        (array([[1, 1],
               [1, 1]], dtype=uint8), array([[158,  97],
               [ 56, 200]], dtype=uint8))
    """
    true_mask, false_mask = image_gray.copy(), image_gray.copy()
    true_mask[image_map == 1] = 1
    false_mask[image_map == 0] = 0

    return true_mask, false_mask


def matrix_concurrency(image: np.ndarray, coordinate: tuple[int, int]) -> np.ndarray:
    """
    根据输入图像及图像上选定的坐标计算样本共生矩阵。

    由于要执行的函数（np.max）是非线性的，无法在频域调用，
    因此本实现使用基本迭代。

    示例：
        >>> img = np.array([[[108, 201, 72], [255, 11,  127]],
        ...                 [[56,  56,  56], [128, 255, 107]]])
        >>> gray = grayscale(img)
        >>> binary = binarize(gray)
        >>> morphological = opening_filter(binary)
        >>> mask_1 = binary_mask(gray, morphological)[0]
        >>> matrix_concurrency(mask_1, (0, 1))
        array([[0., 0.],
               [0., 0.]])
    """
    matrix = np.zeros([np.max(image) + 1, np.max(image) + 1])

    offset_x, offset_y = coordinate

    for x in range(1, image.shape[0] - 1):
        for y in range(1, image.shape[1] - 1):
            base_pixel = image[x, y]
            offset_pixel = image[x + offset_x, y + offset_y]

            matrix[base_pixel, offset_pixel] += 1
    matrix_sum = np.sum(matrix)
    return matrix / (1 if matrix_sum == 0 else matrix_sum)


def haralick_descriptors(matrix: np.ndarray) -> list[float]:
    """根据输入的共生矩阵计算全部 8 个 Haralick 描述子：
    最大概率、逆差、同质性、熵、能量、非相似性、对比度和相关性。

    参数：
        matrix: 用作描述子计算基础的共生矩阵。

    返回：
        逆序排列的描述子结果列表

    示例：
        >>> img = np.array([[[108, 201, 72], [255, 11,  127]],
        ...                 [[56,  56,  56], [128, 255, 107]]])
        >>> gray = grayscale(img)
        >>> binary = binarize(gray)
        >>> morphological = opening_filter(binary)
        >>> mask_1 = binary_mask(gray, morphological)[0]
        >>> concurrency = matrix_concurrency(mask_1, (0, 1))
        >>> [float(f) for f in haralick_descriptors(concurrency)]
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    """
    # 对于更大的输入类型可以使用 np.indices，但 np.ogrid 已足够
    i, j = np.ogrid[0 : matrix.shape[0], 0 : matrix.shape[1]]  # np.indices()

    # 预先计算频繁使用的乘法和减法
    prod = np.multiply(i, j)
    sub = np.subtract(i, j)

    # 计算最大概率的数值
    maximum_prob = np.max(matrix)
    # 根据每个描述子的定义分别计算其矩阵
    correlation = prod * matrix
    energy = np.power(matrix, 2)
    contrast = matrix * np.power(sub, 2)

    dissimilarity = matrix * np.abs(sub)
    inverse_difference = matrix / (1 + np.abs(sub))
    homogeneity = matrix / (1 + np.power(sub, 2))
    entropy = -(matrix[matrix > 0] * np.log(matrix[matrix > 0]))

    # 对从第一个到最后一个描述子的值求和，因为此时各项仍是各自的原始矩阵，
    # 尚未得到最终数值
    return [
        maximum_prob,
        correlation.sum(),
        energy.sum(),
        contrast.sum(),
        dissimilarity.sum(),
        inverse_difference.sum(),
        homogeneity.sum(),
        entropy.sum(),
    ]


def get_descriptors(
    masks: tuple[np.ndarray, np.ndarray], coordinate: tuple[int, int]
) -> np.ndarray:
    """
    根据输入掩码和坐标，计算一系列不同共生矩阵的全部 Haralick 描述子。

    示例：
        >>> img = np.array([[[108, 201, 72], [255, 11,  127]],
        ...                 [[56,  56,  56], [128, 255, 107]]])
        >>> gray = grayscale(img)
        >>> binary = binarize(gray)
        >>> morphological = opening_filter(binary)
        >>> get_descriptors(binary_mask(gray, morphological), (0, 1))
        array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
    """
    descriptors = np.array(
        [haralick_descriptors(matrix_concurrency(mask, coordinate)) for mask in masks]
    )

    # 将各个描述子连接成一个包含描述子序列的列表
    return np.concatenate(descriptors, axis=None)


def euclidean(point_1: np.ndarray, point_2: np.ndarray) -> float:
    """
    计算两个 np.ndarray 类型点之间欧氏距离的简单方法。

    示例：
        >>> a = np.array([1, 0, -2])
        >>> b = np.array([2, -1, 1])
        >>> euclidean(a, b)
        3.3166247903554
    """
    return float(np.sqrt(np.sum(np.square(point_1 - point_2))))


def get_distances(descriptors: np.ndarray, base: int) -> list[tuple[int, float]]:
    """
    计算选定基准描述子与其他所有 Haralick 描述子之间的欧氏距离。
    比较结果按降序返回，以显示哪个描述子与选定基准最相似。

    参数：
        descriptors: 要与基准索引比较的 Haralick 描述子
        base: 计算与其他描述子欧氏距离时用作基准的 Haralick 描述子索引。

    返回：
        描述子之间排好序的距离

    示例：
        >>> index = 1
        >>> img = np.array([[[108, 201, 72], [255, 11,  127]],
        ...                 [[56,  56,  56], [128, 255, 107]]])
        >>> gray = grayscale(img)
        >>> binary = binarize(gray)
        >>> morphological = opening_filter(binary)
        >>> get_distances(get_descriptors(
        ...                 binary_mask(gray, morphological), (0, 1)),
        ...               index)
        [(0, 0.0), (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), \
(6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 0.0), \
(13, 0.0), (14, 0.0), (15, 0.0)]
    """
    distances = np.array(
        [euclidean(descriptor, descriptors[base]) for descriptor in descriptors]
    )
    # 将距离归一化到 [0, 1] 范围
    normalized_distances: list[float] = normalize_array(distances, 1).tolist()
    enum_distances = list(enumerate(normalized_distances))
    enum_distances.sort(key=lambda tup: tup[1], reverse=True)
    return enum_distances


if __name__ == "__main__":
    # 用于比较 Haralick 描述子的索引
    index = int(input())
    q_value_list = [int(value) for value in input().split()]
    q_value = (q_value_list[0], q_value_list[1])

    # 格式表示要应用的相应滤波器：1 表示开运算滤波器，其他值表示闭运算
    parameters = {"format": int(input()), "threshold": int(input())}

    # 要执行这些方法的图像数量
    b_number = int(input())

    files, descriptors = [], []

    for _ in range(b_number):
        file = input().rstrip()
        files.append(file)

        # 打开给定图像，计算形态学滤波、相应掩码和对应的 Haralick 描述子
        image = imageio.imread(file).astype(np.float32)
        gray = grayscale(image)
        threshold = binarize(gray, parameters["threshold"])

        morphological = (
            opening_filter(threshold)
            if parameters["format"] == 1
            else closing_filter(threshold)
        )
        masks = binary_mask(gray, morphological)
        descriptors.append(get_descriptors(masks, q_value))

    # 将排好序的距离数组转换为与原文件位置对应的索引序列
    distances = get_distances(np.array(descriptors), index)
    indexed_distances = np.array(distances).astype(np.uint8)[:, 0]

    # 最后，使用所选形态学方法，输出基准文件的 Haralick 描述子与其他所有
    # 图像之间的距离
    print(f"Query: {files[index]}")
    print("Ranking:")
    for idx, file_idx in enumerate(indexed_distances):
        print(f"({idx}) {files[file_idx]}", end="\n")
