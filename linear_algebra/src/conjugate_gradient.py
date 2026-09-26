"""
参考资料：
- https://en.wikipedia.org/wiki/Conjugate_gradient_method
- https://en.wikipedia.org/wiki/Definite_symmetric_matrix
"""

from typing import Any

import numpy as np


def _is_matrix_spd(matrix: np.ndarray) -> bool:
    """
    若输入矩阵为对称正定矩阵，则返回 True；否则返回 False。

    对称正定（SPD）矩阵的所有特征值都必须为正。

    >>> import numpy as np
    >>> matrix = np.array([
    ... [4.12401784, -5.01453636, -0.63865857],
    ... [-5.01453636, 12.33347422, -3.40493586],
    ... [-0.63865857, -3.40493586,  5.78591885]])
    >>> _is_matrix_spd(matrix)
    True
    >>> matrix = np.array([
    ... [0.34634879,  1.96165514,  2.18277744],
    ... [0.74074469, -1.19648894, -1.34223498],
    ... [-0.7687067 ,  0.06018373, -1.16315631]])
    >>> _is_matrix_spd(matrix)
    False
    """
    # 确保矩阵为方阵
    assert np.shape(matrix)[0] == np.shape(matrix)[1]

    # 若矩阵不对称，则立即退出
    if np.allclose(matrix, matrix.T) is False:
        return False

    # 获取对称矩阵的特征值和特征向量
    eigen_values, _ = np.linalg.eigh(matrix)

    # 检查所有特征值的符号
    # np.all 返回 np.bool_ 类型的值
    return bool(np.all(eigen_values > 0))


def _create_spd_matrix(dimension: int) -> Any:
    """
    根据给定维数返回一个对称正定矩阵。

    输入：
    dimension 指定方阵的维数。

    输出：
    spd_matrix 是 dimension x dimension 的对称正定（SPD）矩阵。

    >>> import numpy as np
    >>> dimension = 3
    >>> spd_matrix = _create_spd_matrix(dimension)
    >>> _is_matrix_spd(spd_matrix)
    True
    """
    rng = np.random.default_rng()
    random_matrix = rng.normal(size=(dimension, dimension))
    spd_matrix = np.dot(random_matrix, random_matrix.T)
    assert _is_matrix_spd(spd_matrix)
    return spd_matrix


def conjugate_gradient(
    spd_matrix: np.ndarray,
    load_vector: np.ndarray,
    max_iterations: int = 1000,
    tol: float = 1e-8,
) -> Any:
    """
    返回线性方程组 np.dot(spd_matrix, x) = b 的解。

    输入：
    spd_matrix 是 NxN 对称正定（SPD）矩阵。
    load_vector 是 Nx1 向量。

    输出：
    x 是作为解向量的 Nx1 向量。

    >>> import numpy as np
    >>> spd_matrix = np.array([
    ... [8.73256573, -5.02034289, -2.68709226],
    ... [-5.02034289,  3.78188322,  0.91980451],
    ... [-2.68709226,  0.91980451,  1.94746467]])
    >>> b = np.array([
    ... [-5.80872761],
    ... [ 3.23807431],
    ... [ 1.95381422]])
    >>> conjugate_gradient(spd_matrix, b)
    array([[-0.63114139],
           [-0.01561498],
           [ 0.13979294]])
    """
    # 确保维数正确
    assert np.shape(spd_matrix)[0] == np.shape(spd_matrix)[1]
    assert np.shape(load_vector)[0] == np.shape(spd_matrix)[0]
    assert _is_matrix_spd(spd_matrix)

    # 初始化解的估计值、残差和搜索方向
    x0 = np.zeros((np.shape(load_vector)[0], 1))
    r0 = np.copy(load_vector)
    p0 = np.copy(r0)

    # 设置解估计值和残差的初始误差
    error_residual = 1e9
    error_x_solution = 1e9
    error = 1e9

    # 将迭代计数器设为阈值迭代次数
    iterations = 0

    while error > tol:
    # 保存该值，以便矩阵与向量的乘积只计算一次
        w = np.dot(spd_matrix, p0)

    # 主算法

        # 更新搜索方向的幅度
        alpha = np.dot(r0.T, r0) / np.dot(p0.T, w)
        # 更新解的估计值
        x = x0 + alpha * p0
        # 计算新残差
        r = r0 - alpha * w
        # 计算新的 Krylov 子空间缩放系数
        beta = np.dot(r.T, r) / np.dot(r0.T, r0)
        # 计算新的 A 共轭搜索方向
        p = r + beta * p0

        # 计算误差
        error_residual = np.linalg.norm(r - r0)
        error_x_solution = np.linalg.norm(x - x0)
        error = np.maximum(error_residual, error_x_solution)

        # 更新变量
        x0 = np.copy(x)
        r0 = np.copy(r)
        p0 = np.copy(p)

        # 更新迭代次数
        iterations += 1
        if iterations > max_iterations:
            break

    return x


def test_conjugate_gradient() -> None:
    """
    >>> test_conjugate_gradient()  # self running tests
    """
    # 使用 SPD 矩阵和已知解 x_true 构造线性方程组
    dimension = 3
    spd_matrix = _create_spd_matrix(dimension)
    rng = np.random.default_rng()
    x_true = rng.normal(size=(dimension, 1))
    b = np.dot(spd_matrix, x_true)

    # NumPy 的解
    x_numpy = np.linalg.solve(spd_matrix, b)

    # 本实现的解
    x_conjugate_gradient = conjugate_gradient(spd_matrix, b)

    # 确保两个解都接近 x_true（因而彼此也接近）
    assert np.linalg.norm(x_numpy - x_true) <= 1e-6
    assert np.linalg.norm(x_conjugate_gradient - x_true) <= 1e-6


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    test_conjugate_gradient()
