"""将十进制数转换为二进制数。"""


def decimal_to_binary_iterative(num: int) -> str:
    """
    将十进制整数转换为以字符串表示的二进制数。
    >>> decimal_to_binary_iterative(0)
    '0b0'
    >>> decimal_to_binary_iterative(2)
    '0b10'
    >>> decimal_to_binary_iterative(7)
    '0b111'
    >>> decimal_to_binary_iterative(35)
    '0b100011'
    >>> # negatives work too
    >>> decimal_to_binary_iterative(-2)
    '-0b10'
    >>> # other floats will error
    >>> decimal_to_binary_iterative(16.16) # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: 'float' object cannot be interpreted as an integer
    >>> # strings will error as well
    >>> decimal_to_binary_iterative('0xfffff') # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: 'str' object cannot be interpreted as an integer
    """

    if isinstance(num, float):
        raise TypeError("'float' object cannot be interpreted as an integer")
    if isinstance(num, str):
        raise TypeError("'str' object cannot be interpreted as an integer")

    if num == 0:
        return "0b0"

    negative = False

    if num < 0:
        negative = True
        num = -num

    binary: list[int] = []
    while num > 0:
        binary.insert(0, num % 2)
        num >>= 1

    if negative:
        return "-0b" + "".join(str(e) for e in binary)

    return "0b" + "".join(str(e) for e in binary)


def decimal_to_binary_recursive_helper(decimal: int) -> str:
    """
    接收一个正整数并返回其等价的二进制值。
    >>> decimal_to_binary_recursive_helper(1000)
    '1111101000'
    >>> decimal_to_binary_recursive_helper("72")
    '1001000'
    >>> decimal_to_binary_recursive_helper("number")
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for int() with base 10: 'number'
    """
    decimal = int(decimal)
    if decimal in (0, 1):  # 递归的终止条件
        return str(decimal)
    div, mod = divmod(decimal, 2)
    return decimal_to_binary_recursive_helper(div) + str(mod)


def decimal_to_binary_recursive(number: str) -> str:
    """
    接收一个整数值，对错误输入引发 ValueError；调用上方函数，
    并分别为正整数和负整数的输出添加 "0b" 与 "-0b" 前缀。
    >>> decimal_to_binary_recursive(0)
    '0b0'
    >>> decimal_to_binary_recursive(40)
    '0b101000'
    >>> decimal_to_binary_recursive(-40)
    '-0b101000'
    >>> decimal_to_binary_recursive(40.8)
    Traceback (most recent call last):
        ...
    ValueError: Input value is not an integer
    >>> decimal_to_binary_recursive("forty")
    Traceback (most recent call last):
        ...
    ValueError: Input value is not an integer
    """
    number = str(number).strip()
    if not number:
        raise ValueError("No input value was provided")
    negative = "-" if number.startswith("-") else ""
    number = number.lstrip("-")
    if not number.isnumeric():
        raise ValueError("Input value is not an integer")
    return f"{negative}0b{decimal_to_binary_recursive_helper(int(number))}"


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print(decimal_to_binary_recursive(input("Input a decimal number: ")))
