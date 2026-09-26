"""
同或门（XNOR Gate）是布尔代数中的一种逻辑门。两个输入不同时输出 0（False），
输入相同时输出 1（True）。它相当于在异或门后连接非门。

以下是同或门的真值表：
    ------------------------------
    |  输入 1 |  输入 2 |  输出  |
    ------------------------------
    |    0    |    0    |    1   |
    |    0    |    1    |    0   |
    |    1    |    0    |    0   |
    |    1    |    1    |    1   |
    ------------------------------
参考资料：https://www.geeksforgeeks.org/logic-gates-in-python/
"""


def xnor_gate(input_1: int, input_2: int) -> int:
    """
    计算输入值的逻辑同或。
    >>> xnor_gate(0, 0)
    1
    >>> xnor_gate(0, 1)
    0
    >>> xnor_gate(1, 0)
    0
    >>> xnor_gate(1, 1)
    1
    """
    return 1 if input_1 == input_2 else 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
