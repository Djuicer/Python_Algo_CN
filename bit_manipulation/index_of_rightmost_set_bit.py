# 参考资料：https://www.geeksforgeeks.org/position-of-rightmost-set-bit/


def get_index_of_rightmost_set_bit(number: int) -> int:
    """
    接收一个正整数 'number'。
    返回该数从右侧起第一个置位比特的索引（从零开始）。
    如果未找到置位比特，则返回 -1。

    >>> get_index_of_rightmost_set_bit(0)
    -1
    >>> get_index_of_rightmost_set_bit(5)
    0
    >>> get_index_of_rightmost_set_bit(36)
    2
    >>> get_index_of_rightmost_set_bit(8)
    3
    >>> get_index_of_rightmost_set_bit(-18)
    Traceback (most recent call last):
        ...
    ValueError: Input must be a non-negative integer
    >>> get_index_of_rightmost_set_bit('test')
    Traceback (most recent call last):
        ...
    ValueError: Input must be a non-negative integer
    >>> get_index_of_rightmost_set_bit(1.25)
    Traceback (most recent call last):
        ...
    ValueError: Input must be a non-negative integer
    """

    if not isinstance(number, int) or number < 0:
        raise ValueError("Input must be a non-negative integer")

    intermediate = number & ~(number - 1)
    index = 0
    while intermediate:
        intermediate >>= 1
        index += 1
    return index - 1


if __name__ == "__main__":
    """
    查找最右侧置位比特的索引有一些特殊用途，尤其适用于在正整数列表中
    查找缺失和／或重复的数字。
    """
    import doctest

    doctest.testmod(verbose=True)
