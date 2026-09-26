B64_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def base64_encode(data: bytes) -> bytes:
    """按照 RFC4648 编码数据。

    首先将数据转换为二进制，并追加二进制数字，使长度成为 6 的倍数；随后每 6 个
    二进制数字对应 B64_CHARSET 字符串中的一个字符。追加的二进制数字数量决定
    后续要添加多少个作为填充的 "=" 符号。每追加 2 个二进制数字，输出中就添加
    一个 "=" 符号。可以追加任意二进制数字使长度成为 6 的倍数，例如：
    "AA" -> 0010100100101001 -> 001010 010010 1001
    如上所示，需要再添加 2 个二进制数字，因此有四种可能：00、01、10 或 11。
    因此，可以在隐写术中利用 Base64 编码，将数据隐藏在这些追加数字中。

    >>> from base64 import b64encode
    >>> a = b"This pull request is part of Hacktoberfest20!"
    >>> b = b"https://tools.ietf.org/html/rfc4648"
    >>> c = b"A"
    >>> base64_encode(a) == b64encode(a)
    True
    >>> base64_encode(b) == b64encode(b)
    True
    >>> base64_encode(c) == b64encode(c)
    True
    >>> base64_encode("abc")
    Traceback (most recent call last):
      ...
    TypeError: a bytes-like object is required, not 'str'
    """
    # 确保给定数据是字节类对象
    if not isinstance(data, bytes):
        msg = f"a bytes-like object is required, not '{data.__class__.__name__}'"
        raise TypeError(msg)

    binary_stream = "".join(bin(byte)[2:].zfill(8) for byte in data)

    padding_needed = len(binary_stream) % 6 != 0

    if padding_needed:
        # 稍后添加的填充
        padding = b"=" * ((6 - len(binary_stream) % 6) // 2)

        # 向 binary_stream 追加任意二进制数字（默认为 0），使其长度成为 6 的倍数
        binary_stream += "0" * (6 - len(binary_stream) % 6)
    else:
        padding = b""

    # 将每 6 个二进制数字编码为对应的 Base64 字符
    return (
        "".join(
            B64_CHARSET[int(binary_stream[index : index + 6], 2)]
            for index in range(0, len(binary_stream), 6)
        ).encode()
        + padding
    )


def base64_decode(encoded_data: str) -> bytes:
    """按照 RFC4648 解码数据。

    此函数执行 base64_encode 的逆操作。首先将编码数据转换回二进制流，再根据
    填充移除先前追加的二进制数字。此时二进制流的长度是 8 的倍数，最后将每
    8 位转换为一个字节。

    >>> from base64 import b64decode
    >>> a = "VGhpcyBwdWxsIHJlcXVlc3QgaXMgcGFydCBvZiBIYWNrdG9iZXJmZXN0MjAh"
    >>> b = "aHR0cHM6Ly90b29scy5pZXRmLm9yZy9odG1sL3JmYzQ2NDg="
    >>> c = "QQ=="
    >>> base64_decode(a) == b64decode(a)
    True
    >>> base64_decode(b) == b64decode(b)
    True
    >>> base64_decode(c) == b64decode(c)
    True
    >>> base64_decode("abc")
    Traceback (most recent call last):
      ...
    AssertionError: Incorrect padding
    """
    # 确保 encoded_data 是字符串或字节类对象
    if not isinstance(encoded_data, bytes) and not isinstance(encoded_data, str):
        msg = (
            "argument should be a bytes-like object or ASCII string, "
            f"not '{encoded_data.__class__.__name__}'"
        )
        raise TypeError(msg)

    # 如果 encoded_data 是字节类对象，确保它只包含 ASCII 字符，再转换为字符串对象
    if isinstance(encoded_data, bytes):
        try:
            encoded_data = encoded_data.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("base64 encoded data should only contain ASCII characters")

    padding = encoded_data.count("=")

    # 检查编码字符串是否包含非 Base64 字符
    if padding:
        assert all(char in B64_CHARSET for char in encoded_data[:-padding]), (
            "Invalid base64 character(s) found."
        )
    else:
        assert all(char in B64_CHARSET for char in encoded_data), (
            "Invalid base64 character(s) found."
        )

    # 检查填充
    assert len(encoded_data) % 4 == 0 and padding < 3, "Incorrect padding"

    if padding:
        # 如果存在填充，则将其移除
        encoded_data = encoded_data[:-padding]

        binary_stream = "".join(
            bin(B64_CHARSET.index(char))[2:].zfill(6) for char in encoded_data
        )[: -padding * 2]
    else:
        binary_stream = "".join(
            bin(B64_CHARSET.index(char))[2:].zfill(6) for char in encoded_data
        )

    data = [
        int(binary_stream[index : index + 8], 2)
        for index in range(0, len(binary_stream), 8)
    ]

    return bytes(data)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
