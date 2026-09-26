"""
在会计中，折旧是指固定资产在使用寿命内的价值减少。组织购买固定资产时，购买
支出不会立即确认为费用，而是将资产价值的减少在资产使用年限内逐年确认为费用。

会计中广泛使用以下折旧计算方法：
- 直线法
- 余额递减法
- 工作量法

直线法最简单且应用最广。该方法将成本均匀分摊到资产的使用寿命内以计算折旧。

年度折旧费用的计算公式如下：

- annual depreciation expense =
    (purchase cost of asset - residual value) / useful life of asset(years)

更多信息：
https://en.wikipedia.org/wiki/Depreciation

函数 straight_line_depreciation 返回给定期间内的折旧费用列表。
"""


def straight_line_depreciation(
    useful_years: int,
    purchase_value: float,
    residual_value: float = 0.0,
) -> list[float]:
    """
    计算给定期间内的折旧费用。
    :param useful_years: 资产的使用年数
    :param purchase_value: 资产的购买支出
    :param residual_value: 资产使用寿命结束时的残值
    :return: 资产使用寿命内的年度折旧费用列表
    >>> straight_line_depreciation(10, 1100.0, 100.0)
    [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
    >>> straight_line_depreciation(6, 1250.0, 50.0)
    [200.0, 200.0, 200.0, 200.0, 200.0, 200.0]
    >>> straight_line_depreciation(4, 1001.0)
    [250.25, 250.25, 250.25, 250.25]
    >>> straight_line_depreciation(11, 380.0, 50.0)
    [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0]
    >>> straight_line_depreciation(1, 4985, 100)
    [4885.0]
    """

    if not isinstance(useful_years, int):
        raise TypeError("Useful years must be an integer")

    if useful_years < 1:
        raise ValueError("Useful years cannot be less than 1")

    if not isinstance(purchase_value, (float, int)):
        raise TypeError("Purchase value must be numeric")

    if not isinstance(residual_value, (float, int)):
        raise TypeError("Residual value must be numeric")

    if purchase_value < 0.0:
        raise ValueError("Purchase value cannot be less than zero")

    if purchase_value < residual_value:
        raise ValueError("Purchase value cannot be less than residual value")

    # 计算年度折旧费用
    depreciable_cost = purchase_value - residual_value
    annual_depreciation_expense = depreciable_cost / useful_years

    # 年度折旧费用列表
    list_of_depreciation_expenses = []
    accumulated_depreciation_expense = 0.0
    for period in range(useful_years):
        if period != useful_years - 1:
            accumulated_depreciation_expense += annual_depreciation_expense
            list_of_depreciation_expenses.append(annual_depreciation_expense)
        else:
            depreciation_expense_in_end_year = (
                depreciable_cost - accumulated_depreciation_expense
            )
            list_of_depreciation_expenses.append(depreciation_expense_in_end_year)

    return list_of_depreciation_expenses


if __name__ == "__main__":
    user_input_useful_years = int(input("Please Enter Useful Years:\n > "))
    user_input_purchase_value = float(input("Please Enter Purchase Value:\n > "))
    user_input_residual_value = float(input("Please Enter Residual Value:\n > "))
    print(
        straight_line_depreciation(
            user_input_useful_years,
            user_input_purchase_value,
            user_input_residual_value,
        )
    )
