"""
此脚本实现 Damerau-Levenshtein 距离算法。

该算法用于度量两个字符串序列之间的编辑距离

关于该算法的更多信息可见以下维基百科文章：
https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
"""


def damerau_levenshtein_distance(first_string: str, second_string: str) -> int:
    """
    实现 Damerau-Levenshtein 距离算法，用于度量
    两个字符串之间的编辑距离。

    参数：
        first_string: 第一个待比较字符串
        second_string: 第二个待比较字符串

    返回：
        distance: 两个字符串之间的编辑距离

    >>> damerau_levenshtein_distance("cat", "cut")
    1
    >>> damerau_levenshtein_distance("kitten", "sitting")
    3
    >>> damerau_levenshtein_distance("hello", "world")
    4
    >>> damerau_levenshtein_distance("book", "back")
    2
    >>> damerau_levenshtein_distance("container", "containment")
    3
    >>> damerau_levenshtein_distance("container", "containment")
    3
    """
    # 创建动态规划矩阵以保存距离
    dp_matrix = [[0] * (len(second_string) + 1) for _ in range(len(first_string) + 1)]

    # 初始化矩阵
    for i in range(len(first_string) + 1):
        dp_matrix[i][0] = i
    for j in range(len(second_string) + 1):
        dp_matrix[0][j] = j

    # 填充矩阵
    for i, first_char in enumerate(first_string, start=1):
        for j, second_char in enumerate(second_string, start=1):
            cost = int(first_char != second_char)

            dp_matrix[i][j] = min(
                dp_matrix[i - 1][j] + 1,  # 删除
                dp_matrix[i][j - 1] + 1,  # 插入
                dp_matrix[i - 1][j - 1] + cost,  # 替换
            )

            if (
                i > 1
                and j > 1
                and first_string[i - 1] == second_string[j - 2]
                and first_string[i - 2] == second_string[j - 1]
            ):
                # 交换相邻字符
                dp_matrix[i][j] = min(dp_matrix[i][j], dp_matrix[i - 2][j - 2] + cost)

    return dp_matrix[-1][-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
