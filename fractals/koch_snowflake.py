"""
说明
    科赫雪花（Koch Snowflake）是一条分形曲线，也是最早被描述的分形之一。科赫
    雪花可分阶段迭代构造。第一阶段是等边三角形，此后每一阶段都在上一阶段的
    每条边上添加向外的弯折，形成更小的等边三角形。
    对每条线段执行以下步骤即可实现：
        1. 将线段等分为三段。
        2. 以步骤 1 的中间线段为底边，向外绘制一个等边三角形。
        3. 删除步骤 2 中作为三角形底边的线段。
    （说明改编自 https://en.wikipedia.org/wiki/Koch_snowflake ）
    （更详细的说明和 Processing 语言实现参见 https://natureofcode.com/book/chapter-8-fractals/
    #84-the-koch-curve-and-the-arraylist-technique )

依赖（pip）：
    - matplotlib
    - numpy
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

# 科赫雪花的初始三角形
VECTOR_1 = np.array([0, 0])
VECTOR_2 = np.array([0.5, 0.8660254])
VECTOR_3 = np.array([1, 0])
INITIAL_VECTORS = [VECTOR_1, VECTOR_2, VECTOR_3, VECTOR_1]

# 取消注释可改为简单科赫曲线，而非科赫雪花
# INITIAL_VECTORS = [VECTOR_1, VECTOR_3]


def iterate(initial_vectors: list[np.ndarray], steps: int) -> list[np.ndarray]:
    """
    执行参数 "steps" 指定次数的迭代。较大值（5 以上）需谨慎使用，因为计算时间
    会呈指数增长。
    >>> iterate([np.array([0, 0]), np.array([1, 0])], 1)
    [array([0, 0]), array([0.33333333, 0.        ]), array([0.5       , \
0.28867513]), array([0.66666667, 0.        ]), array([1, 0])]
    """
    vectors = initial_vectors
    for _ in range(steps):
        vectors = iteration_step(vectors)
    return vectors


def iteration_step(vectors: list[np.ndarray]) -> list[np.ndarray]:
    """
    遍历每一对相邻向量。在原有两个向量之间添加 3 个向量，将相邻向量间的线段
    分成 4 段。中间向量通过旋转 60 度构造，使线段向外弯折。
    >>> iteration_step([np.array([0, 0]), np.array([1, 0])])
    [array([0, 0]), array([0.33333333, 0.        ]), array([0.5       , \
0.28867513]), array([0.66666667, 0.        ]), array([1, 0])]
    """
    new_vectors = []
    for i, start_vector in enumerate(vectors[:-1]):
        end_vector = vectors[i + 1]
        new_vectors.append(start_vector)
        difference_vector = end_vector - start_vector
        new_vectors.append(start_vector + difference_vector / 3)
        new_vectors.append(
            start_vector + difference_vector / 3 + rotate(difference_vector / 3, 60)
        )
        new_vectors.append(start_vector + difference_vector * 2 / 3)
    new_vectors.append(vectors[-1])
    return new_vectors


def rotate(vector: np.ndarray, angle_in_degrees: float) -> np.ndarray:
    """
    使用旋转矩阵对二维向量进行标准旋转
    （参见 https://en.wikipedia.org/wiki/Rotation_matrix ）
    >>> rotate(np.array([1, 0]), 60)
    array([0.5      , 0.8660254])
    >>> rotate(np.array([1, 0]), 90)
    array([6.123234e-17, 1.000000e+00])
    """
    theta = np.radians(angle_in_degrees)
    c, s = np.cos(theta), np.sin(theta)
    rotation_matrix = np.array(((c, -s), (s, c)))
    return np.dot(rotation_matrix, vector)


def plot(vectors: list[np.ndarray]) -> None:
    """
    使用 matplotlib.pyplot 绘制向量的辅助函数。
    由于此函数没有返回值，因此未实现 doctest。
    """
    # 避免图形显示被拉伸
    axes = plt.gca()
    axes.set_aspect("equal")

    # matplotlib.pyplot.plot 接受所有 x 坐标和所有 y 坐标的列表作为输入，
    # 这两个列表使用 zip() 从向量列表构造
    x_coordinates, y_coordinates = zip(*vectors)
    plt.plot(x_coordinates, y_coordinates)
    plt.show()


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    processed_vectors = iterate(INITIAL_VECTORS, 5)
    plot(processed_vectors)
