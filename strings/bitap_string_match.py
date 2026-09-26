"""
Bitap 精确字符串匹配
https://en.wikipedia.org/wiki/Bitap_algorithm

在文本中搜索模式，返回模式第一次出现的
索引。文本和模式均仅由小写字母组成。

复杂度：O(m*n)
    n = 文本长度
    m = 模式长度

可使用以下命令运行 Python doctest：
python3 -m doctest -v bitap_string_match.py
"""


def bitap_string_match(text: str, pattern: str) -> int:
    """
    获取 pattern 在 text 中第一次出现的索引。

    Args:
        text: 仅由小写字母组成的字符串。
        pattern: 仅由小写字母组成的字符串。

    Returns:
        int: pattern 第一次出现的索引，未找到则返回 -1。

    >>> bitap_string_match('abdabababc', 'ababc')
    5
    >>> bitap_string_match('aaaaaaaaaaaaaaaaaa', 'a')
    0
    >>> bitap_string_match('zxywsijdfosdfnso', 'zxywsijdfosdfnso')
    0
    >>> bitap_string_match('abdabababc', '')
    0
    >>> bitap_string_match('abdabababc', 'c')
    9
    >>> bitap_string_match('abdabababc', 'fofosdfo')
    -1
    >>> bitap_string_match('abdab', 'fofosdfo')
    -1
    """
    if not pattern:
        return 0
    m = len(pattern)
    if m > len(text):
        return -1

    # 位串的初始状态为 1110
    state = ~1
    # 若字符出现在该索引处，则对应位为 0，否则为 1
    pattern_mask: list[int] = [~0] * 27  # 1111

    for i, char in enumerate(pattern):
        # 在该字符的模式掩码中，将字符出现的
        # 每个位置 i 对应的位设为 0。
        pattern_index: int = ord(char) - ord("a")
        pattern_mask[pattern_index] &= ~(1 << i)

    for i, char in enumerate(text):
        text_index = ord(char) - ord("a")
        # 若字符未出现在模式中，其模式掩码为 1111。
        # 将状态与 1111 按位或，会把状态重置为 1111，
        # 重新开始查找模式的起点。
        state |= pattern_mask[text_index]
        state <<= 1

        # 若状态从右向左数的第 m 位为 0，说明
        # 已在文本中找到模式
        if (state & (1 << m)) == 0:
            return i - m + 1

    return -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
