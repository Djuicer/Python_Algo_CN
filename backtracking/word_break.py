"""
单词拆分（Word Break）是计算机科学中的一个经典问题。
给定字符串和单词词典，判断能否将
该字符串拆分为一个或多个词典单词组成的序列。

Wikipedia: https://en.wikipedia.org/wiki/Word_break_problem
"""


def backtrack(input_string: str, word_dict: set[str], start: int) -> bool:
    """
    使用回溯法判断从索引 'start' 开始
    能否进行有效单词拆分的辅助函数。

    参数：
    input_string (str): 待拆分的输入字符串。
    word_dict (set[str]): 有效词典单词的集合。
    start (int): 待检查子串的起始索引。

    返回：
    bool: 能有效拆分时返回 True，否则返回 False。

    示例：
    >>> backtrack("leetcode", {"leet", "code"}, 0)
    True

    >>> backtrack("applepenapple", {"apple", "pen"}, 0)
    True

    >>> backtrack("catsandog", {"cats", "dog", "sand", "and", "cat"}, 0)
    False
    """

    # 递归终止条件：起始索引已到达字符串末尾
    if start == len(input_string):
        return True

    # 尝试所有从 'start' 到 'end' 的可能子串
    for end in range(start + 1, len(input_string) + 1):
        if input_string[start:end] in word_dict and backtrack(
            input_string, word_dict, end
        ):
            return True

    return False


def word_break(input_string: str, word_dict: set[str]) -> bool:
    """
    使用回溯法判断输入字符串能否拆分为
    有效词典单词组成的序列。

    参数：
    input_string (str): 待拆分的输入字符串。
    word_dict (set[str]): 有效单词集合。

    返回：
    bool: 字符串能拆分为有效单词时返回 True，否则返回 False。

    示例：
    >>> word_break("leetcode", {"leet", "code"})
    True

    >>> word_break("applepenapple", {"apple", "pen"})
    True

    >>> word_break("catsandog", {"cats", "dog", "sand", "and", "cat"})
    False

    >>> word_break("applepenapple", {})
    False
    """

    return backtrack(input_string, word_dict, 0)
