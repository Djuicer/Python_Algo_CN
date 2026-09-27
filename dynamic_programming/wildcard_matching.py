"""
Author  : ilyas dahhou
Date    : Oct 7, 2023

任务：
给定输入字符串和模式，实现支持 '?' 和 '*' 的通配符模式匹配，其中：
'?' 匹配任意单个字符。
'*' 匹配任意字符序列（包括空序列）。
匹配应覆盖整个输入字符串（而非局部）。

运行时间复杂度：O(m * n)

此实现在 leetcode 上通过了测试：
https://leetcode.com/problems/wildcard-matching/
"""


def is_match(string: str, pattern: str) -> bool:
    """
    >>> is_match("", "")
    True
    >>> is_match("aa", "a")
    False
    >>> is_match("abc", "abc")
    True
    >>> is_match("abc", "*c")
    True
    >>> is_match("abc", "a*")
    True
    >>> is_match("abc", "*a*")
    True
    >>> is_match("abc", "?b?")
    True
    >>> is_match("abc", "*?")
    True
    >>> is_match("abc", "a*d")
    False
    >>> is_match("abc", "a*c?")
    False
    >>> is_match('baaabab','*****ba*****ba')
    False
    >>> is_match('baaabab','*****ba*****ab')
    True
    >>> is_match('aa','*')
    True
    """
    dp = [[False] * (len(pattern) + 1) for _ in string + "1"]
    dp[0][0] = True
    # 填充第一行
    for j, char in enumerate(pattern, 1):
        if char == "*":
            dp[0][j] = dp[0][j - 1]
    # 填充 DP 表的其余部分
    for i, s_char in enumerate(string, 1):
        for j, p_char in enumerate(pattern, 1):
            if p_char in (s_char, "?"):
                dp[i][j] = dp[i - 1][j - 1]
            elif pattern[j - 1] == "*":
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
    return dp[len(string)][len(pattern)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(f"{is_match('baaabab','*****ba*****ab') = }")
