# 通过背包问题理解贪心算法（Greedy Algorithm）


"""
一位店主有若干袋小麦，每袋的重量和利润各不相同。
例如：
profit 5 8 7 1 12 3 4
weight 2 7 1 6  4 2 5
max_weight 100

约束：
max_weight > 0
profit[i] >= 0
weight[i] >= 0
在给定最大承载重量的条件下，计算店主可以获得的最大利润。
"""


def calc_profit(profit: list, weight: list, max_weight: int) -> int:
    """
    函数说明如下：
    :param profit: 利润列表
    :param weight: 与利润对应的各袋重量列表
    :param max_weight: 最大承载重量
    :return: 最大预期收益

    >>> calc_profit([1, 2, 3], [3, 4, 5], 15)
    6
    >>> calc_profit([10, 9 , 8], [3 ,4 , 5], 25)
    27
    """
    if len(profit) != len(weight):
        raise ValueError("The length of profit and weight must be same.")
    if max_weight <= 0:
        raise ValueError("max_weight must greater than zero.")
    if any(p < 0 for p in profit):
        raise ValueError("Profit can not be negative.")
    if any(w < 0 for w in weight):
        raise ValueError("Weight can not be negative.")

    # 创建列表，分别存储各种重量下每 1kg 可获得的利润。
    # 计算每个元素的 profit/weight 并添加到列表。
    profit_by_weight = [p / w for p, w in zip(profit, weight)]

    # 创建列表副本，并按升序排列 profit/weight
    sorted_profit_by_weight = sorted(profit_by_weight)

    # 声明所需变量
    length = len(sorted_profit_by_weight)
    limit = 0
    gain = 0
    i = 0

    # 在总重量未达到最大限制（例如 15kg）且 i < length 时循环
    while limit <= max_weight and i < length:
        # 标记 sorted_profit_by_weight 中遇到的最大元素
        biggest_profit_by_weight = sorted_profit_by_weight[length - i - 1]
        """
        计算 biggest_profit_by_weight 在 profit_by_weight 列表中的索引。
        这会得到第一个与 biggest_profit_by_weight 相同的元素的索引。
        可能有一个或多个相同值，但 index 始终只返回第一个元素。
        为避免重复使用，元素用过后就修改 profit_by_weight 中的对应值；
        此处将其设为 -1，因为 profit 和 weight 都不能为负数。
        """
        index = profit_by_weight.index(biggest_profit_by_weight)
        profit_by_weight[index] = -1

        # 检查当前重量是否小于此前剩余的可承载重量
        if max_weight - limit >= weight[index]:
            limit += weight[index]
            # 添加给定重量可获得的利润，1 ===
            # weight[index]/weight[index]
            gain += 1 * profit[index]
        else:
            # 当前重量超过剩余限制，因此只取所需的剩余千克数并计算其利润。
            # 剩余重量 / weight[index]
            gain += (max_weight - limit) / weight[index] * profit[index]
            break
        i += 1
    return gain


if __name__ == "__main__":
    print(
        "Input profits, weights, and then max_weight (all positive ints) separated by "
        "spaces."
    )

    profit = [int(x) for x in input("Input profits separated by spaces: ").split()]
    weight = [int(x) for x in input("Input weights separated by spaces: ").split()]
    max_weight = int(input("Max weight allowed: "))

    # 函数调用
    calc_profit(profit, weight, max_weight)
