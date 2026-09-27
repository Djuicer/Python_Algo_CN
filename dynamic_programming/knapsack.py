"""
给定 n 个物品的重量和价值，将这些物品放入容量为 W 的背包，
使背包中物品的总价值最大。

请注意，只有整数重量的 0-1 背包问题可以使用动态规划求解。
"""


def mf_knapsack(i, wt, val, j):
    """
    此代码使用记忆函数的概念。与下面的示例不同，这里只求解需要的子问题。
    F 是一个 2D 数组，以 ``-1`` 填充。
    """
    global f  # 背包问题的全局 dp 表
    if f[i][j] < 0:
        if j < wt[i - 1]:
            val = mf_knapsack(i - 1, wt, val, j)
        else:
            val = max(
                mf_knapsack(i - 1, wt, val, j),
                mf_knapsack(i - 1, wt, val, j - wt[i - 1]) + val[i - 1],
            )
        f[i][j] = val
    return f[i][j]


def knapsack(w, wt, val, n):
    dp = [[0] * (w + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w_ in range(1, w + 1):
            if wt[i - 1] <= w_:
                dp[i][w_] = max(val[i - 1] + dp[i - 1][w_ - wt[i - 1]], dp[i - 1][w_])
            else:
                dp[i][w_] = dp[i - 1][w_]

    return dp[n][w_], dp


def knapsack_with_example_solution(w: int, wt: list, val: list):
    """
    求解整数重量背包问题，并返回多个可能最优子集中的一个。

    参数
    ----------

    * `w`: int，给定背包问题允许的最大总重量。
    * `wt`: list，所有物品的重量向量，其中 ``wt[i]`` 是第 ``i`` 个物品的重量。
    * `val`: list，所有物品的价值向量，其中 ``val[i]`` 是第 ``i`` 个物品的价值。

    返回
    -------

    * `optimal_val`: float，给定背包问题的最优值。
    * `example_optional_set`: set，产生最优值的一个最优子集的索引。

    示例
    --------

    >>> knapsack_with_example_solution(10, [1, 3, 5, 2], [10, 20, 100, 22])
    (142, {2, 3, 4})
    >>> knapsack_with_example_solution(6, [4, 3, 2, 3], [3, 2, 4, 4])
    (8, {3, 4})
    >>> knapsack_with_example_solution(6, [4, 3, 2, 3], [3, 2, 4])
    Traceback (most recent call last):
        ...
    ValueError: The number of weights must be the same as the number of values.
    But got 4 weights and 3 values
    """
    if not (isinstance(wt, (list, tuple)) and isinstance(val, (list, tuple))):
        raise ValueError(
            "Both the weights and values vectors must be either lists or tuples"
        )

    num_items = len(wt)
    if num_items != len(val):
        msg = (
            "The number of weights must be the same as the number of values.\n"
            f"But got {num_items} weights and {len(val)} values"
        )
        raise ValueError(msg)
    for i in range(num_items):
        if not isinstance(wt[i], int):
            msg = (
                "All weights must be integers but got weight of "
                f"type {type(wt[i])} at index {i}"
            )
            raise TypeError(msg)

    optimal_val, dp_table = knapsack(w, wt, val, num_items)
    example_optional_set: set = set()
    _construct_solution(dp_table, wt, num_items, w, example_optional_set)

    return optimal_val, example_optional_set


def _construct_solution(dp: list, wt: list, i: int, j: int, optimal_set: set) -> None:
    """
    根据已填充的 DP 表和重量向量，递归重建一个最优子集。

    参数
    ----------

    * `dp`: list of list，已求解的整数重量动态规划问题表。
    * `wt`: list or tuple，物品的重量向量。
    * `i`: int，当前考虑的物品索引。
    * `j`: int，当前可能的最大重量。
    * `optimal_set`: set，当前的最优子集。此函数会修改它。

    返回
    -------

    ``None``
    """
    # 要使最大重量 j 下的当前物品 i 成为最优子集的一部分，
    # (i, j) 处的最优值必须大于 (i-1, j) 处的最优值。
    # 其中 i - 1 表示在给定最大重量下只考虑之前的物品
    if i > 0 and j > 0:
        if dp[i - 1][j] == dp[i][j]:
            _construct_solution(dp, wt, i - 1, j, optimal_set)
        else:
            optimal_set.add(i)
            _construct_solution(dp, wt, i - 1, j - wt[i - 1], optimal_set)


if __name__ == "__main__":
    """
    添加背包问题测试用例
    """
    val = [3, 2, 4, 4]
    wt = [4, 3, 2, 3]
    n = 4
    w = 6
    f = [[0] * (w + 1)] + [[0] + [-1] * (w + 1) for _ in range(n + 1)]
    optimal_solution, _ = knapsack(w, wt, val, n)
    print(optimal_solution)
    print(mf_knapsack(n, wt, val, w))  # 交换了 n 和 w

    # 使用示例测试动态规划问题
    # 上述示例的最优子集是物品 3 和 4
    optimal_solution, optimal_subset = knapsack_with_example_solution(w, wt, val)
    assert optimal_solution == 8
    assert optimal_subset == {3, 4}
    print("optimal_value = ", optimal_solution)
    print("An optimal subset corresponding to the optimal value", optimal_subset)
