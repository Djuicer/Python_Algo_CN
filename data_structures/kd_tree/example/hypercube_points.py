#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11532
#  https://github.com/TheAlgorithms/Python/pull/11532
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

import numpy as np


def hypercube_points(
    num_points: int, hypercube_size: float, num_dimensions: int
) -> np.ndarray:
    """
    Generates 随机 点 uniformly distributed 之内 n-dimensional hypercube。

    参数：
        num_points: 数 的 点 到 生成。
        hypercube_size: 大小 的 hypercube。
        num_dimensions: 数 的 dimensions 的 hypercube。

    返回值：
        一个数组 的 shape (num_points，num_dimensions)
                    带有 generated 点。
    """
    rng = np.random.default_rng()
    shape = (num_points, num_dimensions)
    return hypercube_size * rng.random(shape)
