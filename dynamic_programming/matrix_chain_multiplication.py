"""
| 求矩阵链相乘所需的最少乘法次数。
| Reference: https://www.geeksforgeeks.org/matrix-chain-multiplication-dp-8/

该算法有许多有趣的实际应用。

示例：
  1. 计算机图形学中的图像变换，因为图像由矩阵构成。
  2. 以最少的处理能力求解代数领域的复杂多项式方程。
  3. 计算宏观经济决策的整体影响，因为经济方程涉及多个变量。
  4. 矩阵乘法可以在短时间内准确确定障碍物的位置和方向，从而提高自动驾驶汽车导航的准确性。

可使用以下命令运行 Python doctest：

  python -m doctest -v matrix_chain_multiply.py

给定表示 2D 矩阵链的序列 ``arr[]``，其中第 ``i`` 个矩阵的维度为
``arr[i-1]*arr[i]``。例如，``arr = [40, 20, 30, 10, 30]`` 表示有 ``4`` 个矩阵，
其维度分别为 ``40*20``、``20*30``、``30*10`` 和 ``10*30``。

``matrix_chain_multiply()`` 返回一个整数，表示矩阵链相乘所需的最少乘法次数。

这里不需要执行实际的乘法，只需决定执行乘法的顺序。

提示：
  1. 将 ``2`` 个大小分别为 ``m*p`` 和 ``p*n`` 的矩阵相乘，乘法次数（即代价）为 ``m*p*n``。
  2. 矩阵乘法的代价不满足结合律，即 ``(M1*M2)*M3 != M1*(M2*M3)``。
  3. 矩阵乘法不满足交换律，因此 ``M1*M2`` 并不意味着可以执行 ``M2*M1``。
  4. 为确定所需顺序，可以尝试不同的组合。

因此，此问题具有重叠子问题，可以使用递归求解。
我们使用动态规划（Dynamic Programming）来获得最优时间复杂度。

示例输入：
    ``arr = [40, 20, 30, 10, 30]``
输出：
    ``26000``
"""

from collections.abc import Iterator
from contextlib import contextmanager
from functools import cache
from sys import maxsize


def matrix_chain_multiply(arr: list[int]) -> int:
    """
    求矩阵链相乘所需的最少乘法次数。

    参数：
        `arr`: 输入整数数组。

    返回：
        矩阵链相乘所需的最少乘法次数。

    示例：

    >>> matrix_chain_multiply([1, 2, 3, 4, 3])
    30
    >>> matrix_chain_multiply([10])
    0
    >>> matrix_chain_multiply([10, 20])
    0
    >>> matrix_chain_multiply([19, 2, 19])
    722
    >>> matrix_chain_multiply(list(range(1, 100)))
    323398
    >>> # matrix_chain_multiply(list(range(1, 251)))
    # 2626798
    """
    if len(arr) < 2:
        return 0
    # 初始化 2D dp 矩阵
    n = len(arr)
    dp = [[maxsize for j in range(n)] for i in range(n)]
    # 求维度为 (i*k) 和 (k*j) 的矩阵相乘的最小代价
    # 该代价为 arr[i-1]*arr[k]*arr[j]
    for i in range(n - 1, 0, -1):
        for j in range(i, n):
            if i == j:
                dp[i][j] = 0
                continue
            for k in range(i, j):
                dp[i][j] = min(
                    dp[i][j], dp[i][k] + dp[k + 1][j] + arr[i - 1] * arr[k] * arr[j]
                )

    return dp[1][n - 1]


def matrix_chain_order(dims: list[int]) -> int:
    """
    来源：https://en.wikipedia.org/wiki/Matrix_chain_multiplication

    动态规划解法比带缓存的递归解法更快，并且可以处理更大的输入。

    >>> matrix_chain_order([1, 2, 3, 4, 3])
    30
    >>> matrix_chain_order([10])
    0
    >>> matrix_chain_order([10, 20])
    0
    >>> matrix_chain_order([19, 2, 19])
    722
    >>> matrix_chain_order(list(range(1, 100)))
    323398
    >>> # matrix_chain_order(list(range(1, 251)))  # Max before RecursionError is raised
    # 2626798
    """

    @cache
    def a(i: int, j: int) -> int:
        return min(
            (a(i, k) + dims[i] * dims[k] * dims[j] + a(k, j) for k in range(i + 1, j)),
            default=0,
        )

    return a(0, len(dims) - 1)


@contextmanager
def elapsed_time(msg: str) -> Iterator:
    # print(f"Starting: {msg}")
    from time import perf_counter_ns

    start = perf_counter_ns()
    yield
    print(f"Finished: {msg} in {(perf_counter_ns() - start) / 10**9} seconds.")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    with elapsed_time("matrix_chain_order"):
        print(f"{matrix_chain_order(list(range(1, 251))) = }")
    with elapsed_time("matrix_chain_multiply"):
        print(f"{matrix_chain_multiply(list(range(1, 251))) = }")
    with elapsed_time("matrix_chain_order"):
        print(f"{matrix_chain_order(list(range(1, 251))) = }")
    with elapsed_time("matrix_chain_multiply"):
        print(f"{matrix_chain_multiply(list(range(1, 251))) = }")
