"""
Author  : Alexander Pantyukhin
Date    : October 14, 2022
这是使用自顶向下方法求编辑距离的实现。
此实现在 Leetcode 上通过了测试：https://leetcode.com/problems/edit-distance/

Levinstein 距离
动态规划（Dynamic Programming）：自顶向下。
"""

import functools


def min_distance_up_bottom(word1: str, word2: str) -> int:
    """
    >>> min_distance_up_bottom("intention", "execution")
    5
    >>> min_distance_up_bottom("intention", "")
    9
    >>> min_distance_up_bottom("", "")
    0
    >>> min_distance_up_bottom("zooicoarchaeologist", "zoologist")
    10
    """
    len_word1 = len(word1)
    len_word2 = len(word2)

    @functools.cache
    def min_distance(index1: int, index2: int) -> int:
        # 如果第一个单词的索引越界，则删除第二个单词中的所有剩余字符
        if index1 >= len_word1:
            return len_word2 - index2
        # 如果第二个单词的索引越界，则删除第一个单词中的所有剩余字符
        if index2 >= len_word2:
            return len_word1 - index1
        diff = int(word1[index1] != word2[index2])  # 当前字母不相同
        return min(
            1 + min_distance(index1 + 1, index2),
            1 + min_distance(index1, index2 + 1),
            diff + min_distance(index1 + 1, index2 + 1),
        )

    return min_distance(0, 0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
