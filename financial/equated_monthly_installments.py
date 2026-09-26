"""
根据以下信息计算每月摊还金额：
- 借款本金
- 年利率
- 贷款偿还年限

维基百科参考资料：https://en.wikipedia.org/wiki/Equated_monthly_installment
"""


def equated_monthly_installments(
    principal: float, rate_per_annum: float, years_to_repay: int
) -> float:
    """
    每月摊还金额公式：
    A = p * r * (1 + r)^n / ((1 + r)^n - 1)
    其中 p 为本金，r 为月利率，n 为付款次数。

    >>> equated_monthly_installments(25000, 0.12, 3)
    830.3577453212793
    >>> equated_monthly_installments(25000, 0.12, 10)
    358.67737100646826
    >>> equated_monthly_installments(0, 0.12, 3)
    Traceback (most recent call last):
        ...
    Exception: Principal borrowed must be > 0
    >>> equated_monthly_installments(25000, -1, 3)
    Traceback (most recent call last):
        ...
    Exception: Rate of interest must be >= 0
    >>> equated_monthly_installments(25000, 0.12, 0)
    Traceback (most recent call last):
        ...
    Exception: Years to repay must be an integer > 0
    """
    if principal <= 0:
        raise Exception("Principal borrowed must be > 0")
    if rate_per_annum < 0:
        raise Exception("Rate of interest must be >= 0")
    if years_to_repay <= 0 or not isinstance(years_to_repay, int):
        raise Exception("Years to repay must be an integer > 0")

    # 年利率除以 12 得到月利率
    rate_per_month = rate_per_annum / 12

    # 按月付款，因此还款年数乘以 12 得到付款次数
    number_of_payments = years_to_repay * 12

    return (
        principal
        * rate_per_month
        * (1 + rate_per_month) ** number_of_payments
        / ((1 + rate_per_month) ** number_of_payments - 1)
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
