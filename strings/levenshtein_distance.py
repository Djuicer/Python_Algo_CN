from collections.abc import Callable


def levenshtein_distance(first_word: str, second_word: str) -> int:
    """
    莱文斯坦距离（Levenshtein Distance）的 Python 实现。
    :param first_word: 第一个待度量差异的单词。
    :param second_word: 第二个待度量差异的单词。
    :return: 两个单词之间的莱文斯坦距离。
    示例：
    >>> levenshtein_distance("planet", "planetary")
    3
    >>> levenshtein_distance("", "test")
    4
    >>> levenshtein_distance("book", "back")
    2
    >>> levenshtein_distance("book", "book")
    0
    >>> levenshtein_distance("test", "")
    4
    >>> levenshtein_distance("", "")
    0
    >>> levenshtein_distance("orchestration", "container")
    10
    """
    # 较长的单词应放在前面
    if len(first_word) < len(second_word):
        return levenshtein_distance(second_word, first_word)

    if len(second_word) == 0:
        return len(first_word)

    previous_row = list(range(len(second_word) + 1))

    for i, c1 in enumerate(first_word):
        current_row = [i + 1]

        for j, c2 in enumerate(second_word):
            # 计算插入、删除和替换的代价
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            # 取最小值并追加到当前行
            current_row.append(min(insertions, deletions, substitutions))

        # 保存上一行
        previous_row = current_row

    # 返回最后一个元素（距离）
    return previous_row[-1]


def levenshtein_distance_optimized(first_word: str, second_word: str) -> int:
    """
    计算两个单词（字符串）之间的莱文斯坦距离。
    通过原地修改各行提高效率。
    :param first_word: 第一个待度量差异的单词。
    :param second_word: 第二个待度量差异的单词。
    :return: 两个单词之间的莱文斯坦距离。
    示例：
    >>> levenshtein_distance_optimized("planet", "planetary")
    3
    >>> levenshtein_distance_optimized("", "test")
    4
    >>> levenshtein_distance_optimized("book", "back")
    2
    >>> levenshtein_distance_optimized("book", "book")
    0
    >>> levenshtein_distance_optimized("test", "")
    4
    >>> levenshtein_distance_optimized("", "")
    0
    >>> levenshtein_distance_optimized("orchestration", "container")
    10
    """
    if len(first_word) < len(second_word):
        return levenshtein_distance_optimized(second_word, first_word)

    if len(second_word) == 0:
        return len(first_word)

    previous_row = list(range(len(second_word) + 1))

    for i, c1 in enumerate(first_word):
        current_row = [i + 1] + [0] * len(second_word)

        for j, c2 in enumerate(second_word):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row[j + 1] = min(insertions, deletions, substitutions)

        previous_row = current_row

    return previous_row[-1]


def benchmark_levenshtein_distance(func: Callable) -> None:
    """
    对莱文斯坦距离函数进行基准测试。
    :param str: 被测函数的名称。
    :param func: 被测函数。
    """
    from timeit import timeit

    stmt = f"{func.__name__}('sitting', 'kitten')"
    setup = f"from __main__ import {func.__name__}"
    number = 25_000
    result = timeit(stmt=stmt, setup=setup, number=number)
    print(f"{func.__name__:<30} finished {number:,} runs in {result:.5f} seconds")


if __name__ == "__main__":
    # 获取用户输入的单词
    first_word = input("Enter the first word for Levenshtein distance:\n").strip()
    second_word = input("Enter the second word for Levenshtein distance:\n").strip()

    # 计算并输出莱文斯坦距离
    print(f"{levenshtein_distance(first_word, second_word) = }")
    print(f"{levenshtein_distance_optimized(first_word, second_word) = }")

    # 对莱文斯坦距离函数进行基准测试
    benchmark_levenshtein_distance(levenshtein_distance)
    benchmark_levenshtein_distance(levenshtein_distance_optimized)
