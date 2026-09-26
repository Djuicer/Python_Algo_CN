"""
Boyer-Moore-Horspool 字符串搜索算法。

这是 Boyer-Moore 算法的简化版本，只保留
坏字符位移表（Horspool 变体）。其平均运行时间仍为
次线性（随机文本约为 O(n / m)），
最坏为 O(n * m)。空间为 O(sigma)，其中 sigma 为
模式中出现的字符集大小。

Reference: https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore%E2%80%93Horspool_algorithm
"""

from __future__ import annotations


def _build_shift_table(pattern: str) -> dict[str, int]:
    """
    构建 ``pattern`` 的坏字符位移表。

    对于模式中除最后一个字符外的各个字符，
    表中记录该字符到模式末尾的距离。
    模式中未出现的字符在查询时
    使用默认值 ``len(pattern)``。

    >>> _build_shift_table("abcab")
    {'a': 1, 'b': 3, 'c': 2}
    >>> _build_shift_table("a")
    {}
    >>> _build_shift_table("")
    {}
    >>> _build_shift_table("aaaa")
    {'a': 1}
    """
    pattern_length = len(pattern)
    table: dict[str, int] = {}
    for index in range(pattern_length - 1):
        table[pattern[index]] = pattern_length - 1 - index
    return table


def boyer_moore_horspool_search(text: str, pattern: str) -> int:
    """
    返回 ``pattern`` 在 ``text`` 中第一次出现的索引，
    未出现则返回 ``-1``。

    空模式在位置 ``0`` 匹配（与
    :py:meth:`str.find` 的约定一致）。

    >>> boyer_moore_horspool_search("ABAAABCD", "ABC")
    4
    >>> boyer_moore_horspool_search("hello world", "world")
    6
    >>> boyer_moore_horspool_search("hello world", "Python")
    -1
    >>> boyer_moore_horspool_search("aaaaa", "aa")
    0
    >>> boyer_moore_horspool_search("anything", "")
    0
    >>> boyer_moore_horspool_search("", "x")
    -1
    >>> sample = "the quick brown fox jumps over the lazy dog"
    >>> boyer_moore_horspool_search(sample, "fox") == sample.find("fox")
    True
    >>> boyer_moore_horspool_search(sample, "cat") == sample.find("cat")
    True
    """
    pattern_length = len(pattern)
    text_length = len(text)
    if pattern_length == 0:
        return 0
    if pattern_length > text_length:
        return -1

    shift_table = _build_shift_table(pattern)
    skip = 0
    while text_length - skip >= pattern_length:
        index = pattern_length - 1
        while index >= 0 and pattern[index] == text[skip + index]:
            index -= 1
        if index < 0:
            return skip
        skip += shift_table.get(text[skip + pattern_length - 1], pattern_length)
    return -1


def boyer_moore_horspool_search_all(text: str, pattern: str) -> list[int]:
    """
    返回 ``pattern`` 在 ``text`` 中所有出现位置的起始索引。

    包含重叠匹配（例如 ``"aaa"`` 中的 ``"aa"``
    出现在索引 ``0`` 和 ``1``）。空模式在
    ``0`` 到 ``len(text)``（包含两端）的所有位置匹配，与
    :py:meth:`str.find` 和 :py:func:`re.finditer` 的约定一致。

    >>> boyer_moore_horspool_search_all("ababcabab", "ab")
    [0, 2, 5, 7]
    >>> boyer_moore_horspool_search_all("aaaa", "aa")
    [0, 1, 2]
    >>> boyer_moore_horspool_search_all("abcdef", "gh")
    []
    >>> boyer_moore_horspool_search_all("abc", "")
    [0, 1, 2, 3]
    >>> boyer_moore_horspool_search_all("", "abc")
    []
    """
    pattern_length = len(pattern)
    text_length = len(text)
    if pattern_length == 0:
        return list(range(text_length + 1))
    if pattern_length > text_length:
        return []

    shift_table = _build_shift_table(pattern)
    matches: list[int] = []
    skip = 0
    while text_length - skip >= pattern_length:
        index = pattern_length - 1
        while index >= 0 and pattern[index] == text[skip + index]:
            index -= 1
        if index < 0:
            matches.append(skip)
            skip += 1
        else:
            skip += shift_table.get(text[skip + pattern_length - 1], pattern_length)
    return matches


if __name__ == "__main__":
    import doctest

    doctest.testmod()
