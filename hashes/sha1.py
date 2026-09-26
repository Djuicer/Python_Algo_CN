"""
实现 SHA1 哈希函数，并提供计算字符串或文件文本哈希值的工具。本模块还包含一个
Test 类，用于验证生成的哈希值是否与 hashlib 库的返回值一致。

用法：python sha1.py --string "Hello World!!"
       python sha1.py --file "hello_world.txt"
       不带任何参数运行时，会输出字符串 "Hello World!! Welcome to Cryptography"
       的哈希值。

字符串的 SHA1 哈希（或 SHA1 和）是一种密码学函数，正向计算容易，反向计算却
极其困难。也就是说，可以轻松计算字符串的哈希值，但仅凭哈希值很难获知原始
字符串。这一性质可用于安全通信和发送加密消息，在支付系统、区块链和加密货币
等领域也非常有用。

参考资料所述算法如下：
首先从一条消息开始，对消息进行填充，并在末尾添加消息长度。然后将其分成
512 位（即 64 字节）的块，再逐块处理。每个块都必须经过扩展和压缩。
每次压缩后的值会累加到一个称为“当前哈希状态”的 160 位缓冲区中。
处理完最后一个块后，返回当前哈希状态作为最终哈希值。

参考资料：https://deadhacker.com/2006/02/21/sha-1-illustrated/
"""

import argparse
import hashlib  # hashlib 仅在 Test 类中使用
import struct


class SHA1Hash:
    """
    封装 SHA1 哈希算法完整处理流程的类。
    >>> SHA1Hash(bytes('Allan', 'utf-8')).final_hash()
    '872af2d8ac3d8695387e7c804bf0e02c18df9e6e'
    """

    def __init__(self, data) -> None:
        """
        初始化变量 data 和 h。h 是由 5 个八位十六进制数组成的列表，依次对应
        (1732584193, 4023233417, 2562383102, 271733878, 3285377520)
        以此作为初始消息摘要。在 Python 中，十六进制数以 0x 开头。
        """
        self.data = data
        self.h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    @staticmethod
    def rotate(n, b):
        """
        供其他方法调用的静态方法，将 n 向左循环移动 b 位。
        >>> SHA1Hash('').rotate(12,2)
        48
        """
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def padding(self):
        """
        用零填充输入消息，使 padded_data 的长度为 64 字节或 512 位。
        """
        padding = b"\x80" + b"\x00" * (63 - (len(self.data) + 8) % 64)
        padded_data = self.data + padding + struct.pack(">Q", 8 * len(self.data))
        return padded_data

    def split_blocks(self):
        """
        返回一个字节串列表，其中每个字节串的长度均为 64。
        """
        return [
            self.padded_data[i : i + 64] for i in range(0, len(self.padded_data), 64)
        ]

    # @staticmethod
    def expand_block(self, block):
        """
        接收一个长度为 64 的字节串块，将其解包为整数列表，并经过若干位运算后
        返回包含 80 个整数的列表。
        """
        w = list(struct.unpack(">16L", block)) + [0] * 64
        for i in range(16, 80):
            w[i] = self.rotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1)
        return w

    def final_hash(self):
        """
        调用其他所有方法处理输入。先填充数据并分块，再对每个块执行一系列操作
        （包括扩展）。
        对每个块，将已初始化的变量 h 复制到 a、b、c、d、e，这 5 个变量随后
        经历多次变化。处理完所有块后，将这 5 个变量与 h 对应相加，即 a 加到
        h[0]、b 加到 h[1]，依此类推。此时的 h 即为最终返回的哈希值。
        """
        self.padded_data = self.padding()
        self.blocks = self.split_blocks()
        for block in self.blocks:
            expanded_block = self.expand_block(block)
            a, b, c, d, e = self.h
            for i in range(80):
                if 0 <= i < 20:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= i < 40:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= i < 60:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                elif 60 <= i < 80:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6
                a, b, c, d, e = (
                    self.rotate(a, 5) + f + e + k + expanded_block[i] & 0xFFFFFFFF,
                    a,
                    self.rotate(b, 30),
                    c,
                    d,
                )
            self.h = (
                self.h[0] + a & 0xFFFFFFFF,
                self.h[1] + b & 0xFFFFFFFF,
                self.h[2] + c & 0xFFFFFFFF,
                self.h[3] + d & 0xFFFFFFFF,
                self.h[4] + e & 0xFFFFFFFF,
            )
        return ("{:08x}" * 5).format(*self.h)


def test_sha1_hash() -> None:
    msg = b"Test String"
    assert SHA1Hash(msg).final_hash() == hashlib.sha1(msg).hexdigest()  # noqa: S324


def main() -> None:
    """
    提供 'string' 或 'file' 选项来接收输入，并输出计算得到的 SHA1 哈希值。
    unittest.main() 已被注释掉，因为通常不需要每次都运行测试。
    """
    # unittest.main()
    parser = argparse.ArgumentParser(description="Process some strings or files")
    parser.add_argument(
        "--string",
        dest="input_string",
        default="Hello World!! Welcome to Cryptography",
        help="Hash the string",
    )
    parser.add_argument("--file", dest="input_file", help="Hash contents of a file")
    args = parser.parse_args()
    input_string = args.input_string
    # 无论哪种情况，哈希输入都应为字节串
    if args.input_file:
        with open(args.input_file, "rb") as f:
            hash_input = f.read()
    else:
        hash_input = bytes(input_string, "utf-8")
    print(SHA1Hash(hash_input).final_hash())


if __name__ == "__main__":
    main()
    import doctest

    doctest.testmod()
