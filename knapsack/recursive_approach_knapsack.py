# 理解使用朴素递归方法求解背包问题


"""
一位店主有若干袋小麦，每袋的重量和利润各不相同。
例如：
no_of_items 4
profit 5 4 8 6
weight 1 2 4 5
max_weight 5
约束：
max_weight > 0
profit[i] >= 0
weight[i] >= 0
在给定最大承载重量的条件下，计算店主可以获得的最大利润。
"""


def knapsack(
    weights: list, values: list, number_of_items: int, max_weight: int, index: int
) -> int:
    """
    函数说明如下：
    :param weights: 重量列表
    :param values: 与各重量对应的利润列表
    :param number_of_items: 可供选择的物品数量
    :param max_weight: 最大承载重量
    :param index: 当前考察的元素
    :return: 最大预期收益
    >>> knapsack([1, 2, 4, 5], [5, 4, 8, 6], 4, 5, 0)
    13
    >>> knapsack([3 ,4 , 5], [10, 9 , 8], 3, 25, 0)
    27
    """
    if index == number_of_items:
        return 0
    ans1 = 0
    ans2 = 0
    ans1 = knapsack(weights, values, number_of_items, max_weight, index + 1)
    if weights[index] <= max_weight:
        ans2 = values[index] + knapsack(
            weights, values, number_of_items, max_weight - weights[index], index + 1
        )
    return max(ans1, ans2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
