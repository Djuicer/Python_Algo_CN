"""
author: Sanket Kittad
给定字符串 s，求 s 中最长回文子序列的长度。
输入：s = "bbbab"
输出：4
解释：一个可能的最长回文子序列是 "bbbb"。
Leetcode link: https://leetcode.com/problems/longest-palindromic-subsequence/description/
"""


def longest_palindromic_subsequence(input_string: str) -> int:
    """
    此函数返回字符串中最长回文子序列的长度。
    >>> longest_palindromic_subsequence("bbbab")
    4
    >>> longest_palindromic_subsequence("bbabcbcab")
    7
    """
    n = len(input_string)
    rev = input_string[::-1]
    m = len(rev)
    dp = [[-1] * (m + 1) for i in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 0
    for i in range(m + 1):
        dp[0][i] = 0

    # 创建并初始化 dp 数组
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # 如果 i 和 j 处的字符相同，则将其纳入回文子序列
            if input_string[i - 1] == rev[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
