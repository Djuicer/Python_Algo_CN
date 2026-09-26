def hex_to_bin(hex_num: str) -> int:
    """
    将十六进制值转换为等价的二进制值。
    #https://stackoverflow.com/questions/1425493/convert-hex-to-binary
    此处使用了按位右移运算符：>>
    它将数字的各位向右移动，并在左侧空位补 0，
    效果类似于将数字除以 2 的某次幂。
    示例：
    a = 10
    a >> 1 = 5

    >>> hex_to_bin("AC")
    10101100
    >>> hex_to_bin("9A4")
    100110100100
    >>> hex_to_bin("   12f   ")
    100101111
    >>> hex_to_bin("FfFf")
    1111111111111111
    >>> hex_to_bin("-fFfF")
    -1111111111111111
    >>> hex_to_bin("F-f")
    Traceback (most recent call last):
        ...
    ValueError: Invalid value was passed to the function
    >>> hex_to_bin("")
    Traceback (most recent call last):
        ...
    ValueError: No value was passed to the function
    """

    hex_num = hex_num.strip()
    if not hex_num:
        raise ValueError("No value was passed to the function")

    is_negative = hex_num[0] == "-"
    if is_negative:
        hex_num = hex_num[1:]

    try:
        int_num = int(hex_num, 16)
    except ValueError:
        raise ValueError("Invalid value was passed to the function")

    bin_str = ""
    while int_num > 0:
        bin_str = str(int_num % 2) + bin_str
        int_num >>= 1

    return int(("-" + bin_str) if is_negative else bin_str)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
