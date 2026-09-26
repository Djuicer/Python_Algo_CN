"""
或门（OR Gate）是布尔代数中的一种逻辑门。当两个输入均为 0 时，
其输出为 0（False）；否则输出为 1（True）。
以下是与门的真值表：
    ------------------------------
    |  输入 1 |  输入 2 |  输出  |
    ------------------------------
    |    0    |    0    |    0   |
    |    0    |    1    |    1   |
    |    1    |    0    |    1   |
    |    1    |    1    |    1   |
    ------------------------------
参考资料：https://www.geeksforgeeks.org/logic-gates-in-python/
"""


def or_gate(input_1: int, input_2: int) -> int:
    """
    计算输入值的逻辑或。
    >>> or_gate(0, 0)
    0
    >>> or_gate(0, 1)
    1
    >>> or_gate(1, 0)
    1
    >>> or_gate(1, 1)
    1
    """
    return int((input_1, input_2).count(1) != 0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
