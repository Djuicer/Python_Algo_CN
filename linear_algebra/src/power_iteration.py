import numpy as np


def power_iteration(
    input_matrix: np.ndarray,
    vector: np.ndarray,
    error_tol: float = 1e-12,
    max_iterations: int = 100,
) -> tuple[float, np.ndarray]:
    """
    幂迭代法（Power Iteration）。
    给定同一空间中的随机向量，求矩阵 input_matrix 的最大特征值及对应特征向量。
    只要 vector 含有最大特征向量方向上的分量，该方法即可工作。
    input_matrix 必须为实矩阵或厄米矩阵。

    输入
    input_matrix: 要求最大特征值的输入矩阵。
    NumPy 数组。np.shape(input_matrix) == (N,N)。
    vector: 与矩阵处于同一空间的随机初始向量。
    NumPy 数组。np.shape(vector) == (N,) 或 (N,1)。

    输出
    largest_eigenvalue: 矩阵 input_matrix 的最大特征值。
    浮点标量。
    largest_eigenvector: largest_eigenvalue 对应的特征向量。
    NumPy 数组。np.shape(largest_eigenvector) == (N,) 或 (N,1)。

    >>> import numpy as np
    >>> input_matrix = np.array([
    ... [41,  4, 20],
    ... [ 4, 26, 30],
    ... [20, 30, 50]
    ... ])
    >>> vector = np.array([41,4,20])
    >>> power_iteration(input_matrix,vector)
    (79.66086378788381, array([0.44472726, 0.46209842, 0.76725662]))
    """

    # 确保矩阵为方阵
    assert np.shape(input_matrix)[0] == np.shape(input_matrix)[1]
    # 确保维数正确
    assert np.shape(input_matrix)[0] == np.shape(vector)[0]
    # 确保两个输入同为复数类型或同为实数类型
    assert np.iscomplexobj(input_matrix) == np.iscomplexobj(vector)
    is_complex = np.iscomplexobj(input_matrix)
    if is_complex:
    # 确保复数 input_matrix 为厄米矩阵
        assert np.array_equal(input_matrix, input_matrix.conj().T)

    # 初始设置为未收敛；超过 max_iterations，或相邻两次迭代变化很小时，
    # 再确定收敛状态

    convergence = False
    lambda_previous = 0
    iterations = 0
    error = 1e12

    while not convergence:
        # 矩阵乘以向量
        w = np.dot(input_matrix, vector)
        # 对所得输出向量归一化
        vector = w / np.linalg.norm(w)
        # 计算瑞利商
        # 由于已知向量已归一化，因此比常规计算更快
        vector_h = vector.conj().T if is_complex else vector.T
        lambda_ = np.dot(vector_h, np.dot(input_matrix, vector))

        # 检查是否收敛
        error = np.abs(lambda_ - lambda_previous) / lambda_
        iterations += 1

        if error <= error_tol or iterations >= max_iterations:
            convergence = True

        lambda_previous = lambda_

    if is_complex:
        lambda_ = np.real(lambda_)

    return float(lambda_), vector


def test_power_iteration() -> None:
    """
    >>> test_power_iteration()  # self running tests
    """
    real_input_matrix = np.array([[41, 4, 20], [4, 26, 30], [20, 30, 50]])
    real_vector = np.array([41, 4, 20])
    complex_input_matrix = real_input_matrix.astype(np.complex128)
    imag_matrix = np.triu(1j * complex_input_matrix, 1)
    complex_input_matrix += imag_matrix
    complex_input_matrix += -1 * imag_matrix.T
    complex_vector = np.array([41, 4, 20]).astype(np.complex128)

    for problem_type in ["real", "complex"]:
        if problem_type == "real":
            input_matrix = real_input_matrix
            vector = real_vector
        elif problem_type == "complex":
            input_matrix = complex_input_matrix
            vector = complex_vector

    # 本实现
        eigen_value, eigen_vector = power_iteration(input_matrix, vector)

    # NumPy 实现

    # 使用 NumPy 内置的 eigh 获取特征值和特征向量
    # （eigh 用于对称矩阵或厄米矩阵）
        eigen_values, eigen_vectors = np.linalg.eigh(input_matrix)
    # 最后一个特征值为最大特征值
        eigen_value_max = eigen_values[-1]
    # 该矩阵的最后一列是最大特征值对应的特征向量
        eigen_vector_max = eigen_vectors[:, -1]

    # 检查本实现与 NumPy 是否给出相近结果
        assert np.abs(eigen_value - eigen_value_max) <= 1e-6
    # 对每个特征向量逐元素取绝对值，
    # 因为它们仅相差一个负号
        assert np.linalg.norm(np.abs(eigen_vector) - np.abs(eigen_vector_max)) <= 1e-6


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    test_power_iteration()
