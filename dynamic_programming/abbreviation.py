"""
https://www.hackerrank.com/challenges/abbr/problem
可以对某个字符串执行以下操作：

1. 将某些索引 i 处的零个或多个小写字母转换为大写
   （即，使它们成为大写字母）。
2. 删除其余所有小写字母。

示例：
a=daBcd and b="ABC"
daBcd -> 将 a 和 c 转换为大写(dABCd) -> 删除 d (ABC)
"""


def abbr(a: str, b: str) -> bool:
    """
    >>> abbr("daBcd", "ABC")
    True
    >>> abbr("dBcd", "ABC")
    False
    """
    n = len(a)
    m = len(b)
    dp = [[False for _ in range(m + 1)] for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(n):
        for j in range(m + 1):
            if dp[i][j]:
                if j < m and a[i].upper() == b[j]:
                    dp[i + 1][j + 1] = True
                if a[i].islower():
                    dp[i + 1][j] = True
    return dp[n][m]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
