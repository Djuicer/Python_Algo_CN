# 二进制移位相关资料：
# https://docs.python.org/3/library/stdtypes.html#bitwise-operations-on-integer-types
# https://www.interviewcake.com/concept/java/bit-shift


def logical_left_shift(number: int, shift_amount: int) -> str:
    """
    接收两个正整数。
    'number' 是要逻辑左移 'shift_amount' 位的整数，
    即 (number << shift_amount)。
    返回移位后的二进制表示。

    >>> logical_left_shift(0, 1)
    '0b00'
    >>> logical_left_shift(1, 1)
    '0b10'
    >>> logical_left_shift(1, 5)
    '0b100000'
    >>> logical_left_shift(17, 2)
    '0b1000100'
    >>> logical_left_shift(1983, 4)
    '0b111101111110000'
    >>> logical_left_shift(1, -1)
    Traceback (most recent call last):
        ...
    ValueError: both inputs must be positive integers
    """
    if number < 0 or shift_amount < 0:
        raise ValueError("both inputs must be positive integers")

    binary_number = str(bin(number))
    binary_number += "0" * shift_amount
    return binary_number


def logical_right_shift(number: int, shift_amount: int) -> str:
    """
    接收两个正整数。
    'number' 是要逻辑右移 'shift_amount' 位的整数，
    即 (number >>> shift_amount)。
    返回移位后的二进制表示。

    >>> logical_right_shift(0, 1)
    '0b0'
    >>> logical_right_shift(1, 1)
    '0b0'
    >>> logical_right_shift(1, 5)
    '0b0'
    >>> logical_right_shift(17, 2)
    '0b100'
    >>> logical_right_shift(1983, 4)
    '0b1111011'
    >>> logical_right_shift(1, -1)
    Traceback (most recent call last):
        ...
    ValueError: both inputs must be positive integers
    """
    if number < 0 or shift_amount < 0:
        raise ValueError("both inputs must be positive integers")

    binary_number = str(bin(number))[2:]
    if shift_amount >= len(binary_number):
        return "0b0"
    shifted_binary_number = binary_number[: len(binary_number) - shift_amount]
    return "0b" + shifted_binary_number


def arithmetic_right_shift(number: int, shift_amount: int) -> str:
    """
    接收两个整数。
    'number' 是要算术右移 'shift_amount' 位的整数，
    即 (number >> shift_amount)。
    返回移位后的二进制表示。

    >>> arithmetic_right_shift(0, 1)
    '0b00'
    >>> arithmetic_right_shift(1, 1)
    '0b00'
    >>> arithmetic_right_shift(-1, 1)
    '0b11'
    >>> arithmetic_right_shift(17, 2)
    '0b000100'
    >>> arithmetic_right_shift(-17, 2)
    '0b111011'
    >>> arithmetic_right_shift(-1983, 4)
    '0b111110000100'
    """
    if number >= 0:  # 获取正数的二进制表示
        binary_number = "0" + str(bin(number)).strip("-")[2:]
    else:  # 获取负数的二进制补码表示
        binary_number_length = len(bin(number)[3:])  # 求该数的二进制补码
        binary_number = bin(abs(number) - (1 << binary_number_length))[3:]
        binary_number = (
            "1" + "0" * (binary_number_length - len(binary_number)) + binary_number
        )

    if shift_amount >= len(binary_number):
        return "0b" + binary_number[0] * len(binary_number)
    return (
        "0b"
        + binary_number[0] * shift_amount
        + binary_number[: len(binary_number) - shift_amount]
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
