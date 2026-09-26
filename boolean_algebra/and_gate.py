"""
与门（AND Gate）是布尔代数中的一种逻辑门。当所有输入均为 1（True）时，
其输出为 1（True）；否则输出为 0（False）。

以下是二输入与门的真值表：
    ------------------------------
    |  输入 1 |  输入 2 |  输出  |
    ------------------------------
    |    0    |    0    |    0   |
    |    0    |    1    |    0   |
    |    1    |    0    |    0   |
    |    1    |    1    |    1   |
    ------------------------------

参考资料：https://www.geeksforgeeks.org/logic-gates/
"""


def and_gate(input_1: int, input_2: int) -> int:
    """
    计算两个二进制输入值的逻辑与。

    >>> and_gate(0, 0)
    0
    >>> and_gate(0, 1)
    0
    >>> and_gate(1, 0)
    0
    >>> and_gate(1, 1)
    1
    >>> and_gate(2, 1)
    Traceback (most recent call last):
        ...
    ValueError: Both inputs must be 0 or 1
    >>> and_gate(0, "1")
    Traceback (most recent call last):
        ...
    TypeError: Both inputs must be integers
    """
    # 类型验证
    if not isinstance(input_1, int) or not isinstance(input_2, int):
        raise TypeError("Both inputs must be integers")

    # 值验证
    if input_1 not in (0, 1) or input_2 not in (0, 1):
        raise ValueError("Both inputs must be 0 or 1")

    return input_1 & input_2


def n_input_and_gate(inputs: list[int]) -> int:
    """
    计算二进制输入值列表的逻辑与。

    >>> n_input_and_gate([1, 0, 1, 1, 0])
    0
    >>> n_input_and_gate([1, 1, 1, 1, 1])
    1
    >>> n_input_and_gate([1, 0, 1, 1, 0])
    0
    >>> n_input_and_gate([])
    Traceback (most recent call last):
        ...
    ValueError: Input list cannot be empty
    >>> n_input_and_gate([1, 2, 1])
    Traceback (most recent call last):
        ...
    ValueError: All inputs in the list must be 0 or 1
    >>> n_input_and_gate([1, "1"])
    Traceback (most recent call last):
        ...
    TypeError: All inputs in the list must be integers
    """
    # 验证列表本身的类型
    if not isinstance(inputs, list):
        raise TypeError("Input must be a list")

    # 验证空列表这一边界情况
    if not inputs:
        raise ValueError("Input list cannot be empty")

    # 验证列表中各项的类型和值
    for item in inputs:
        if not isinstance(item, int):
            raise TypeError("All inputs in the list must be integers")
        if item not in (0, 1):
            raise ValueError("All inputs in the list must be 0 or 1")

    return int(all(inputs))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
