"""
LCS 问题描述：给定两个序列，求同时存在于两者中的最长子序列长度。
子序列中的元素保持相同的相对顺序，但不一定连续。
示例："abc", "abg" 都是 "abcdefgh" 的子序列。
"""


def longest_common_subsequence(x: str, y: str):
    """
    查找两个字符串的最长公共子序列，同时返回找到的子序列。

    参数
    ----------

    x: str，其中一个字符串。
    y: str，另一个字符串。

    返回
    -------
    L[m][n]: int，最长子序列的长度，也等于 len(seq)。
    Seq: str，找到的子序列。

    >>> longest_common_subsequence("programming", "gaming")
    (6, 'gaming')
    >>> longest_common_subsequence("physics", "smartphone")
    (2, 'ph')
    >>> longest_common_subsequence("computer", "food")
    (1, 'o')
    >>> longest_common_subsequence("", "abc")  # One string is empty
    (0, '')
    >>> longest_common_subsequence("abc", "")  # Other string is empty
    (0, '')
    >>> longest_common_subsequence("", "")  # Both strings are empty
    (0, '')
    >>> longest_common_subsequence("abc", "def")  # No common subsequence
    (0, '')
    >>> longest_common_subsequence("abc", "abc")  # Identical strings
    (3, 'abc')
    >>> longest_common_subsequence("a", "a")  # Single character match
    (1, 'a')
    >>> longest_common_subsequence("a", "b")  # Single character no match
    (0, '')
    >>> longest_common_subsequence("abcdef", "ace")  # Interleaved subsequence
    (3, 'ace')
    >>> longest_common_subsequence("ABCD", "ACBD")  # No repeated characters
    (3, 'ABD')
    """
    # 获取字符串长度

    assert x is not None
    assert y is not None

    m = len(x)
    n = len(y)

    # 声明用于存储 dp 值的数组
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = 1 if x[i - 1] == y[j - 1] else 0

            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1] + match)

    seq = ""
    i, j = m, n
    while i > 0 and j > 0:
        match = 1 if x[i - 1] == y[j - 1] else 0

        if dp[i][j] == dp[i - 1][j - 1] + match:
            if match == 1:
                seq = x[i - 1] + seq
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], seq


if __name__ == "__main__":
    a = "AGGTAB"
    b = "GXTXAYB"
    expected_ln = 4
    expected_subseq = "GTAB"

    ln, subseq = longest_common_subsequence(a, b)
    print("len =", ln, ", sub-sequence =", subseq)
    import doctest

    doctest.testmod()
