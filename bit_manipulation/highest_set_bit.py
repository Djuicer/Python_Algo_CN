def get_highest_set_bit_position(number: int) -> int:
    """
    返回一个数的最高置位比特所在位置。
    参考资料：https://graphics.stanford.edu/~seander/bithacks.html#IntegerLogObvious
    >>> get_highest_set_bit_position(25)
    5
    >>> get_highest_set_bit_position(37)
    6
    >>> get_highest_set_bit_position(1)
    1
    >>> get_highest_set_bit_position(4)
    3
    >>> get_highest_set_bit_position(0)
    0
    >>> get_highest_set_bit_position(0.8)
    Traceback (most recent call last):
        ...
    TypeError: Input value must be an 'int' type
    """
    if not isinstance(number, int):
        raise TypeError("Input value must be an 'int' type")

    position = 0
    while number:
        position += 1
        number >>= 1

    return position


if __name__ == "__main__":
    import doctest

    doctest.testmod()
