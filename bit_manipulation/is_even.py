def is_even(number: int) -> bool:
    """使用位运算检查输入整数是否为偶数，是则返回 True。

    说明：
    在二进制表示中，偶数的最低有效位始终为 0，而奇数的最低有效位为 1。
    因此，``n & 1 == 0`` 表示该数为偶数。

    >>> is_even(1)
    False
    >>> is_even(4)
    True
    >>> is_even(9)
    False
    >>> is_even(15)
    False
    >>> is_even(40)
    True
    >>> is_even(100)
    True
    >>> is_even(101)
    False
    >>> is_even(True)
    Traceback (most recent call last):
        ...
    TypeError: input must be an integer
    >>> is_even(3.14)
    Traceback (most recent call last):
        ...
    TypeError: input must be an integer
    """
    if not isinstance(number, int) or isinstance(number, bool):
        # bool 是 int 的子类；这里明确禁止将其作为数字传入。
        raise TypeError("input must be an integer")
    return (number & 1) == 0


def is_even_using_shift_operator(number: int) -> bool:
    """
    如果输入整数为偶数，则返回 True。

    说明：
    在二进制表示中，偶数以 0 结尾，奇数以 1 结尾。
    示例：
    2  -> 10
    3  -> 11
    4  -> 100
    5  -> 101

    奇数的末位始终为 1。
    使用移位运算：
    (n >> 1) << 1 会移除末位。
    如果结果等于 n，则 n 为偶数。

    >>> is_even_using_shift_operator(1)
    False
    >>> is_even_using_shift_operator(4)
    True
    >>> is_even_using_shift_operator(9)
    False
    >>> is_even_using_shift_operator(15)
    False
    >>> is_even_using_shift_operator(40)
    True
    >>> is_even_using_shift_operator(100)
    True
    >>> is_even_using_shift_operator(101)
    False
    """
    return (number >> 1) << 1 == number


if __name__ == "__main__":
    import doctest

    doctest.testmod()
