def excess_3_code(number: int) -> str:
    """
    求十进制整数的余 3 码（Excess-3 Code）。
    将十进制数的每一位加 3，再转换为二进制编码十进制数。
    https://en.wikipedia.org/wiki/Excess-3

    >>> excess_3_code(0)
    '0b0011'
    >>> excess_3_code(3)
    '0b0110'
    >>> excess_3_code(2)
    '0b0101'
    >>> excess_3_code(20)
    '0b01010011'
    >>> excess_3_code(120)
    '0b010001010011'
    """
    num = ""
    for digit in str(max(0, number)):
        num += str(bin(int(digit) + 3))[2:].zfill(4)
    return "0b" + num


if __name__ == "__main__":
    import doctest

    doctest.testmod()
