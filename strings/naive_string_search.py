"""
https://en.wikipedia.org/wiki/String-searching_algorithm#Na%C3%AFve_string_search
从主字符串 mainString 的每个位置尝试匹配模式。
若在位置 i 找到模式，则将该位置加入
答案，再从位置 i+1 继续执行相同操作
复杂度：O(n*m)
    n=主字符串长度
    m=模式字符串长度
"""


def naive_pattern_search(s: str, pattern: str) -> list:
    """
    >>> naive_pattern_search("ABAAABCDBBABCDDEBCABC", "ABC")
    [4, 10, 18]
    >>> naive_pattern_search("ABC", "ABAAABCDBBABCDDEBCABC")
    []
    >>> naive_pattern_search("", "ABC")
    []
    >>> naive_pattern_search("TEST", "TEST")
    [0]
    >>> naive_pattern_search("ABCDEGFTEST", "TEST")
    [7]
    """
    pat_len = len(pattern)
    position = []
    for i in range(len(s) - pat_len + 1):
        match_found = True
        for j in range(pat_len):
            if s[i + j] != pattern[j]:
                match_found = False
                break
        if match_found:
            position.append(i)
    return position


if __name__ == "__main__":
    assert naive_pattern_search("ABCDEFG", "DE") == [3]
    print(naive_pattern_search("ABAAABCDBBABCDDEBCABC", "ABC"))
