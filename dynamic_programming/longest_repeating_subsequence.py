"""
最长重复子序列（LRS）

给定一个字符串，求最长重复子序列的长度，即至少出现两次的最长子序列。
两次出现必须使用原字符串中不同位置的字符。

这是最长公共子序列（LCS）问题的一种变体：求字符串与自身的 LCS，
同时约束同一索引位置的字符不能在两个子序列中同时使用。

Reference: https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
"""


def longest_repeating_subsequence(string: str) -> int:
    """
    求给定字符串中最长重复子序列的长度。

    重复子序列是在字符串中至少出现两次的子序列，其中同一索引处的字符
    不能同时计入两个子序列。

    使用动态规划，时间复杂度为 O(n^2)，空间复杂度为 O(n^2)，
    其中 n 是输入字符串的长度。

    参数
    ----------
    string : str
        要在其中查找重复子序列的输入字符串。

    返回
    -------
    int
        最长重复子序列的长度。

    示例
    --------
    >>> longest_repeating_subsequence("aabb")
    2
    >>> longest_repeating_subsequence("aab")
    1
    >>> longest_repeating_subsequence("axxxy")
    2
    >>> longest_repeating_subsequence("abcabc")
    3
    >>> longest_repeating_subsequence("")
    0
    >>> longest_repeating_subsequence("a")
    0
    >>> longest_repeating_subsequence("abcdef")
    0
    >>> longest_repeating_subsequence("aaa")
    2
    >>> longest_repeating_subsequence("aaaa")
    3
    >>> longest_repeating_subsequence(12345)
    Traceback (most recent call last):
        ...
    TypeError: Input must be a string, got int
    """
    if not isinstance(string, str):
        msg = f"Input must be a string, got {type(string).__name__}"
        raise TypeError(msg)

    n = len(string)
    if n == 0:
        return 0

    # dp[i][j] 存储考虑 string[0..i-1] 和 string[0..j-1] 时
    # 最长重复子序列的长度
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # 字符匹配且位于不同位置
            if string[i - 1] == string[j - 1] and i != j:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][n]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
