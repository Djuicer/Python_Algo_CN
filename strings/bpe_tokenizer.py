"""
字节对编码（Byte-Pair Encoding）：一种基于子词的分词算法，
用于先进的语言模型。

Wikipedia: https://en.wikipedia.org/wiki/Byte_pair_encoding
"""

import itertools
from collections import OrderedDict


def get_byte_pair_counts(ids: list[int]) -> dict:
    """统计编码后字符串中连续字节对的频次。

    >>> ids = [73, 32, 97, 109, 32, 74, 111, 110, 83, 110, 111, 119, 46]
    >>> get_byte_pair_counts(ids)
    {(73, 32): 1, (32, 97): 1, (97, 109): 1, (109, 32): 1, (32, 74): 1, (74, 111): 1, (111, 110): 1, (110, 83): 1, (83, 110): 1, (110, 111): 1, (111, 119): 1, (119, 46): 1}
    >>> ids = [2, 3, 6, 2, 3, 6, 2, 5]
    >>> get_byte_pair_counts(ids)
    {(2, 3): 2, (3, 6): 2, (6, 2): 2, (2, 5): 1}
    """  # noqa: E501
    counts: dict = {}
    for pair in itertools.pairwise(ids):
        counts[pair] = counts.get(pair, 0) + 1
    return counts


def merge(ids: list[int], pair: tuple, idx: int) -> list[int]:
    """将出现次数最多的字节对替换为数据中尚未使用的新字节。
    对于 utf-8 编码，新字节编号从 256 开始

    >>> ids = [2, 3, 6, 2, 3, 6, 2, 5]
    >>> pair = (2, 3)
    >>> idx = 256
    >>> merge(ids, pair, idx)
    [256, 6, 256, 6, 2, 5]
    """
    new_ids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i] == pair[0] and ids[i + 1] == pair[1]):
            new_ids.append(idx)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids


class Tokenizer:
    """使用字节对编码算法对字符串分词"""

    def __init__(self, num_merges: int = 20, verbose: bool = False) -> None:
        self.num_merges = num_merges
        self.merges: dict = {}
        self.verbose = verbose

    def encode(self, text: str) -> list[int]:
        """将字符串转换为词元（字节）

        >>> t = Tokenizer()
        >>> text = "I am JonSnow."
        >>> t.encode(text)
        [73, 32, 97, 109, 32, 74, 111, 110, 83, 110, 111, 119, 46]

        >>> t = Tokenizer()
        >>> text = ""
        >>> t.encode(text)
        []
        """
        text_b = text.encode("utf-8")  # 原始字节
        tokens = list(map(int, text_b))  # 转换为整数列表

        if self.verbose:
            print(f"Input text: {text}")
            print(f"Tokens: {tokens}")

        ids = list(tokens)  # 创建 tokens 的副本
        self.merges = OrderedDict()  # 保存合并映射 (int, int) -> int
        max_merges = len(tokens) - 1
        num_merges = min(self.num_merges, max_merges)
        # 开始合并出现次数最多的字节对
        for i in range(num_merges):
            counts = get_byte_pair_counts(ids)
            pair = max(counts, key=counts.__getitem__)

            if counts[pair] == 1:
                continue

            idx = 256 + i  # 每次合并都创建新词元
            if self.verbose:
                print(f"Merging {pair} into a new token {idx}")
            ids = merge(ids, pair, idx)
            self.merges[pair] = idx

        return ids

    def decode(self, ids: list[int]) -> str:
        """将词元列表还原为原始字符串

        >>> t = Tokenizer()
        >>> ids = [73, 32, 97, 109, 32, 74, 111, 110, 83, 110, 111, 119, 46]
        >>> t.decode(ids)
        'I am JonSnow.'

        >>> t = Tokenizer()
        >>> ids = []
        >>> t.decode(ids)
        ''
        """
        vocab = {idx: bytes([idx]) for idx in range(256)}  # 原始词表
        # 各项应按插入顺序
        # 迭代。Python 3 默认如此，
        # 但这里显式使用 OrderedDict
        for (p0, p1), idx in self.merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]

        if self.verbose:
            print("Vocabulary (after merging): {vocab}")

        tokens = b"".join(vocab[idx] for idx in ids)
        # 通过替换无效的起始字节来处理 UnicodeDecodeError，
        # 使其符合 utf-8 格式
        text = tokens.decode("utf-8", errors="replace")
        return text


if __name__ == "__main__":
    import doctest

    doctest.testmod()
