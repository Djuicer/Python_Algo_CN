"""
MD5 算法是一种哈希函数，常用作校验和来检测数据损坏。该算法将给定消息分成
512 位的块进行处理，并按需填充消息。它使用这些块操作一个 128 位状态，共执行
64 次此类操作。请注意，所有值均采用小端序，因此会按需转换输入。

尽管 MD5 过去曾用作密码学哈希函数，但它已经被攻破，因此不应再用于安全用途。

更多信息请参阅 https://en.wikipedia.org/wiki/MD5
"""

from collections.abc import Generator
from math import sin


def to_little_endian(string_32: bytes) -> bytes:
    """
    以每 8 个字符为一组，将给定字符串转换为小端序。

    参数：
        string_32 {[string]} -- [32 字符字符串]

    异常：
        ValueError -- [输入不是 32 个字符]

    返回：
        32 字符的小端序字符串
    >>> to_little_endian(b'1234567890abcdfghijklmnopqrstuvw')
    b'pqrstuvwhijklmno90abcdfg12345678'
    >>> to_little_endian(b'1234567890')
    Traceback (most recent call last):
    ...
    ValueError: Input must be of length 32
    """
    if len(string_32) != 32:
        raise ValueError("Input must be of length 32")

    little_endian = b""
    for i in [3, 2, 1, 0]:
        little_endian += string_32[8 * i : 8 * i + 8]
    return little_endian


def reformat_hex(i: int) -> bytes:
    """
    将给定的非负整数转换为十六进制字符串。

    示例：假设输入如下：
        i = 1234

        输入的十六进制形式为 0x000004d2，因此小端序十六进制字符串为
        "d2040000"。

    参数：
        i {[int]} -- [整数]

    异常：
        ValueError -- [输入为负数]

    返回：
        8 字符的小端序十六进制字符串

    >>> reformat_hex(1234)
    b'd2040000'
    >>> reformat_hex(666)
    b'9a020000'
    >>> reformat_hex(0)
    b'00000000'
    >>> reformat_hex(1234567890)
    b'd2029649'
    >>> reformat_hex(1234567890987654321)
    b'b11c6cb1'
    >>> reformat_hex(-1)
    Traceback (most recent call last):
    ...
    ValueError: Input must be non-negative
    """
    if i < 0:
        raise ValueError("Input must be non-negative")

    hex_rep = format(i, "08x")[-8:]
    little_endian_hex = b""
    for j in [3, 2, 1, 0]:
        little_endian_hex += hex_rep[2 * j : 2 * j + 2].encode("utf-8")
    return little_endian_hex


def preprocess(message: bytes) -> bytes:
    """
    对消息字符串进行预处理：
    - 将消息转换为比特字符串
    - 将比特字符串填充到字符数为 512 的倍数：
        - 追加一个 1
        - 追加若干个 0，直至 length = 448 (mod 512)
        - 追加原始消息的长度（64 个字符）

    示例：假设输入如下：
        message = "a"

        消息的比特字符串为 "01100001"，长度为 8 位。因此，需要填充 439 位，
        使得
        (bit_string + "1" + padding) = 448 (mod 512).
        消息长度以 64 位小端序二进制表示为 "000010000...0"。
        合并后的比特字符串长度为 512 位。

    参数：
        message {[string]} -- [消息字符串]

    返回：
        已处理并填充到字符数为 512 倍数的比特字符串

    >>> preprocess(b"a") == (b"01100001" + b"1" +
    ...                     (b"0" * 439) + b"00001000" + (b"0" * 56))
    True
    >>> preprocess(b"") == b"1" + (b"0" * 447) + (b"0" * 64)
    True
    """
    bit_string = b""
    for char in message:
        bit_string += format(char, "08b").encode("utf-8")
    start_len = format(len(bit_string), "064b").encode("utf-8")

    # 将 bit_string 填充到字符数为 512 的倍数
    bit_string += b"1"
    while len(bit_string) % 512 != 448:
        bit_string += b"0"
    bit_string += to_little_endian(start_len[32:]) + to_little_endian(start_len[:32])

    return bit_string


def get_block_words(bit_string: bytes) -> Generator[list[int]]:
    """
    将比特字符串分成 512 字符的块，并以 32 位字列表的形式逐块生成。

    示例：假设输入如下：
        bit_string =
            "000000000...0" +  # 0x00 (32 bits, padded to the right)
            "000000010...0" +  # 0x01 (32 bits, padded to the right)
            "000000100...0" +  # 0x02 (32 bits, padded to the right)
            "000000110...0" +  # 0x03 (32 bits, padded to the right)
            ...
            "000011110...0"    # 0x0a (32 bits, padded to the right)

        此时 len(bit_string) == 512，因此只有 1 个块。该块被分成若干 32 位字，
        每个字都转换为小端序。第一个字解释为十进制的 0，第二个字解释为
        十进制的 1，依此类推。

        因此，block_words == [[0, 1, 2, 3, ..., 15]]。

    参数：
        bit_string {[string]} -- [长度为 512 倍数的比特字符串]

    异常：
        ValueError -- [比特字符串长度不是 512 的倍数]

    生成：
        包含 16 个 32 位字的列表

    >>> test_string = ("".join(format(n << 24, "032b") for n in range(16))
    ...                  .encode("utf-8"))
    >>> list(get_block_words(test_string))
    [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]
    >>> list(get_block_words(test_string * 4)) == [list(range(16))] * 4
    True
    >>> list(get_block_words(b"1" * 512)) == [[4294967295] * 16]
    True
    >>> list(get_block_words(b""))
    []
    >>> list(get_block_words(b"1111"))
    Traceback (most recent call last):
    ...
    ValueError: Input must have length that's a multiple of 512
    """
    if len(bit_string) % 512 != 0:
        raise ValueError("Input must have length that's a multiple of 512")

    for pos in range(0, len(bit_string), 512):
        block = bit_string[pos : pos + 512]
        block_words = []
        for i in range(0, 512, 32):
            block_words.append(int(to_little_endian(block[i : i + 32]), 2))
        yield block_words


def not_32(i: int) -> int:
    """
    对给定整数执行按位取反。

    参数：
        i {[int]} -- [给定整数]

    异常：
        ValueError -- [输入为负数]

    返回：
        对 i 按位取反的结果

    >>> not_32(34)
    4294967261
    >>> not_32(1234)
    4294966061
    >>> not_32(4294966061)
    1234
    >>> not_32(0)
    4294967295
    >>> not_32(1)
    4294967294
    >>> not_32(-1)
    Traceback (most recent call last):
    ...
    ValueError: Input must be non-negative
    """
    if i < 0:
        raise ValueError("Input must be non-negative")

    i_str = format(i, "032b")
    new_str = ""
    for c in i_str:
        new_str += "1" if c == "0" else "0"
    return int(new_str, 2)


def sum_32(a: int, b: int) -> int:
    """
    将两个数作为 32 位整数相加。

    参数：
        a {[int]} -- [第一个给定整数]
        b {[int]} -- [第二个给定整数]

    返回：
        以无符号 32 位整数表示的 (a + b)

    >>> sum_32(1, 1)
    2
    >>> sum_32(2, 3)
    5
    >>> sum_32(0, 0)
    0
    >>> sum_32(-1, -1)
    4294967294
    >>> sum_32(4294967295, 1)
    0
    """
    return (a + b) % 2**32


def left_rotate_32(i: int, shift: int) -> int:
    """
    将给定整数的比特向左循环移位指定次数。

    参数：
        i {[int]} -- [给定整数]
        shift {[int]} -- [移位次数]

    异常：
        ValueError -- [给定整数或 shift 为负数]

    返回：
        将 `i` 向左循环移动 `shift` 位后的结果

    >>> left_rotate_32(1234, 1)
    2468
    >>> left_rotate_32(1111, 4)
    17776
    >>> left_rotate_32(2147483648, 1)
    1
    >>> left_rotate_32(2147483648, 3)
    4
    >>> left_rotate_32(4294967295, 4)
    4294967295
    >>> left_rotate_32(1234, 0)
    1234
    >>> left_rotate_32(0, 0)
    0
    >>> left_rotate_32(-1, 0)
    Traceback (most recent call last):
    ...
    ValueError: Input must be non-negative
    >>> left_rotate_32(0, -1)
    Traceback (most recent call last):
    ...
    ValueError: Shift must be non-negative
    """
    if i < 0:
        raise ValueError("Input must be non-negative")
    if shift < 0:
        raise ValueError("Shift must be non-negative")
    return ((i << shift) ^ (i >> (32 - shift))) % 2**32


def md5_me(message: bytes) -> bytes:
    """
    返回给定消息的 32 字符 MD5 哈希值。

    参考资料：https://en.wikipedia.org/wiki/MD5#Algorithm

    参数：
        message {[string]} -- [消息]

    返回：
        32 字符的 MD5 哈希字符串

    >>> md5_me(b"")
    b'd41d8cd98f00b204e9800998ecf8427e'
    >>> md5_me(b"The quick brown fox jumps over the lazy dog")
    b'9e107d9d372bb6826bd81d3542a419d6'
    >>> md5_me(b"The quick brown fox jumps over the lazy dog.")
    b'e4d909c290d0fb1ca068ffaddf22cbd0'

    >>> import hashlib
    >>> from string import ascii_letters
    >>> msgs = [b"", ascii_letters.encode("utf-8"), "Üñîçø∂é".encode("utf-8"),
    ...         b"The quick brown fox jumps over the lazy dog."]
    >>> all(md5_me(msg) == hashlib.md5(msg).hexdigest().encode("utf-8") for msg in msgs)
    True
    """

    # 转换为比特字符串、添加填充并追加消息长度
    bit_string = preprocess(message)

    added_consts = [int(2**32 * abs(sin(i + 1))) for i in range(64)]

    # 初始状态
    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476

    shift_amounts = [
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
    ]

    # 分块处理比特字符串，每块包含 16 个 32 位字
    for block_words in get_block_words(bit_string):
        a = a0
        b = b0
        c = c0
        d = d0

        # 对当前块进行哈希处理
        for i in range(64):
            if i <= 15:
                # f = (b & c) | (not_32(b) & d)     # f 的另一种定义
                f = d ^ (b & (c ^ d))
                g = i
            elif i <= 31:
                # f = (d & b) | (not_32(d) & c)     # f 的另一种定义
                f = c ^ (d & (b ^ c))
                g = (5 * i + 1) % 16
            elif i <= 47:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | not_32(d))
                g = (7 * i) % 16
            f = (f + a + added_consts[i] + block_words[g]) % 2**32
            a = d
            d = c
            c = b
            b = sum_32(b, left_rotate_32(f, shift_amounts[i]))

        # 将当前块的哈希结果加入累计值
        a0 = sum_32(a0, a)
        b0 = sum_32(b0, b)
        c0 = sum_32(c0, c)
        d0 = sum_32(d0, d)

    digest = reformat_hex(a0) + reformat_hex(b0) + reformat_hex(c0) + reformat_hex(d0)
    return digest


if __name__ == "__main__":
    import doctest

    doctest.testmod()
