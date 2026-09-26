"""0-N 背包问题（Knapsack Problem）的递归实现。
https://en.wikipedia.org/wiki/Knapsack_problem
"""

from __future__ import annotations

from functools import lru_cache


def knapsack(
    capacity: int,
    weights: list[int],
    values: list[int],
    counter: int,
    allow_repetition=False,
) -> int:
    """
    返回容量为 cap 的背包能够装入的最大价值，其中每个重量 w 都有对应价值 val，
    并可选择是否允许重复选取物品。

    >>> cap = 50
    >>> val = [60, 100, 120]
    >>> w = [10, 20, 30]
    >>> c = len(val)
    >>> knapsack(cap, w, val, c)
    220

    不允许重复选取时，结果为 220，因为价值 100 和 120 对应物品的总重量为 50，
    恰好达到容量上限。
    >>> knapsack(cap, w, val, c, True)
    300

    允许重复选取时，结果为 300，因为价值为 60 的物品选取 5 次，
    总价值为 60*5，总重量为 10*5，恰好达到容量上限。
    """

    @lru_cache
    def knapsack_recur(capacity: int, counter: int) -> int:
        # 基本情况
        if counter == 0 or capacity == 0:
            return 0

        # 如果第 n 个物品的重量超过背包容量，
        #   则该物品不能加入最优解；
        # 否则返回以下两种情况的最大值：
        #   (1) allow_repetition 为 False 时，第 n 个物品只选一次（0-1）；
        #       allow_repetition 为 True 时，第 n 个物品选取一次或多次（0-N）
        #   (2) 不选取该物品
        if weights[counter - 1] > capacity:
            return knapsack_recur(capacity, counter - 1)
        else:
            left_capacity = capacity - weights[counter - 1]
            new_value_included = values[counter - 1] + knapsack_recur(
                left_capacity, counter - 1 if not allow_repetition else counter
            )
            without_new_value = knapsack_recur(capacity, counter - 1)
            return max(new_value_included, without_new_value)

    return knapsack_recur(capacity, counter)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
