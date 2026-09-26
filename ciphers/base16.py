def base16_encode(data: bytes) -> str:
    """
    将给定字节编码为 Base16。

    >>> base16_encode(b'Hello World!')
    '48656C6C6F20576F726C6421'
    >>> base16_encode(b'HELLO WORLD!')
    '48454C4C4F20574F524C4421'
    >>> base16_encode(b'')
    ''
    """
    # 将数据转换为整数列表（每个整数表示一个字节），再将每个字节转换为大写的
    # 十六进制表示，最后拼接并返回结果。
    return "".join([hex(byte)[2:].zfill(2).upper() for byte in list(data)])


def base16_decode(data: str) -> bytes:
    """
    将给定的 Base16 编码数据解码为字节。

    >>> base16_decode('48656C6C6F20576F726C6421')
    b'Hello World!'
    >>> base16_decode('48454C4C4F20574F524C4421')
    b'HELLO WORLD!'
    >>> base16_decode('')
    b''
    >>> base16_decode('486')
    Traceback (most recent call last):
      ...
    ValueError: Base16 encoded data is invalid:
    Data does not have an even number of hex digits.
    >>> base16_decode('48656c6c6f20576f726c6421')
    Traceback (most recent call last):
      ...
    ValueError: Base16 encoded data is invalid:
    Data is not uppercase hex or it contains invalid characters.
    >>> base16_decode('This is not base64 encoded data.')
    Traceback (most recent call last):
      ...
    ValueError: Base16 encoded data is invalid:
    Data is not uppercase hex or it contains invalid characters.
    """
    # 按照 RFC3548 检查数据有效性
    # https://www.ietf.org/rfc/rfc3548.txt
    if (len(data) % 2) != 0:
        raise ValueError(
            """Base16 encoded data is invalid:
Data does not have an even number of hex digits."""
        )
    # 检查字符集——按照 RFC3548 第 6 节，标准 Base16 字母表使用大写字符
    if not set(data) <= set("0123456789ABCDEF"):
        raise ValueError(
            """Base16 encoded data is invalid:
Data is not uppercase hex or it contains invalid characters."""
        )
    # 每两个十六进制数字（一个字节）转换为整数，再将结果组成字节并返回
    return bytes(int(data[i] + data[i + 1], 16) for i in range(0, len(data), 2))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
