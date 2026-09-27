"""
正则表达式匹配用于检查文本是否与模式匹配。
模式：

    1. ``.`` 匹配任意单个字符。
    2. ``*`` 匹配前一个元素零次或多次。

更多信息：
    https://medium.com/trick-the-interviwer/regular-expression-matching-9972eb74c03
"""


def recursive_match(text: str, pattern: str) -> bool:
    r"""
    递归匹配算法。

    | 时间复杂度：O(2^(\|text\| + \|pattern\|))
    | 空间复杂度：递归深度为 O(\|text\| + \|pattern\|)。

    :param text: 要匹配的文本。
    :param pattern: 要匹配的模式。
    :return: ``True`` 表示 `text` 与 `pattern` 匹配，``False`` 表示不匹配。

    >>> recursive_match('abc', 'a.c')
    True
    >>> recursive_match('abc', 'af*.c')
    True
    >>> recursive_match('abc', 'a.c*')
    True
    >>> recursive_match('abc', 'a.c*d')
    False
    >>> recursive_match('aa', '.*')
    True
    """
    if not pattern:
        return not text

    if not text:
        return pattern[-1] == "*" and recursive_match(text, pattern[:-2])

    if text[-1] == pattern[-1] or pattern[-1] == ".":
        return recursive_match(text[:-1], pattern[:-1])

    if pattern[-1] == "*":
        return recursive_match(text[:-1], pattern) or recursive_match(
            text, pattern[:-2]
        )

    return False


def dp_match(text: str, pattern: str) -> bool:
    r"""
    动态规划匹配算法。

    | 时间复杂度：O(\|text\| * \|pattern\|)
    | 空间复杂度：O(\|text\| * \|pattern\|)

    :param text: 要匹配的文本。
    :param pattern: 要匹配的模式。
    :return: ``True`` 表示 `text` 与 `pattern` 匹配，``False`` 表示不匹配。

    >>> dp_match('abc', 'a.c')
    True
    >>> dp_match('abc', 'af*.c')
    True
    >>> dp_match('abc', 'a.c*')
    True
    >>> dp_match('abc', 'a.c*d')
    False
    >>> dp_match('aa', '.*')
    True
    """
    m = len(text)
    n = len(pattern)
    dp = [[False for _ in range(n + 1)] for _ in range(m + 1)]
    dp[0][0] = True

    for j in range(1, n + 1):
        dp[0][j] = pattern[j - 1] == "*" and dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pattern[j - 1] in {".", text[i - 1]}:
                dp[i][j] = dp[i - 1][j - 1]
            elif pattern[j - 1] == "*":
                dp[i][j] = dp[i][j - 2]
                if pattern[j - 2] in {".", text[i - 1]}:
                    dp[i][j] |= dp[i - 1][j]
            else:
                dp[i][j] = False

    return dp[m][n]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
