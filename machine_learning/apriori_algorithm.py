"""
Apriori 算法是一种关联规则挖掘技术，也称为购物篮分析，旨在发现事务型
或关系型数据库中一组项目之间值得关注的关系或关联。

例如，Apriori 算法可以得到如下规则：“如果顾客购买了商品 A 和商品 B，
那么他们很可能也会购买商品 C。”该规则表明商品 A、B、C 之间存在关联，
即购买 A 和 B 的顾客更有可能同时购买 C。

WIKI: https://en.wikipedia.org/wiki/Apriori_algorithm
示例： https://www.kaggle.com/code/earthian/apriori-association-rules-mining
"""

from collections import Counter
from itertools import combinations


def load_data() -> list[list[str]]:
    """
    返回一个事务数据集示例。

    >>> load_data()
    [['milk'], ['milk', 'butter'], ['milk', 'bread'], ['milk', 'bread', 'chips']]
    """
    return [["milk"], ["milk", "butter"], ["milk", "bread"], ["milk", "bread", "chips"]]


def prune(itemset: list, candidates: list, length: int) -> list:
    """
    剪除非频繁候选项集。
    剪枝的目的是过滤掉非频繁候选项集。具体做法是检查候选项集的所有
    (k-1) 子集是否都出现在上一轮的频繁项集中（即上一轮频繁项集的有效子序列）。

    剪除非频繁候选项集。

    >>> itemset = ['X', 'Y', 'Z']
    >>> candidates = [['X', 'Y'], ['X', 'Z'], ['Y', 'Z']]
    >>> prune(itemset, candidates, 2)
    [['X', 'Y'], ['X', 'Z'], ['Y', 'Z']]

    >>> itemset = ['1', '2', '3', '4']
    >>> candidates = ['1', '2', '4']
    >>> prune(itemset, candidates, 3)
    []
    """
    itemset_counter = Counter(tuple(item) for item in itemset)
    pruned = []
    for candidate in candidates:
        is_subsequence = True
        for item in candidate:
            item_tuple = tuple(item)
            if (
                item_tuple not in itemset_counter
                or itemset_counter[item_tuple] < length - 1
            ):
                is_subsequence = False
                break
        if is_subsequence:
            pruned.append(candidate)
    return pruned


def apriori(data: list[list[str]], min_support: int) -> list[tuple[list[str], int]]:
    """
    返回频繁项集及其支持度计数的列表。

    >>> data = [['A', 'B', 'C'], ['A', 'B'], ['A', 'C'], ['A', 'D'], ['B', 'C']]
    >>> apriori(data, 2)
    [(['A', 'B'], 1), (['A', 'C'], 2), (['B', 'C'], 2)]

    >>> data = [['1', '2', '3'], ['1', '2'], ['1', '3'], ['1', '4'], ['2', '3']]
    >>> apriori(data, 3)
    []
    """
    itemset = [list(transaction) for transaction in data]
    frequent_itemsets = []
    length = 1

    while itemset:
            # 统计项集的支持度
        counts = [0] * len(itemset)
        for transaction in data:
            for j, candidate in enumerate(itemset):
                if all(item in transaction for item in candidate):
                    counts[j] += 1

        # 剪除非频繁项集
        itemset = [item for i, item in enumerate(itemset) if counts[i] >= min_support]

        # 追加频繁项集（使用列表以保持顺序）
        for i, item in enumerate(itemset):
            frequent_itemsets.append((sorted(item), counts[i]))

        length += 1
        itemset = prune(itemset, list(combinations(itemset, length)), length)

    return frequent_itemsets


if __name__ == "__main__":
    """
    Apriori algorithm for finding frequent itemsets.

    参数：
        data: A list of transactions, where each transaction is a list of items.
        min_support: The minimum support threshold for frequent itemsets.

    返回：
        A list of frequent itemsets along with their support counts.
    """
    import doctest

    doctest.testmod()

    # 用户定义的阈值或最小支持度
    frequent_itemsets = apriori(data=load_data(), min_support=2)
    print("\n".join(f"{itemset}: {support}" for itemset, support in frequent_itemsets))
