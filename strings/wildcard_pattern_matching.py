"""
实现支持 '.' 和 '*' 的正则表达式匹配。
'.' 匹配任意单个字符。
'*' 匹配前一个元素零次或多次。
匹配应覆盖整个输入字符串，而非部分匹配。

"""


def match_pattern(input_string: str, pattern: str) -> bool:
    """
    使用自底向上的动态规划，匹配输入字符串
    与给定模式。

    运行时间：O(len(input_string)*len(pattern))

    参数
    --------
    input_string: str，待与模式比较的任意字符串
    pattern: str，表示模式的字符串，可以包含
    匹配单个字符的 '.'，以及匹配前一个字符零次或多次的
    '*'

    注意
    ----
    模式不能以 '*' 开头，
    因为 * 前至少应有一个字符

    返回
    -------
    表示给定字符串是否匹配模式的布尔值

    示例
    -------
    >>> match_pattern("aab", "c*a*b")
    True
    >>> match_pattern("dabc", "*abc")
    False
    >>> match_pattern("aaa", "aa")
    False
    >>> match_pattern("aaa", "a.a")
    True
    >>> match_pattern("aaab", "aa*")
    False
    >>> match_pattern("aaab", ".*")
    True
    >>> match_pattern("a", "bbbb")
    False
    >>> match_pattern("", "bbbb")
    False
    >>> match_pattern("a", "")
    False
    >>> match_pattern("", "")
    True
    """

    len_string = len(input_string) + 1
    len_pattern = len(pattern) + 1

    # dp 是二维矩阵，dp[i][j] 表示 input_string 的
    # 长度为 i 的前缀，是否与给定 pattern 的长度为 j 的
    # 前缀匹配。
    # "dp" 表示动态规划。
    dp = [[0 for i in range(len_pattern)] for j in range(len_string)]

    # 长度为零的字符串与长度为零的模式匹配
    dp[0][0] = 1

    # 长度为零的模式永远无法匹配非空字符串
    for i in range(1, len_string):
        dp[i][0] = 0

    # 长度为零的字符串可以匹配
    # 含有交替出现的 * 的模式
    for j in range(1, len_pattern):
        dp[0][j] = dp[0][j - 2] if pattern[j - 1] == "*" else 0

    # 使用自底向上的方法求出其余所有长度的匹配结果
    for i in range(1, len_string):
        for j in range(1, len_pattern):
            if input_string[i - 1] == pattern[j - 1] or pattern[j - 1] == ".":
                dp[i][j] = dp[i - 1][j - 1]

            elif pattern[j - 1] == "*":
                if dp[i][j - 2] == 1:
                    dp[i][j] = 1
                elif pattern[j - 2] in (input_string[i - 1], "."):
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = 0
            else:
                dp[i][j] = 0

    return bool(dp[-1][-1])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # 输入字符串
    # input_string = input("input a string :")
    # pattern = input("input a pattern :")

    input_string = "aab"
    pattern = "c*a*b"

    # 使用函数检查给定字符串是否匹配给定模式
    if match_pattern(input_string, pattern):
        print(f"{input_string} matches the given pattern {pattern}")
    else:
        print(f"{input_string} does not match with the given pattern {pattern}")
