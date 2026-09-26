# 二进制补码（Two's Complement）相关资料：https://en.wikipedia.org/wiki/Two%27s_complement


def twos_complement(number: int) -> str:
    """
    接收一个负整数 'number'。
    返回 'number' 的二进制补码表示。

    >>> twos_complement(0)
    '0b0'
    >>> twos_complement(-1)
    '0b11'
    >>> twos_complement(-5)
    '0b1011'
    >>> twos_complement(-17)
    '0b101111'
    >>> twos_complement(-207)
    '0b100110001'
    >>> twos_complement(1)
    Traceback (most recent call last):
        ...
    ValueError: input must be a negative integer
    """
    if number > 0:
        raise ValueError("input must be a negative integer")
    binary_number_length = len(bin(number)[3:])
    twos_complement_number = bin(abs(number) - (1 << binary_number_length))[3:]
    twos_complement_number = (
        (
            "1"
            + "0" * (binary_number_length - len(twos_complement_number))
            + twos_complement_number
        )
        if number < 0
        else "0"
    )
    return "0b" + twos_complement_number


if __name__ == "__main__":
    import doctest

    doctest.testmod()
