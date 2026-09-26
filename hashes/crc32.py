"""
CRC32（32 位循环冗余校验）哈希算法

本模块实现 CRC32 哈希算法。这是一种非密码学哈希函数，广泛用于错误检测和
数据完整性验证。

CRC32 常用于：
- ZIP 文件格式中的数据完整性校验
- 以太网帧校验序列
- PNG 图像格式中的数据块校验
- Gzip 压缩

该算法使用 IEEE 802.3 多项式（按反向位序表示为 0xEDB88320），并生成一个
32 位哈希值。

注意：CRC32 不适用于密码学用途。它用于错误检测，而非安全防护。
如需密码学哈希，请使用 SHA-256 或类似算法。

参考资料：
- https://en.wikipedia.org/wiki/Cyclic_redundancy_check
- https://www.rfc-editor.org/rfc/rfc1952.html（GZIP 规范）
"""


def _generate_crc32_table() -> list[int]:
    """
    生成用于优化计算的 CRC32 查找表。

    使用 IEEE 802.3 多项式：0xEDB88320（反向位序）。

    >>> table = _generate_crc32_table()
    >>> len(table)
    256
    >>> hex(table[0])
    '0x0'
    >>> hex(table[128])
    '0xedb88320'
    """
    polynomial = 0xEDB88320
    table = []

    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1
        table.append(crc)

    return table


CRC32_TABLE = _generate_crc32_table()


def crc32(data: bytes) -> int:
    """
    计算字节数据的 CRC32 哈希值。

    参数：
        data: 要计算哈希值的字节数据

    返回：
        以 32 位整数表示的 CRC32 哈希值（0 到 4294967295）

    异常：
        TypeError: data 不是 bytes 类型时抛出

    >>> crc32(b"Hello World")
    1243066710

    >>> crc32(b"")
    0

    >>> crc32(b"The quick brown fox jumps over the lazy dog")
    1095738169

    >>> crc32(b"a")
    3904355907

    >>> crc32(b"abc")
    891568578

    >>> crc32(b"123456789")
    3421780262

    >>> crc32(b"Python")
    2742599054

    >>> crc32(b"Algorithms")
    3866870335

    >>> crc32(b"CRC32")
    4128576900

    >>> crc32(b"\\x00\\x00\\x00\\x00")
    558161692

    >>> import zlib
    >>> test_data = b"Verify with zlib"
    >>> crc32(test_data) == zlib.crc32(test_data)
    True
    """
    if not isinstance(data, bytes):
        msg = f"data must be bytes, not {type(data).__name__}"
        raise TypeError(msg)

    crc = 0xFFFFFFFF

    for byte in data:
        table_index = (crc ^ byte) & 0xFF
        crc = (crc >> 8) ^ CRC32_TABLE[table_index]

    return crc ^ 0xFFFFFFFF


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print(f"CRC32 of 'Hello World': {crc32(b'Hello World')}")
    print(f"CRC32 of empty bytes: {crc32(b'')}")
