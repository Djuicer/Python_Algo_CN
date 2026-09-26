"""
期初年金是指在给定期间内，于每期期初支付或收取款项。
例如，给定期间包含 3 期，每期付款 $1000，则现金流如下：

    0: $1000 --- 1: $1000 --- 2: $1000 --- 3: no payment

函数 annuity_due_future_value 给出指定期初年金的终值。在上述示例中，函数应返回
每笔付款在第 3 期末的终值之和。

更多信息：https://www.investopedia.com/retirement/calculating-present-and-future-value-of-annuities

对于期限和利率固定、每期期初定期存款的储蓄方案，此函数可帮助计算最终所得金额。
"""


def annuity_due_future_value(
    term_payment: float, number_of_payments: int, term_interest_rate: float
) -> float:
    """
    计算指定期初年金的终值。
    :param term_payment: 每期期初支付的款项
    :param number_of_payments: 付款次数
    :param term_interest_rate: 每期利率
    :return: 指定期初年金的终值（到期值）

    示例：
    >>> round(annuity_due_future_value(500, 10, 0.05), 2)
    6603.39
    >>> round(annuity_due_future_value(1000, 10, 0.05), 2)
    13206.79
    >>> round(annuity_due_future_value(1000, 10, 0.10), 2)
    17531.17
    >>> round(annuity_due_future_value(1000, 20, 0.10), 2)
    63002.5
    """

    annuity_factor = (
        ((1 + term_interest_rate) ** number_of_payments) - 1
    ) / term_interest_rate
    future_value = term_payment * annuity_factor * (1 + term_interest_rate)
    return future_value


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    user_input_amount = float(input("How much money will be deposited each term?\n> "))
    user_input_payment_number = int(input("How many payments will be made?\n> "))
    term_interest_rate = float(input("What is the interest rate per term?\n> "))
    print(
        annuity_due_future_value(
            user_input_amount, user_input_payment_number, term_interest_rate
        )
    )
