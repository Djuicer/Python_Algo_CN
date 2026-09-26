def show_bits(before: int, after: int) -> str:
    """
    >>> print(show_bits(0, 0xFFFF))
        0: 00000000
    65535: 1111111111111111
    """
    return f"{before:>5}: {before:08b}\n{after:>5}: {after:08b}"


def swap_odd_even_bits(num: int) -> int:
    """
    1. 使用按位与运算分离输入数字中的偶数位（0、2、4、6 等）和
       奇数位（1、3、5、7 等）。
    2. 将偶数位右移一位、奇数位左移一位，从而交换它们。
    3. 最后，使用按位或运算合并交换后的偶数位和奇数位，得到最终结果。
    >>> print(show_bits(0, swap_odd_even_bits(0)))
        0: 00000000
        0: 00000000
    >>> print(show_bits(1, swap_odd_even_bits(1)))
        1: 00000001
        2: 00000010
    >>> print(show_bits(2, swap_odd_even_bits(2)))
        2: 00000010
        1: 00000001
    >>> print(show_bits(3, swap_odd_even_bits(3)))
        3: 00000011
        3: 00000011
    >>> print(show_bits(4, swap_odd_even_bits(4)))
        4: 00000100
        8: 00001000
    >>> print(show_bits(5, swap_odd_even_bits(5)))
        5: 00000101
       10: 00001010
    >>> print(show_bits(6, swap_odd_even_bits(6)))
        6: 00000110
        9: 00001001
    >>> print(show_bits(23, swap_odd_even_bits(23)))
       23: 00010111
       43: 00101011
    """
    # 获取所有偶数位：0xAAAAAAAA 是所有偶数位均为 1 的 32 位数
    even_bits = num & 0xAAAAAAAA

    # 获取所有奇数位：0x55555555 是所有奇数位均为 1 的 32 位数
    odd_bits = num & 0x55555555

    # 将偶数位右移、奇数位左移，从而交换它们
    return even_bits >> 1 | odd_bits << 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for i in (-1, 0, 1, 2, 3, 4, 23, 24):
        print(show_bits(i, swap_odd_even_bits(i)), "\n")
