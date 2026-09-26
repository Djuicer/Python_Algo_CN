def binary_coded_decimal(number: int) -> str:
    """
    求十进制整数的二进制编码十进制（Binary-Coded Decimal，BCD）表示。
    数字的每一位均用 4 位二进制数表示。
    示例：
    >>> binary_coded_decimal(-2)
    '0b0000'
    >>> binary_coded_decimal(-1)
    '0b0000'
    >>> binary_coded_decimal(0)
    '0b0000'
    >>> binary_coded_decimal(3)
    '0b0011'
    >>> binary_coded_decimal(2)
    '0b0010'
    >>> binary_coded_decimal(12)
    '0b00010010'
    >>> binary_coded_decimal(987)
    '0b100110000111'
    """
    return "0b" + "".join(
        str(bin(int(digit)))[2:].zfill(4) for digit in str(max(0, number))
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
