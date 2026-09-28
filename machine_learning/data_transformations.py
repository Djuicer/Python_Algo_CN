"""
归一化（Normalization）。

Wikipedia: https://en.wikipedia.org/wiki/Normalization
归一化是将数值数据转换到标准取值范围的过程，该范围通常为 [0, 1] 或
[-1, 1]。归一化公式为 x_norm = (x - x_min)/(x_max - x_min)，其中 x_norm
是归一化后的值，x 是原值，x_min 和 x_max 分别是数据列或列表中的最小值
和最大值。归一化可加快训练并使所有数据处于相近尺度，因为数据集取值范围
的差异会显著影响优化过程，尤其是梯度下降（Gradient Descent）。

Standardization Wikipedia: https://en.wikipedia.org/wiki/Standardization
标准化是将数值数据转换为均值为 0、标准差为 1 的分布，也称为 z-score
归一化。标准化公式为 x_std = (x - mu)/(sigma)，其中 mu 是数据列或列表
的均值，sigma 是其标准差。

选择归一化还是标准化往往需要通过实验判断。常见经验如下：
    1. 高斯（正态）分布通常更适合标准化
    2. 非高斯（非正态）分布通常更适合归一化
    3. 数据列或列表中存在极端值或离群值时，使用标准化
"""

from statistics import mean, stdev


def normalization(data: list, ndigits: int = 3) -> list:
    """
    返回归一化后的数值列表。

    @params：data，要归一化的数值列表
    @returns：归一化后的数值列表（四舍五入到 ndigits 位小数）
    @examples：
    >>> normalization([2, 7, 10, 20, 30, 50])
    [0.0, 0.104, 0.167, 0.375, 0.583, 1.0]
    >>> normalization([5, 10, 15, 20, 25])
    [0.0, 0.25, 0.5, 0.75, 1.0]
    """
    # 用于计算的变量
    x_min = min(data)
    x_max = max(data)
    # 归一化数据
    return [round((x - x_min) / (x_max - x_min), ndigits) for x in data]


def standardization(data: list, ndigits: int = 3) -> list:
    """
    返回标准化后的数值列表。

    @params：data，要标准化的数值列表
    @returns：标准化后的数值列表（四舍五入到 ndigits 位小数）
    @examples：
    >>> standardization([2, 7, 10, 20, 30, 50])
    [-0.999, -0.719, -0.551, 0.009, 0.57, 1.69]
    >>> standardization([5, 10, 15, 20, 25])
    [-1.265, -0.632, 0.0, 0.632, 1.265]
    """
    # 用于计算的变量
    mu = mean(data)
    sigma = stdev(data)
    # 标准化数据
    return [round((x - mu) / (sigma), ndigits) for x in data]
