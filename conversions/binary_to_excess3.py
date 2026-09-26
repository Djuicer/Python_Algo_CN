def binary_to_excess3(binary_str: str) -> str:
    """
    将以字符串表示的二进制数转换为余 3 码（Excess-3）。
    https://en.wikipedia.org/wiki/Excess-3

    参数：
        binary_str (str)：以字符串表示的二进制数（例如 "1010"）。

    返回：
        str：以二进制字符串表示的余 3 码。

    示例：
        >>> binary_to_excess3("1010")
        '1101'
    """
    # 将二进制转换为十进制
    decimal_value = int(binary_str, 2)

    # 加 3（余 3 编码）
    excess3_value = decimal_value + 3

    # 转换回 4 位二进制
    excess3_binary = format(excess3_value, "04b")

    return excess3_binary


if __name__ == "__main__":
    from dostest import testmod

    testmod()
    binary_input = input("Enter a 4-bit binary number: ")
    excess3_output = binary_to_excess3(binary_input)
    print(f"Excess-3 code of {binary_input} is: {excess3_output}")
