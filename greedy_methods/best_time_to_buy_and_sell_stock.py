"""
给定股票价格列表，计算只买卖一股股票一次
所能获得的最大利润。只允许完成一次买入
和一次卖出交易，且必须先买后卖。

示例：prices = [7, 1, 5, 3, 6, 4]
max_profit 返回 5，即以价格 1 买入、以价格 6 卖出。

该问题可以使用贪心算法（Greedy Algorithm）求解。

只遍历价格数组一次，记录最低价格
（买入价）以及截至每个位置可获得的最大利润。每一步的贪心选择是：
如果当前价格低于已记录的买入价，就以当前价格买入；或者，
如果当前卖出的利润超过已记录的最大利润，就以当前价格卖出。
"""


def max_profit(prices: list[int]) -> int:
    """
    >>> max_profit([7, 1, 5, 3, 6, 4])
    5
    >>> max_profit([7, 6, 4, 3, 1])
    0
    """
    if not prices:
        return 0

    min_price = prices[0]
    max_profit: int = 0

    for price in prices:
        min_price = min(price, min_price)
        max_profit = max(price - min_price, max_profit)

    return max_profit


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(max_profit([7, 1, 5, 3, 6, 4]))
