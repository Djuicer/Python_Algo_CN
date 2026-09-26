"""
异或门（XOR Gate）是布尔代数中的一种逻辑门。两个输入中只有一个为 1 时，
其输出为 1（True）；为 1 的输入数量是偶数时，输出为 0（False）。
以下是异或门的真值表：
    ------------------------------
    |  输入 1 |  输入 2 |  输出  |
    ------------------------------
    |    0    |    0    |    0   |
    |    0    |    1    |    1   |
    |    1    |    0    |    1   |
    |    1    |    1    |    0   |
    ------------------------------

参考资料：https://www.geeksforgeeks.org/logic-gates-in-python/
"""


def xor_gate(input_1: int, input_2: int) -> int:
    """
    计算输入值的逻辑异或。

    >>> xor_gate(0, 0)
    0
    >>> xor_gate(0, 1)
    1
    >>> xor_gate(1, 0)
    1
    >>> xor_gate(1, 1)
    0
    """
    return (input_1, input_2).count(0) % 2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
