"""
参考资料：https://www.investopedia.com/terms/p/presentvalue.asp

此算法根据以下信息计算年度现金流的现值：
1. 贴现率（用小数而非百分数表示）
2. 现金流数组，其中现金流的索引表示对应年份

注意：此算法假设现金流在指定年份末支付。
"""


def present_value(discount_rate: float, cash_flows: list[float]) -> float:
    """
    >>> present_value(0.13, [10, 20.70, -293, 297])
    4.69
    >>> present_value(0.07, [-109129.39, 30923.23, 15098.93, 29734,39])
    -42739.63
    >>> present_value(0.07, [109129.39, 30923.23, 15098.93, 29734,39])
    175519.15
    >>> present_value(-1, [109129.39, 30923.23, 15098.93, 29734,39])
    Traceback (most recent call last):
        ...
    ValueError: Discount rate cannot be negative
    >>> present_value(0.03, [])
    Traceback (most recent call last):
        ...
    ValueError: Cash flows list cannot be empty
    """
    if discount_rate < 0:
        raise ValueError("Discount rate cannot be negative")
    if not cash_flows:
        raise ValueError("Cash flows list cannot be empty")
    present_value = sum(
        cash_flow / ((1 + discount_rate) ** i) for i, cash_flow in enumerate(cash_flows)
    )
    return round(present_value, ndigits=2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
