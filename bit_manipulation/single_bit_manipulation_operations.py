#!/usr/bin/env python3

"""提供操作单个位的功能。"""


def set_bit(number: int, position: int) -> int:
    """
    将 position 位置的位设为 1。

    细节：对给定的 number 和 X 执行按位或运算。
    X 的所有位均为 0，仅给定位置的位为 1。

    >>> set_bit(0b1101, 1) # 0b1111
    15
    >>> set_bit(0b0, 5) # 0b100000
    32
    >>> set_bit(0b1111, 1) # 0b1111
    15
    """
    return number | (1 << position)


def clear_bit(number: int, position: int) -> int:
    """
    将 position 位置的位设为 0。

    细节：对给定的 number 和 X 执行按位与运算。
    X 的所有位均为 1，仅给定位置的位为 0。

    >>> clear_bit(0b10010, 1) # 0b10000
    16
    >>> clear_bit(0b0, 5) # 0b0
    0
    """
    return number & ~(1 << position)


def flip_bit(number: int, position: int) -> int:
    """
    翻转 position 位置的位。

    细节：对给定的 number 和 X 执行按位异或运算。
    X 的所有位均为 0，仅给定位置的位为 1。

    >>> flip_bit(0b101, 1) # 0b111
    7
    >>> flip_bit(0b101, 0) # 0b100
    4
    """
    return number ^ (1 << position)


def is_bit_set(number: int, position: int) -> bool:
    """
    position 位置的位是否已置位？

    细节：将 position 位置的位移到第一位（最低位），
    再将移位后的数与 1 执行按位与运算，检查第一位是否已置位。

    >>> is_bit_set(0b1010, 0)
    False
    >>> is_bit_set(0b1010, 1)
    True
    >>> is_bit_set(0b1010, 2)
    False
    >>> is_bit_set(0b1010, 3)
    True
    >>> is_bit_set(0b0, 17)
    False
    """
    return ((number >> position) & 1) == 1


def get_bit(number: int, position: int) -> int:
    """
    获取给定位置的位。

    细节：对给定的 number 和 X 执行按位与运算。
    X 的所有位均为 0，仅给定位置的位为 1。
    如果结果不等于 0，则给定位置的位为 1，否则为 0。

    >>> get_bit(0b1010, 0)
    0
    >>> get_bit(0b1010, 1)
    1
    >>> get_bit(0b1010, 2)
    0
    >>> get_bit(0b1010, 3)
    1
    """
    return int((number & (1 << position)) != 0)


def clear_least_significant_set_bit(number: int) -> int:
    """
    清除最低有效置位比特（最右侧的 1）。

    减 1 会将最右侧的 1 变为 0，并将其右侧的各个 0 变为 1。
    因此，将所得结果与原数执行按位与运算即可清除该置位比特。
    对于负整数，使用 Python 的无限符号扩展。
    https://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetKernighan

    >>> clear_least_significant_set_bit(0b101100)  # 0b101000
    40
    >>> clear_least_significant_set_bit(0b1000)  # 0b0
    0
    >>> clear_least_significant_set_bit(0)
    0
    >>> clear_least_significant_set_bit(0b1111)  # 0b1110
    14
    >>> clear_least_significant_set_bit(-5)
    -6
    """
    return number & (number - 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
