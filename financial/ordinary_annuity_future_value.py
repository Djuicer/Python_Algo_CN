"""
普通年金是指在给定期间内，于每期期末支付或收取款项。
例如，给定期间包含 3 期，每期付款 $1000，则现金流如下：

    0: no payment --- 1: $1000 --- 2: $1000 --- 3: $1000

函数 ordinary_annuity_future_value 计算指定普通年金的终值。在上述示例中，函数
应返回每笔付款在第 3 期末的终值之和，即在最后一笔付款完成时返回该总和。

更多信息：https://www.investopedia.com/retirement/calculating-present-and-future-value-of-annuities

对于期限和利率固定、每期期末定期存款的储蓄方案，此函数可帮助计算最终所得金额。
"""


def ordinary_annuity_future_value(
    term_payment: float, number_of_payments: int, term_interest_rate: float
) -> float:
    """
    计算指定普通年金的终值。
    :param term_payment: 每期期末支付的款项
    :param number_of_payments: 付款次数
    :param term_interest_rate: 每期利率
    :return: 指定普通年金的终值（到期值）

    示例：
    >>> round(ordinary_annuity_future_value(500, 10, 0.05), 2)
    6288.95
    >>> round(ordinary_annuity_future_value(1000, 10, 0.05), 2)
    12577.89
    >>> round(ordinary_annuity_future_value(1000, 10, 0.10), 2)
    15937.42
    >>> round(ordinary_annuity_future_value(1000, 20, 0.10), 2)
    57275.0
    """

    annuity_factor = (
        ((1 + term_interest_rate) ** number_of_payments) - 1
    ) / term_interest_rate
    future_value = term_payment * annuity_factor
    return future_value


if __name__ == "__main__":
    user_input_amount = float(input("How much money will be deposited each term?\n> "))
    user_input_payment_number = int(input("How many payments will be made?\n> "))
    term_interest_rate = float(input("What is the interest rate per term?\n> "))
    print(
        ordinary_annuity_future_value(
            user_input_amount, user_input_payment_number, term_interest_rate
        )
    )
