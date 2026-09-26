"""
字节序（Endianness）转换算法

本模块实现字节序转换工具，用于在多字节整数的大端表示与小端表示之间转换。

字节序是指多字节数据类型中各字节的排列顺序：
- 大端序（Big-endian）：最高有效字节在前（例如 0x12345678 → [0x12, 0x34, 0x56, 0x78]）
- 小端序（Little-endian）：最低有效字节在前
  （例如 0x12345678 → [0x78, 0x56, 0x34, 0x12]）

常见用途：
- 网络协议（TCP/IP 的多字节字段使用大端序）
- 文件格式解析（PNG、JPEG 文件头会指定字节序）
- 密码算法（MD5 使用小端序，SHA-256 使用大端序）
- 二进制数据序列化（Protocol Buffers、MessagePack）
- 硬件接口（ARM 支持双字节序，x86 严格使用小端序）
- 跨平台数据交换

实际示例：
- IP 地址以大端序（网络字节序）传输
- 现代 ARM 和 x86 处理器通常以小端模式运行
- Java 类文件使用大端格式
- Bitcoin 的区块哈希使用小端序
- USB 和 PCI 协议使用小端序

参考资料：
- https://en.wikipedia.org/wiki/Endianness
- RFC 1700 (Network Byte Order)
- https://tools.ietf.org/html/rfc1700
"""


def swap_endianness_16(value: int) -> int:
    """
    交换 16 位整数的字节顺序。

    参数：
        value：16 位整数（0 到 65,535）

    返回：
        字节顺序交换后的整数

    异常：
        ValueError：当 value 为负数或超出 16 位范围时

    >>> swap_endianness_16(0x1234)
    13330

    >>> hex(swap_endianness_16(0x1234))
    '0x3412'

    >>> swap_endianness_16(0xABCD)
    52651

    >>> hex(swap_endianness_16(0xABCD))
    '0xcdab'

    >>> swap_endianness_16(0)
    0

    >>> swap_endianness_16(0xFFFF)
    65535
    """
    if value < 0 or value > 0xFFFF:
        msg = f"value must be between 0 and {0xFFFF}"
        raise ValueError(msg)

    return ((value & 0xFF) << 8) | ((value & 0xFF00) >> 8)


def swap_endianness_32(value: int) -> int:
    """
    交换 32 位整数的字节顺序。

    参数：
        value：32 位整数（0 到 4,294,967,295）

    返回：
        字节顺序交换后的整数

    异常：
        ValueError：当 value 为负数或超出 32 位范围时

    >>> swap_endianness_32(0x12345678)
    2018915346

    >>> hex(swap_endianness_32(0x12345678))
    '0x78563412'

    >>> swap_endianness_32(0xDEADBEEF)
    4022250974

    >>> hex(swap_endianness_32(0xDEADBEEF))
    '0xefbeadde'

    >>> swap_endianness_32(0)
    0

    >>> swap_endianness_32(0xFFFFFFFF)
    4294967295

    >>> swap_endianness_32(0x01020304)
    67305985
    """
    if value < 0 or value > 0xFFFFFFFF:
        msg = f"value must be between 0 and {0xFFFFFFFF}"
        raise ValueError(msg)

    return (
        ((value & 0x000000FF) << 24)
        | ((value & 0x0000FF00) << 8)
        | ((value & 0x00FF0000) >> 8)
        | ((value & 0xFF000000) >> 24)
    )


def swap_endianness_64(value: int) -> int:
    """
    交换 64 位整数的字节顺序。

    参数：
        value：64 位整数（0 到 18,446,744,073,709,551,615）

    返回：
        字节顺序交换后的整数

    异常：
        ValueError：当 value 为负数或超出 64 位范围时

    >>> swap_endianness_64(0x0123456789ABCDEF)
    17279655951921914625

    >>> hex(swap_endianness_64(0x0123456789ABCDEF))
    '0xefcdab8967452301'

    >>> swap_endianness_64(0xFEDCBA9876543210)
    1167088121787636990

    >>> hex(swap_endianness_64(0xFEDCBA9876543210))
    '0x1032547698badcfe'

    >>> swap_endianness_64(0)
    0

    >>> swap_endianness_64(0xFFFFFFFFFFFFFFFF)
    18446744073709551615
    """
    if value < 0 or value > 0xFFFFFFFFFFFFFFFF:
        msg = f"value must be between 0 and {0xFFFFFFFFFFFFFFFF}"
        raise ValueError(msg)

    return (
        ((value & 0x00000000000000FF) << 56)
        | ((value & 0x000000000000FF00) << 40)
        | ((value & 0x0000000000FF0000) << 24)
        | ((value & 0x00000000FF000000) << 8)
        | ((value & 0x000000FF00000000) >> 8)
        | ((value & 0x0000FF0000000000) >> 24)
        | ((value & 0x00FF000000000000) >> 40)
        | ((value & 0xFF00000000000000) >> 56)
    )


def bytes_to_int_little(data: bytes) -> int:
    """
    使用小端字节序将字节转换为整数。

    参数：
        data：要转换的字节序列（1 至 8 字节）

    返回：
        按小端序解释所得的整数

    异常：
        TypeError：当 data 不是 bytes 时
        ValueError：当 data 为空或超过 8 字节时

    >>> bytes_to_int_little(b'\\x78\\x56\\x34\\x12')
    305419896

    >>> hex(bytes_to_int_little(b'\\x78\\x56\\x34\\x12'))
    '0x12345678'

    >>> bytes_to_int_little(b'\\x01\\x02')
    513

    >>> bytes_to_int_little(b'\\xff')
    255

    >>> bytes_to_int_little(b'\\x00\\x00\\x00\\x01')
    16777216
    """
    if not data or len(data) > 8:
        msg = "data must be between 1 and 8 bytes"
        raise ValueError(msg)

    return int.from_bytes(data, byteorder="little")


def bytes_to_int_big(data: bytes) -> int:
    """
    使用大端字节序将字节转换为整数。

    参数：
        data：要转换的字节序列（1 至 8 字节）

    返回：
        按大端序解释所得的整数

    异常：
        TypeError：当 data 不是 bytes 时
        ValueError：当 data 为空或超过 8 字节时

    >>> bytes_to_int_big(b'\\x12\\x34\\x56\\x78')
    305419896

    >>> hex(bytes_to_int_big(b'\\x12\\x34\\x56\\x78'))
    '0x12345678'

    >>> bytes_to_int_big(b'\\x01\\x02')
    258

    >>> bytes_to_int_big(b'\\xff')
    255

    >>> bytes_to_int_big(b'\\x00\\x00\\x00\\x01')
    1
    """
    if not data or len(data) > 8:
        msg = "data must be between 1 and 8 bytes"
        raise ValueError(msg)

    return int.from_bytes(data, byteorder="big")


def int_to_bytes_little(value: int, num_bytes: int) -> bytes:
    """
    使用小端字节序将整数转换为字节。

    参数：
        value：要转换的非负整数
        num_bytes：输出的字节数（1 至 8）

    返回：
        小端序的字节表示

    异常：
        ValueError：当 value 为负数、num_bytes 无效或 value 过大时

    >>> int_to_bytes_little(0x12345678, 4)
    b'xV4\\x12'

    >>> int_to_bytes_little(513, 2)
    b'\\x01\\x02'

    >>> int_to_bytes_little(255, 1)
    b'\\xff'

    >>> int_to_bytes_little(16777216, 4)
    b'\\x00\\x00\\x00\\x01'
    """
    if value < 0:
        msg = "value must be non-negative"
        raise ValueError(msg)

    if num_bytes < 1 or num_bytes > 8:
        msg = "num_bytes must be between 1 and 8"
        raise ValueError(msg)

    if value >= (1 << (num_bytes * 8)):
        msg = f"value {value} too large for {num_bytes} bytes"
        raise ValueError(msg)

    return value.to_bytes(num_bytes, byteorder="little")


def int_to_bytes_big(value: int, num_bytes: int) -> bytes:
    """
    使用大端字节序将整数转换为字节。

    参数：
        value：要转换的非负整数
        num_bytes：输出的字节数（1 至 8）

    返回：
        大端序的字节表示

    异常：
        ValueError：当 value 为负数、num_bytes 无效或 value 过大时

    >>> int_to_bytes_big(0x12345678, 4)
    b'\\x124Vx'

    >>> int_to_bytes_big(258, 2)
    b'\\x01\\x02'

    >>> int_to_bytes_big(255, 1)
    b'\\xff'

    >>> int_to_bytes_big(1, 4)
    b'\\x00\\x00\\x00\\x01'
    """
    if value < 0:
        msg = "value must be non-negative"
        raise ValueError(msg)

    if num_bytes < 1 or num_bytes > 8:
        msg = "num_bytes must be between 1 and 8"
        raise ValueError(msg)

    if value >= (1 << (num_bytes * 8)):
        msg = f"value {value} too large for {num_bytes} bytes"
        raise ValueError(msg)

    return value.to_bytes(num_bytes, byteorder="big")


if __name__ == "__main__":
    import doctest

    _ = doctest.testmod()

    print("Endianness Conversion Examples:")
    print(f"16-bit: 0x1234 → {hex(swap_endianness_16(0x1234))}")
    print(f"32-bit: 0x12345678 → {hex(swap_endianness_32(0x12345678))}")
    print(f"64-bit: 0x0123456789ABCDEF → {hex(swap_endianness_64(0x0123456789ABCDEF))}")
    print(f"Bytes to int (little): {bytes_to_int_little(b'\x78\x56\x34\x12'):#x}")
    print(f"Bytes to int (big): {bytes_to_int_big(b'\x12\x34\x56\x78'):#x}")
