"""
蕴含门（IMPLY Gate）是布尔代数中的一种逻辑门。当输入 1 为 0 时输出为 1；
当输入 1 为 1 时，仅当输入 2 为 1，输出才为 1。
输入 1 蕴含输入 2 时，其结果为真。

以下是蕴含门的真值表：
    ------------------------------
    |  输入 1 |  输入 2 |  输出  |
    ------------------------------
    |    0    |    0    |    1   |
    |    0    |    1    |    1   |
    |    1    |    0    |    0   |
    |    1    |    1    |    1   |
    ------------------------------

参考资料：https://en.wikipedia.org/wiki/IMPLY_gate
"""


def imply_gate(input_1: int, input_2: int) -> int:
    """
    计算输入值的逻辑蕴含。

    >>> imply_gate(0, 0)
    1
    >>> imply_gate(0, 1)
    1
    >>> imply_gate(1, 0)
    0
    >>> imply_gate(1, 1)
    1
    """
    return int(input_1 == 0 or input_2 == 1)


def recursive_imply_list(input_list: list[int]) -> int:
    """
    递归计算列表中各项的逻辑蕴含。
    蕴含运算严格按照从左到右的顺序连续执行：
    ( (a -> b) -> c ) -> d ...

    >>> recursive_imply_list([])
    Traceback (most recent call last):
        ...
    ValueError: Input list must contain at least two elements
    >>> recursive_imply_list([0])
    Traceback (most recent call last):
        ...
    ValueError: Input list must contain at least two elements
    >>> recursive_imply_list([1])
    Traceback (most recent call last):
        ...
    ValueError: Input list must contain at least two elements
    >>> recursive_imply_list([0, 0])
    1
    >>> recursive_imply_list([0, 1])
    1
    >>> recursive_imply_list([1, 0])
    0
    >>> recursive_imply_list([1, 1])
    1
    >>> recursive_imply_list([0, 0, 0])
    0
    >>> recursive_imply_list([0, 0, 1])
    1
    >>> recursive_imply_list([0, 1, 0])
    0
    >>> recursive_imply_list([0, 1, 1])
    1
    >>> recursive_imply_list([1, 0, 0])
    1
    >>> recursive_imply_list([1, 0, 1])
    1
    >>> recursive_imply_list([1, 1, 0])
    0
    >>> recursive_imply_list([1, 1, 1])
    1
    """
    if len(input_list) < 2:
        raise ValueError("Input list must contain at least two elements")
    first_implication = imply_gate(input_list[0], input_list[1])
    if len(input_list) == 2:
        return first_implication
    new_list = [first_implication, *input_list[2:]]
    return recursive_imply_list(new_list)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
