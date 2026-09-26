"""
XTEA（eXtended Tiny Encryption Algorithm）是一种用于改进 TEA 弱点的分组密码，
由 David Wheeler 和 Roger Needham 于 1997 年发表。XTEA 使用 128 位密钥处理
64 位分组，并采用建议执行 64 轮的 Feistel 网络。

由于实现简单且代码占用空间小，它仍用于嵌入式系统和游戏网络协议。

参考资料：https://en.wikipedia.org/wiki/XTEA
"""

import struct

DELTA = 0x9E3779B9
MASK = 0xFFFFFFFF


def xtea_encrypt(block: bytes, key: bytes, num_rounds: int = 64) -> bytes:
    """
    使用 XTEA 加密单个 64 位分组。

    :param block: 8 字节明文
    :param key: 16 字节（128 位密钥）
    :param num_rounds: Feistel 轮数（默认 64）
    :return: 8 字节密文

    >>> key = b'\\x00' * 16
    >>> plaintext = b'\\x00' * 8
    >>> ciphertext = xtea_encrypt(plaintext, key)
    >>> ciphertext.hex()
    'fc924d124ad0ed50'

    >>> xtea_encrypt(b'hello!!!', b'sixteenbyteskey!')
    b'u\\x8d\\x00\\x17c\\xb8\\xf0*'

    >>> xtea_encrypt(b'short', key)
    Traceback (most recent call last):
        ...
    ValueError: block must be 8 bytes

    >>> xtea_encrypt(plaintext, b'short')
    Traceback (most recent call last):
        ...
    ValueError: key must be 16 bytes
    """
    if len(block) != 8:
        raise ValueError("block must be 8 bytes")
    if len(key) != 16:
        raise ValueError("key must be 16 bytes")

    v0, v1 = struct.unpack("!II", block)
    k = struct.unpack("!4I", key)

    total = 0
    for _ in range(num_rounds):
        v0 = (v0 + ((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (total + k[total & 3]))) & MASK
        total = (total + DELTA) & MASK
        v1 = (
            v1 + ((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (total + k[(total >> 11) & 3]))
        ) & MASK

    return struct.pack("!II", v0, v1)


def xtea_decrypt(block: bytes, key: bytes, num_rounds: int = 64) -> bytes:
    """
    使用 XTEA 解密单个 64 位分组。

    :param block: 8 字节密文
    :param key: 16 字节（128 位密钥）
    :param num_rounds: Feistel 轮数（默认 64）
    :return: 8 字节明文

    往返测试——加密后再解密应返回原始明文：
    >>> key = b'\\x00' * 16
    >>> plaintext = b'\\x00' * 8
    >>> xtea_decrypt(xtea_encrypt(plaintext, key), key) == plaintext
    True

    >>> msg = b'hello!!!'
    >>> k = b'sixteenbyteskey!'
    >>> xtea_decrypt(xtea_encrypt(msg, k), k) == msg
    True

    >>> xtea_decrypt(b'short', key)
    Traceback (most recent call last):
        ...
    ValueError: block must be 8 bytes

    >>> xtea_decrypt(b'\\x00' * 8, b'short')
    Traceback (most recent call last):
        ...
    ValueError: key must be 16 bytes
    """
    if len(block) != 8:
        raise ValueError("block must be 8 bytes")
    if len(key) != 16:
        raise ValueError("key must be 16 bytes")

    v0, v1 = struct.unpack("!II", block)
    k = struct.unpack("!4I", key)

    total = (DELTA * num_rounds) & MASK
    for _ in range(num_rounds):
        v1 = (
            v1 - ((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (total + k[(total >> 11) & 3]))
        ) & MASK
        total = (total - DELTA) & MASK
        v0 = (v0 - ((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (total + k[total & 3]))) & MASK

    return struct.pack("!II", v0, v1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
