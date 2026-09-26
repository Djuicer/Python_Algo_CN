"""
非蕴含门（NIMPLY Gate）是布尔代数中的一种逻辑门。输入 1 为 0 时输出为 0；
输入 1 为 1 时，仅当输入 2 为 1，输出才为 0。
当输入 1 蕴含输入 2 时，其结果为假。它是蕴含运算的否定形式。

以下是非蕴含门的真值表：
    ------------------------------
    |  输入 1 |  输入 2 |  输出  |
    ------------------------------
    |    0    |    0    |    0   |
    |    0    |    1    |    0   |
    |    1    |    0    |    1   |
    |    1    |    1    |    0   |
    ------------------------------

参考资料：https://en.wikipedia.org/wiki/NIMPLY_gate
"""


def nimply_gate(input_1: int, input_2: int) -> int:
    """
    计算输入值的逻辑非蕴含。

    >>> nimply_gate(0, 0)
    0
    >>> nimply_gate(0, 1)
    0
    >>> nimply_gate(1, 0)
    1
    >>> nimply_gate(1, 1)
    0
    """
    return int(input_1 == 1 and input_2 == 0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
