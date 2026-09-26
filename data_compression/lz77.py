"""
LZ77 压缩算法
- Abraham Lempel 和 Jacob Ziv 于 1977 年在论文中发表的无损数据压缩算法
- 也称为 LZ1 或滑动窗口压缩
- 是 LZW、LZSS、LZMA 等多种变体的基础

它使用“滑动窗口”方法。滑动窗口包含：
  - 搜索缓冲区
  - 先行缓冲区
len(sliding_window) = len(search_buffer) + len(look_ahead_buffer)

LZ77 维护一个使用三元组的字典，三元组由以下部分组成：
    - 搜索缓冲区中的偏移量，即短语起点与文件开头之间的距离。
    - 匹配长度，即构成短语的字符数。
    - 指示符，即下一个要编码的字符。

解析文件时，字典会动态更新，以反映压缩数据的内容和大小。

示例：
"cabracadabrarrarrad" <-> [(0, 0, 'c'), (0, 0, 'a'), (0, 0, 'b'), (0, 0, 'r'),
                           (3, 1, 'c'), (2, 1, 'd'), (7, 4, 'r'), (3, 5, 'd')]
"ababcbababaa" <-> [(0, 0, 'a'), (0, 0, 'b'), (2, 2, 'c'), (4, 3, 'a'), (2, 2, 'a')]
"aacaacabcabaaac" <-> [(0, 0, 'a'), (1, 1, 'c'), (3, 4, 'b'), (3, 3, 'a'), (1, 2, 'c')]

来源：
en.wikipedia.org/wiki/LZ77_and_LZ78
"""

from dataclasses import dataclass

__version__ = "0.1"
__author__ = "Lucia Harcekova"


@dataclass
class Token:
    """
    表示 token 三元组的数据类，由长度、偏移量和指示符组成。
    此三元组用于 LZ77 压缩。
    """

    offset: int
    length: int
    indicator: str

    def __repr__(self) -> str:
        """
        >>> token = Token(1, 2, "c")
        >>> repr(token)
        '(1, 2, c)'
        >>> str(token)
        '(1, 2, c)'
        """
        return f"({self.offset}, {self.length}, {self.indicator})"


class LZ77Compressor:
    """
    包含使用 LZ77 压缩算法进行压缩和解压缩的方法的类。
    """

    def __init__(self, window_size: int = 13, lookahead_buffer_size: int = 6) -> None:
        self.window_size = window_size
        self.lookahead_buffer_size = lookahead_buffer_size
        self.search_buffer_size = self.window_size - self.lookahead_buffer_size

    def compress(self, text: str) -> list[Token]:
        """
        使用 LZ77 压缩算法压缩给定字符串 text。

        参数：
            text: 待压缩字符串

        返回：
            output: 以 Token 列表表示的压缩文本

        >>> lz77_compressor = LZ77Compressor()
        >>> str(lz77_compressor.compress("ababcbababaa"))
        '[(0, 0, a), (0, 0, b), (2, 2, c), (4, 3, a), (2, 2, a)]'
        >>> str(lz77_compressor.compress("aacaacabcabaaac"))
        '[(0, 0, a), (1, 1, c), (3, 4, b), (3, 3, a), (1, 2, c)]'
        """

        output = []
        search_buffer = ""

        # 当 text 中仍有待压缩字符时
        while text:
            # 查找下一个编码短语
            # - 由偏移量、长度、指示符（下一个编码字符）组成的三元组
            token = self._find_encoding_token(text, search_buffer)

            # 更新搜索缓冲区：
            # - 将 text 中的新字符加入其中
            # - 检查是否超过搜索缓冲区的最大大小，若超过则丢弃最早的元素
            search_buffer += text[: token.length + 1]
            if len(search_buffer) > self.search_buffer_size:
                search_buffer = search_buffer[-self.search_buffer_size :]

            # 更新文本
            text = text[token.length + 1 :]

            # 将 token 添加到输出
            output.append(token)

        return output

    def decompress(self, tokens: list[Token]) -> str:
        """
        将 token 列表转换为输出字符串。

        参数：
            tokens: 包含三元组（offset、length、char）的列表

        返回：
            output: 解压缩后的文本

        测试：
            >>> lz77_compressor = LZ77Compressor()
            >>> lz77_compressor.decompress([Token(0, 0, 'c'), Token(0, 0, 'a'),
            ... Token(0, 0, 'b'), Token(0, 0, 'r'), Token(3, 1, 'c'),
            ... Token(2, 1, 'd'), Token(7, 4, 'r'), Token(3, 5, 'd')])
            'cabracadabrarrarrad'
            >>> lz77_compressor.decompress([Token(0, 0, 'a'), Token(0, 0, 'b'),
            ... Token(2, 2, 'c'), Token(4, 3, 'a'), Token(2, 2, 'a')])
            'ababcbababaa'
            >>> lz77_compressor.decompress([Token(0, 0, 'a'), Token(1, 1, 'c'),
            ... Token(3, 4, 'b'), Token(3, 3, 'a'), Token(1, 2, 'c')])
            'aacaacabcabaaac'
        """

        output = ""

        for token in tokens:
            for _ in range(token.length):
                output += output[-token.offset]
            output += token.indicator

        return output

    def _find_encoding_token(self, text: str, search_buffer: str) -> Token:
        """查找文本首字符的编码 token。

        测试：
            >>> lz77_compressor = LZ77Compressor()
            >>> lz77_compressor._find_encoding_token("abrarrarrad", "abracad").offset
            7
            >>> lz77_compressor._find_encoding_token("adabrarrarrad", "cabrac").length
            1
            >>> lz77_compressor._find_encoding_token("abc", "xyz").offset
            0
            >>> lz77_compressor._find_encoding_token("", "xyz").offset
            Traceback (most recent call last):
                ...
            ValueError: We need some text to work with.
            >>> lz77_compressor._find_encoding_token("abc", "").offset
            0
        """

        if not text:
            raise ValueError("We need some text to work with.")

        # 将结果参数初始化为默认值
        length, offset = 0, 0

        if not search_buffer:
            return Token(offset, length, text[length])

        for i, character in enumerate(search_buffer):
            found_offset = len(search_buffer) - i
            if character == text[0]:
                found_length = self._match_length_from_index(text, search_buffer, 0, i)
                # 如果找到的长度大于当前长度，或长度相等但偏移量更小，
                # 则更新偏移量和长度
                if found_length >= length:
                    offset, length = found_offset, found_length

        return Token(offset, length, text[length])

    def _match_length_from_index(
        self, text: str, window: str, text_index: int, window_index: int
    ) -> int:
        """从 text 的 text_index 和 window 的 window_index 开始，
        计算 text 与 window 字符间可能的最长匹配。

        参数：
            text: _description_
            window: 滑动窗口
            text_index: 字符在 text 中的索引
            window_index: 字符在滑动窗口中的索引

        返回：
            从给定索引开始，text 与 window 之间的最大匹配长度。

        测试：
            >>> lz77_compressor = LZ77Compressor(13, 6)
            >>> lz77_compressor._match_length_from_index("rarrad", "adabrar", 0, 4)
            5
            >>> lz77_compressor._match_length_from_index("adabrarrarrad",
            ...     "cabrac", 0, 1)
            1
        """
        if not text or text[text_index] != window[window_index]:
            return 0
        return 1 + self._match_length_from_index(
            text, window + text[text_index], text_index + 1, window_index + 1
        )


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    # 初始化压缩器类
    lz77_compressor = LZ77Compressor(window_size=13, lookahead_buffer_size=6)

    # 示例
    TEXT = "cabracadabrarrarrad"
    compressed_text = lz77_compressor.compress(TEXT)
    print(lz77_compressor.compress("ababcbababaa"))
    decompressed_text = lz77_compressor.decompress(compressed_text)
    assert decompressed_text == TEXT, "The LZ77 algorithm returned the invalid result."
