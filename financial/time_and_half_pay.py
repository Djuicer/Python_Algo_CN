"""
计算 1.5 倍加班工资。
"""


def pay(hours_worked: float, pay_rate: float, hours: float = 40) -> float:
    """
    hours_worked = 总工作时数
    pay_rate = 每小时工资
    hours = 开始获得 1.5 倍工资前必须工作的时数

    >>> pay(41, 1)
    41.5
    >>> pay(65, 19)
    1472.5
    >>> pay(10, 1)
    10.0
    """
    # 检查所有输入参数是否为浮点数或整数
    assert isinstance(hours_worked, (float, int)), (
        "Parameter 'hours_worked' must be of type 'int' or 'float'"
    )
    assert isinstance(pay_rate, (float, int)), (
        "Parameter 'pay_rate' must be of type 'int' or 'float'"
    )
    assert isinstance(hours, (float, int)), (
        "Parameter 'hours' must be of type 'int' or 'float'"
    )

    normal_pay = hours_worked * pay_rate
    over_time = max(0, hours_worked - hours)
    over_time_pay = over_time * pay_rate / 2
    return normal_pay + over_time_pay


if __name__ == "__main__":
    # 测试
    import doctest

    doctest.testmod()
