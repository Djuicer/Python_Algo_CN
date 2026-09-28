"""
See https://en.wikipedia.org/wiki/Bloom_filter

使用 的 此 数据 结构 是 到 测试 membership 在 集合。
Compared 到 Python's built-在 集合() 它 是 更多 空间-efficient。
在 following 示例，仅 8 bits 的 memory 将 为 使用：
>>> bloom = Bloom(size=8)

Initially，filter 包含 所有 zeros：
>>> bloom.bitstring
'00000000'

当 元素 是 added，两个 bits 是 集合 到 1
since 其中 是 2 哈希 函数 在 此 实现：
>>> "Titanic" in bloom
False
>>> bloom.add("Titanic")
>>> bloom.bitstring
'01100000'
>>> "Titanic" in bloom
True

However，sometimes 仅 一个 bit 是 added
因为 两者 哈希 函数 返回 相同 值
>>> bloom.add("Avatar")
>>> "Avatar" in bloom
True
>>> bloom.format_hash("Avatar")
'00000100'
>>> bloom.bitstring
'01100100'

不 added 元素 应 返回 False ..。
>>> not_present_films = ("The Godfather", "Interstellar", "Parasite", "Pulp Fiction")
>>> {
...   film: bloom.format_hash(film) for film in not_present_films
... } # doctest: +NORMALIZE_WHITESPACE
{'The Godfather': '00000101',
 'Interstellar': '00000011',
 'Parasite': '00010010',
 'Pulp Fiction': '10000100'}
>>> any(film in bloom for film in not_present_films)
False

但是 sometimes 其中 是 false positives：
>>> "Ratatouille" in bloom
True
>>> bloom.format_hash("Ratatouille")
'01100000'

probability increases 带有 元素数量 added。
probability decreases 带有 数 的 bits 在 bitarray。
>>> bloom.estimated_error_rate
0.140625
>>> bloom.add("The Godfather")
>>> bloom.estimated_error_rate
0.25
>>> bloom.bitstring
'01100101'
"""

from hashlib import md5, sha256

HASH_FUNCTIONS = (sha256, md5)


class Bloom:
    def __init__(self, size: int = 8) -> None:
        self.bitarray = 0b0
        self.size = size

    def add(self, value: str) -> None:
        h = self.hash_(value)
        self.bitarray |= h

    def exists(self, value: str) -> bool:
        h = self.hash_(value)
        return (h & self.bitarray) == h

    def __contains__(self, other: str) -> bool:
        return self.exists(other)

    def format_bin(self, bitarray: int) -> str:
        res = bin(bitarray)[2:]
        return res.zfill(self.size)

    @property
    def bitstring(self) -> str:
        return self.format_bin(self.bitarray)

    def hash_(self, value: str) -> int:
        res = 0b0
        for func in HASH_FUNCTIONS:
            position = (
                int.from_bytes(func(value.encode()).digest(), "little") % self.size
            )
            res |= 2**position
        return res

    def format_hash(self, value: str) -> str:
        return self.format_bin(self.hash_(value))

    @property
    def estimated_error_rate(self) -> float:
        n_ones = bin(self.bitarray).count("1")
        return (n_ones / self.size) ** len(HASH_FUNCTIONS)
