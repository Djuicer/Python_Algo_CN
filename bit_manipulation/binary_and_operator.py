"""按位与辅助函数。

返回表示 ``a & b`` 的补零二进制字符串，其宽度为输入值中的最大位数。
仅接受非负整数。

>>> binary_and(25, 32)
'0b000000'
>>> binary_and(37, 50)
'0b100000'
>>> binary_and(21, 30)
'0b10100'
>>> binary_and(58, 73)
'0b0001000'
>>> binary_and(0, 255)
'0b00000000'
>>> binary_and(256, 256)
'0b100000000'

无效输入会引发明确的异常：

>>> binary_and(0, -1)
Traceback (most recent call last):
    ...
ValueError: inputs must be non-negative integers
>>> binary_and(0, 1.1)
Traceback (most recent call last):
    ...
TypeError: inputs must be integers
>>> binary_and("0", "1")
Traceback (most recent call last):
    ...
TypeError: inputs must be integers
"""

# https://www.tutorialspoint.com/python3/bitwise_operators_example.htm


def binary_and(a: int, b: int) -> str:
    """
    接收两个整数并将其转换为二进制，返回对这两个整数执行按位与运算的结果，
    结果以二进制数表示。

    >>> binary_and(25, 32)
    '0b000000'
    >>> binary_and(37, 50)
    '0b100000'
    >>> binary_and(21, 30)
    '0b10100'
    >>> binary_and(58, 73)
    '0b0001000'
    >>> binary_and(0, 255)
    '0b00000000'
    >>> binary_and(256, 256)
    '0b100000000'
    >>> binary_and(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: inputs must be non-negative integers
    >>> binary_and(0, 1.1)
    Traceback (most recent call last):
        ...
    TypeError: inputs must be integers
    >>> binary_and("0", "1")
    Traceback (most recent call last):
        ...
    TypeError: inputs must be integers
    >>> binary_and(10, "1")
    Traceback (most recent call last):
        ...
    TypeError: inputs must be integers
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("inputs must be integers")
    if a < 0 or b < 0:
        raise ValueError("inputs must be non-negative integers")

    a_binary = format(a, "b")
    b_binary = format(b, "b")

    max_len = max(len(a_binary), len(b_binary))

    max_len = max(a.bit_length(), b.bit_length())
    return f"0b{(a & b):0{max_len}b}"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
