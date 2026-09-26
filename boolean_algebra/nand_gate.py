"""
与非门（NAND Gate）是布尔代数中的一种逻辑门。当两个输入均为 1 时，
其输出为 0（False）；否则输出为 1（True）。它相当于在与门后连接非门。
以下是与非门的真值表：
    ------------------------------
    |  输入 1 |  输入 2 |  输出  |
    ------------------------------
    |    0    |    0    |    1   |
    |    0    |    1    |    1   |
    |    1    |    0    |    1   |
    |    1    |    1    |    0   |
    ------------------------------
参考资料：https://www.geeksforgeeks.org/logic-gates-in-python/
"""


def nand_gate(input_1: int, input_2: int) -> int:
    """
    计算输入值的逻辑与非。
    >>> nand_gate(0, 0)
    1
    >>> nand_gate(0, 1)
    1
    >>> nand_gate(1, 0)
    1
    >>> nand_gate(1, 1)
    0
    """
    return int(not (input_1 and input_2))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
