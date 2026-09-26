"""
在二进制与格雷码（Gray Code）表示之间转换。

格雷码（又称反射二进制码）是一种相邻两个数值仅有一位不同的二进制编码。
这一特性使其适用于纠错、数字通信和位置编码器。

Wikipedia: https://en.wikipedia.org/wiki/Gray_code
"""


def binary_to_gray(binary_number: int) -> int:
    """
    将二进制数转换为等价的格雷码。

    算法将二进制数与自身右移 1 位后的结果进行异或。
    公式：gray = binary XOR (binary >> 1)

    参数：
        binary_number：表示二进制数的非负整数

    返回：
        以整数表示的等价格雷码

    示例：
    >>> binary_to_gray(0)
    0
    >>> binary_to_gray(1)
    1
    >>> binary_to_gray(2)
    3
    >>> binary_to_gray(3)
    2
    >>> binary_to_gray(4)
    6
    >>> binary_to_gray(7)
    4
    >>> binary_to_gray(10)
    15
    >>> binary_to_gray(15)
    8
    >>> binary_to_gray(255)
    128
    >>> binary_to_gray(-1)
    Traceback (most recent call last):
        ...
    ValueError: Input must be a non-negative integer
    >>> binary_to_gray(3.5)
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    """
    if not isinstance(binary_number, int):
        raise TypeError("Input must be an integer")
    if binary_number < 0:
        raise ValueError("Input must be a non-negative integer")

    return binary_number ^ (binary_number >> 1)


def gray_to_binary(gray_number: int) -> int:
    """
    将格雷码数转换为等价的二进制数。

    算法反复将格雷码与其自身右移后的结果进行异或，
    直到右移后的值变为 0。

    参数：
        gray_number：表示格雷码的非负整数

    返回：
        以整数表示的等价二进制数

    示例：
    >>> gray_to_binary(0)
    0
    >>> gray_to_binary(1)
    1
    >>> gray_to_binary(3)
    2
    >>> gray_to_binary(2)
    3
    >>> gray_to_binary(6)
    4
    >>> gray_to_binary(4)
    7
    >>> gray_to_binary(15)
    10
    >>> gray_to_binary(8)
    15
    >>> gray_to_binary(128)
    255
    >>> gray_to_binary(-1)
    Traceback (most recent call last):
        ...
    ValueError: Input must be a non-negative integer
    >>> gray_to_binary(5.5)
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    """
    if not isinstance(gray_number, int):
        raise TypeError("Input must be an integer")
    if gray_number < 0:
        raise ValueError("Input must be a non-negative integer")

    binary_number = gray_number
    gray_number >>= 1

    while gray_number:
        binary_number ^= gray_number
        gray_number >>= 1

    return binary_number


def decimal_to_gray(decimal_number: int) -> str:
    """
    将十进制数转换为以二进制字符串表示的格雷码。

    参数：
        decimal_number：非负十进制整数

    返回：
        以二进制字符串表示的格雷码

    示例：
    >>> decimal_to_gray(0)
    '0'
    >>> decimal_to_gray(1)
    '1'
    >>> decimal_to_gray(2)
    '11'
    >>> decimal_to_gray(3)
    '10'
    >>> decimal_to_gray(4)
    '110'
    >>> decimal_to_gray(10)
    '1111'
    >>> decimal_to_gray(15)
    '1000'
    >>> decimal_to_gray(-1)
    Traceback (most recent call last):
        ...
    ValueError: Input must be a non-negative integer
    """
    if not isinstance(decimal_number, int):
        raise TypeError("Input must be an integer")
    if decimal_number < 0:
        raise ValueError("Input must be a non-negative integer")

    gray_code = binary_to_gray(decimal_number)
    return bin(gray_code)[2:]  # 移除 '0b' 前缀


def gray_to_decimal(gray_string: str) -> int:
    """
    将格雷码二进制字符串转换为等价的十进制数。

    参数：
        gray_string：由 0 和 1 组成、表示格雷码的字符串

    返回：
        以整数表示的等价十进制数

    示例：
    >>> gray_to_decimal('0')
    0
    >>> gray_to_decimal('1')
    1
    >>> gray_to_decimal('11')
    2
    >>> gray_to_decimal('10')
    3
    >>> gray_to_decimal('110')
    4
    >>> gray_to_decimal('1111')
    10
    >>> gray_to_decimal('1000')
    15
    >>> gray_to_decimal('invalid')
    Traceback (most recent call last):
        ...
    ValueError: Invalid binary string
    >>> gray_to_decimal('')
    Traceback (most recent call last):
        ...
    ValueError: Input string cannot be empty
    """
    if not gray_string:
        raise ValueError("Input string cannot be empty")

    # 验证二进制字符串
    if not all(bit in "01" for bit in gray_string):
        raise ValueError("Invalid binary string")

    gray_number = int(gray_string, 2)
    return gray_to_binary(gray_number)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 交互式演示
    print("=== Binary to Gray Code Converter ===\n")

    # 演示 0 到 15 的转换
    print("Decimal | Binary   | Gray Code")
    print("--------|----------|----------")
    for i in range(16):
        binary = bin(i)[2:].zfill(4)
        gray = decimal_to_gray(i).zfill(4)
        print(f"{i:7} | {binary:8} | {gray:9}")

    print("\n=== Verification: Gray to Binary ===\n")
    print("Gray Code | Binary   | Decimal")
    print("----------|----------|--------")
    for i in range(16):
        gray = decimal_to_gray(i).zfill(4)
        decimal = gray_to_decimal(gray)
        binary = bin(decimal)[2:].zfill(4)
        print(f"{gray:9} | {binary:8} | {decimal:7}")
