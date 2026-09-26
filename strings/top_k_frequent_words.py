"""
找出给定单词列表中出现频次最高的 K 个单词。

展示如何使用本仓库中已有的 Heap 类
解决此问题。
计算顺序统计量是堆的一种典型用途。

此实现主要用于教学，实际上使用 Python 标准库中的
collections.Counter，仅需几行代码即可求解：

from collections import Counter
def top_k_frequent_words(words, k_value):
    return [x[0] for x in Counter(words).most_common(k_value)]
"""

from collections import Counter
from functools import total_ordering

from data_structures.heap.heap import Heap


@total_ordering
class WordCount:
    def __init__(self, word: str, count: int) -> None:
        self.word = word
        self.count = count

    def __eq__(self, other: object) -> bool:
        """
        >>> WordCount('a', 1).__eq__(WordCount('b', 1))
        True
        >>> WordCount('a', 1).__eq__(WordCount('a', 1))
        True
        >>> WordCount('a', 1).__eq__(WordCount('a', 2))
        False
        >>> WordCount('a', 1).__eq__(WordCount('b', 2))
        False
        >>> WordCount('a', 1).__eq__(1)
        NotImplemented
        """
        if not isinstance(other, WordCount):
            return NotImplemented
        return self.count == other.count

    def __lt__(self, other: object) -> bool:
        """
        >>> WordCount('a', 1).__lt__(WordCount('b', 1))
        False
        >>> WordCount('a', 1).__lt__(WordCount('a', 1))
        False
        >>> WordCount('a', 1).__lt__(WordCount('a', 2))
        True
        >>> WordCount('a', 1).__lt__(WordCount('b', 2))
        True
        >>> WordCount('a', 2).__lt__(WordCount('a', 1))
        False
        >>> WordCount('a', 2).__lt__(WordCount('b', 1))
        False
        >>> WordCount('a', 1).__lt__(1)
        NotImplemented
        """
        if not isinstance(other, WordCount):
            return NotImplemented
        return self.count < other.count


def top_k_frequent_words(words: list[str], k_value: int) -> list[str]:
    """
    返回出现频次最高的 `k_value` 个单词，
    按频次的非递增顺序排列。
    这里将给定列表中的每个元素视为一个单词。

    若 `k_value` 大于不同单词的数量，则使用
    不同单词的数量作为 k 值。

    >>> top_k_frequent_words(['a', 'b', 'c', 'a', 'c', 'c'], 3)
    ['c', 'a', 'b']
    >>> top_k_frequent_words(['a', 'b', 'c', 'a', 'c', 'c'], 2)
    ['c', 'a']
    >>> top_k_frequent_words(['a', 'b', 'c', 'a', 'c', 'c'], 1)
    ['c']
    >>> top_k_frequent_words(['a', 'b', 'c', 'a', 'c', 'c'], 0)
    []
    >>> top_k_frequent_words([], 1)
    []
    >>> top_k_frequent_words(['a', 'a'], 2)
    ['a']
    """
    heap: Heap[WordCount] = Heap()
    count_by_word = Counter(words)
    heap.build_max_heap(
        [WordCount(word, count) for word, count in count_by_word.items()]
    )
    return [heap.extract_max().word for _ in range(min(k_value, len(count_by_word)))]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
