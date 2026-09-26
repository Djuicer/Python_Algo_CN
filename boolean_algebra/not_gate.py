"""
非门（NOT Gate）是布尔代数中的一种逻辑门。输入为高电平时输出 0（False），
输入为低电平时输出 1（True）。
以下是异或门的真值表：
    ------------------------------
    |  输入   |   输出  |
    ------------------------------
    |    0    |    1    |
    |    1    |    0    |
    ------------------------------
参考资料：https://www.geeksforgeeks.org/logic-gates-in-python/
"""


def not_gate(input_1: int) -> int:
    """
    计算输入值的逻辑非。
    >>> not_gate(0)
    1
    >>> not_gate(1)
    0
    """

    return 1 if input_1 == 0 else 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
