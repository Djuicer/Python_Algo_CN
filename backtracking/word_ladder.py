"""
单词接龙（Word Ladder）是计算机科学中的经典问题。
要求每次只修改一个字母，
将起始单词转换为目标单词。
每个中间单词都必须属于给定的有效单词列表。
目标是找到从起始单词
到目标单词的转换序列。

Wikipedia: https://en.wikipedia.org/wiki/Word_ladder
"""

import string


def backtrack(
    current_word: str, path: list[str], end_word: str, word_set: set[str]
) -> list[str]:
    """
    使用回溯法寻找从 current_word 到 end_word
    的转换序列的辅助函数。

    参数：
    current_word (str): 转换序列中的当前单词。
    path (list[str]): 从 begin_word 到 current_word 的转换列表。
    end_word (str): 转换的目标单词。
    word_set (set[str]): 转换中可用的有效单词集合。

    返回：
    list[str]: 从 begin_word 到 end_word 的转换列表。
               若不存在从 current_word 到 end_word 的有效
                转换，则返回空列表。

    示例：
    >>> backtrack("hit", ["hit"], "cog", {"hot", "dot", "dog", "lot", "log", "cog"})
    ['hit', 'hot', 'dot', 'lot', 'log', 'cog']

    >>> backtrack("hit", ["hit"], "cog", {"hot", "dot", "dog", "lot", "log"})
    []

    >>> backtrack("lead", ["lead"], "gold", {"load", "goad", "gold", "lead", "lord"})
    ['lead', 'lead', 'load', 'goad', 'gold']

    >>> backtrack("game", ["game"], "code", {"came", "cage", "code", "cade", "gave"})
    ['game', 'came', 'cade', 'code']
    """

    # 递归终止条件：当前单词为目标单词时，返回路径
    if current_word == end_word:
        return path

    # 尝试所有可能的单字母转换
    for i in range(len(current_word)):
        for c in string.ascii_lowercase:  # 尝试修改每个字母
            transformed_word = current_word[:i] + c + current_word[i + 1 :]
            if transformed_word in word_set:
                word_set.remove(transformed_word)
                # 将新单词加入路径并递归
                result = backtrack(
                    transformed_word, [*path, transformed_word], end_word, word_set
                )
                if result:  # 找到有效转换
                    return result
                word_set.add(transformed_word)  # 回溯

    return []  # 未找到有效转换


def word_ladder(begin_word: str, end_word: str, word_set: set[str]) -> list[str]:
    """
    使用回溯法求解单词接龙问题，返回
    从 begin_word 到 end_word 的转换列表。

    参数：
    begin_word (str): 转换开始的单词。
    end_word (str): 转换的目标单词。
    word_list (list[str]): 转换中可用的有效单词列表。

    返回：
    list[str]: 从 begin_word 到 end_word 的转换列表。
               若不存在有效转换，则返回空列表。

    示例：
    >>> word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
    ['hit', 'hot', 'dot', 'lot', 'log', 'cog']

    >>> word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"])
    []

    >>> word_ladder("lead", "gold", ["load", "goad", "gold", "lead", "lord"])
    ['lead', 'lead', 'load', 'goad', 'gold']

    >>> word_ladder("game", "code", ["came", "cage", "code", "cade", "gave"])
    ['game', 'came', 'cade', 'code']
    """

    if end_word not in word_set:  # 不存在有效转换
        return []

    # 从 begin_word 开始进行回溯搜索
    return backtrack(begin_word, [begin_word], end_word, word_set)
