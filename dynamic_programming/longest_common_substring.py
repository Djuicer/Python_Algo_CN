"""
最长公共子串问题描述：
    给定两个序列，查找同时存在于两者中的最长公共子串。
    子串必然是连续的。

示例：
    ``abcdef`` 和 ``xabded`` 有两个最长公共子串：``ab`` 或 ``de``。
    因此，算法应返回其中任意一个。
"""


def longest_common_substring(text1: str, text2: str) -> str:
    """
    查找两个字符串之间的最长公共子串。

    >>> longest_common_substring("", "")
    ''
    >>> longest_common_substring("a","")
    ''
    >>> longest_common_substring("", "a")
    ''
    >>> longest_common_substring("a", "a")
    'a'
    >>> longest_common_substring("abcdef", "bcd")
    'bcd'
    >>> longest_common_substring("abcdef", "xabded")
    'ab'
    >>> longest_common_substring("GeeksforGeeks", "GeeksQuiz")
    'Geeks'
    >>> longest_common_substring("abcdxyz", "xyzabcd")
    'abcd'
    >>> longest_common_substring("zxabcdezy", "yzabcdezx")
    'abcdez'
    >>> longest_common_substring("OldSite:GeeksforGeeks.org", "NewSite:GeeksQuiz.com")
    'Site:Geeks'
    >>> longest_common_substring(1, 1)
    Traceback (most recent call last):
        ...
    ValueError: longest_common_substring() takes two strings for inputs
    """

    if not (isinstance(text1, str) and isinstance(text2, str)):
        raise ValueError("longest_common_substring() takes two strings for inputs")

    if not text1 or not text2:
        return ""

    text1_length = len(text1)
    text2_length = len(text2)

    dp = [[0] * (text2_length + 1) for _ in range(text1_length + 1)]
    end_pos = 0
    max_length = 0

    for i in range(1, text1_length + 1):
        for j in range(1, text2_length + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                if dp[i][j] > max_length:
                    end_pos = i
                    max_length = dp[i][j]

    return text1[end_pos - max_length : end_pos]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
