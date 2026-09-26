from __future__ import annotations


def knuth_morris_pratt(text: str, pattern: str) -> int:
    """
    Knuth-Morris-Pratt（KMP）算法用于在文本中查找模式，
    复杂度为 O(n + m)

    1) 预处理模式，找出与前缀相同的后缀

        这样，当模式中的字符与文本失配时，
        就能确定从哪里继续匹配。

    2) 逐字符遍历文本，与模式字符比较，
        必要时更新模式中的当前位置

    >>> kmp = "knuth_morris_pratt"
    >>> all(
    ...    knuth_morris_pratt(kmp, s) == kmp.find(s)
    ...    for s in ("kn", "h_m", "rr", "tt", "not there")
    ... )
    True
    """

    # 1) 构建失配数组
    failure = get_failure_array(pattern)

    # 2) 遍历文本，查找模式
    i, j = 0, 0  # 文本和模式中的索引
    while i < len(text):
        if pattern[j] == text[i]:
            if j == (len(pattern) - 1):
                return i - j
            j += 1

        # 如果这是模式中的一个前缀，
        # 则只需回退到足以继续匹配的位置
        elif j > 0:
            j = failure[j - 1]
            continue
        i += 1
    return -1


def get_failure_array(pattern: str) -> list[int]:
    """
    计算比较失败后应转到的新索引
    :param pattern:
    :return:
    """
    failure = [0]
    i = 0
    j = 1
    while j < len(pattern):
        if pattern[i] == pattern[j]:
            i += 1
        elif i > 0:
            i = failure[i - 1]
            continue
        j += 1
        failure.append(i)
    return failure


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 测试 1)
    pattern = "abc1abc12"
    text1 = "alskfjaldsabc1abc1abc12k23adsfabcabc"
    text2 = "alskfjaldsk23adsfabcabc"
    assert knuth_morris_pratt(text1, pattern)
    assert knuth_morris_pratt(text2, pattern)

    # 测试 2)
    pattern = "ABABX"
    text = "ABABZABABYABABX"
    assert knuth_morris_pratt(text, pattern)

    # 测试 3)
    pattern = "AAAB"
    text = "ABAAAAAB"
    assert knuth_morris_pratt(text, pattern)

    # 测试 4)
    pattern = "abcdabcy"
    text = "abcxabcdabxabcdabcdabcy"
    assert knuth_morris_pratt(text, pattern)

    # 测试 5) -> doctest
    kmp = "knuth_morris_pratt"
    assert all(
        knuth_morris_pratt(kmp, s) == kmp.find(s)
        for s in ("kn", "h_m", "rr", "tt", "not there")
    )

    # 测试 6)
    pattern = "aabaabaaa"
    assert get_failure_array(pattern) == [0, 1, 0, 1, 2, 3, 4, 5, 2]
