"""
Author  : Alexander Pantyukhin
Date    : December 12, 2022

任务：
给定一个字符串和一个单词列表，如果该字符串可以拆分为由空格分隔的一个或多个单词序列，
则返回 true。

请注意，同一个单词在拆分中可以重复使用多次。

实现说明：Trie + 自顶向下动态规划。
Trie 用于存储单词，便于扫描字符串当前位置可用的单词。

Leetcode:
https://leetcode.com/problems/word-break/description/

运行时间：O(n * n)
空间：O(n)
"""

import functools
from typing import Any


def word_break(string: str, words: list[str]) -> bool:
    """
    如果数字符号相反则返回 True，否则返回 False。

    >>> word_break("applepenapple", ["apple","pen"])
    True
    >>> word_break("catsandog", ["cats","dog","sand","and","cat"])
    False
    >>> word_break("cars", ["car","ca","rs"])
    True
    >>> word_break('abc', [])
    False
    >>> word_break(123, ['a'])
    Traceback (most recent call last):
        ...
    ValueError: the string should be not empty string
    >>> word_break('', ['a'])
    Traceback (most recent call last):
        ...
    ValueError: the string should be not empty string
    >>> word_break('abc', [123])
    Traceback (most recent call last):
        ...
    ValueError: the words should be a list of non-empty strings
    >>> word_break('abc', [''])
    Traceback (most recent call last):
        ...
    ValueError: the words should be a list of non-empty strings
    """

    # 验证
    if not isinstance(string, str) or len(string) == 0:
        raise ValueError("the string should be not empty string")

    if not isinstance(words, list) or not all(
        isinstance(item, str) and len(item) > 0 for item in words
    ):
        raise ValueError("the words should be a list of non-empty strings")

    # 构建 trie
    trie: dict[str, Any] = {}
    word_keeper_key = "WORD_KEEPER"

    for word in words:
        trie_node = trie
        for c in word:
            if c not in trie_node:
                trie_node[c] = {}

            trie_node = trie_node[c]

        trie_node[word_keeper_key] = True

    len_string = len(string)

    # 动态规划方法
    @functools.cache
    def is_breakable(index: int) -> bool:
        """
        >>> string = 'a'
        >>> is_breakable(1)
        True
        """
        if index == len_string:
            return True

        trie_node: Any = trie
        for i in range(index, len_string):
            trie_node = trie_node.get(string[i], None)

            if trie_node is None:
                return False

            if trie_node.get(word_keeper_key, False) and is_breakable(i + 1):
                return True

        return False

    return is_breakable(0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
