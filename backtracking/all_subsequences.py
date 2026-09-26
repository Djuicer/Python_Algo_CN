"""
本问题要求确定给定序列的
所有可能子序列。使用回溯法（Backtracking）求解。

时间复杂度：O(2^n)，
其中 n 表示给定序列的长度。
"""

from __future__ import annotations

from typing import Any


def generate_all_subsequences(sequence: list[Any]) -> None:
    """
    生成并输出给定序列的所有可能子序列。

    >>> generate_all_subsequences([1, 2])
    []
    [2]
    [1]
    [1, 2]
    >>> generate_all_subsequences(["A", "B"])
    []
    ['B']
    ['A']
    ['A', 'B']
    """

    create_state_space_tree(sequence, [], 0)


def create_state_space_tree(
    sequence: list[Any], current_subsequence: list[Any], index: int
) -> None:
    """
    创建状态空间树，使用深度优先搜索（DFS）遍历各分支。
    每个状态恰有两个子节点。
    到达给定序列末尾时终止。

    :param sequence: 待生成子序列的输入序列。
    :param current_subsequence: 正在构建的当前子序列。
    :param index: 序列中的当前索引。

    示例：
    >>> sequence = [3, 2, 1]
    >>> current_subsequence = []
    >>> create_state_space_tree(sequence, current_subsequence, 0)
    []
    [1]
    [2]
    [2, 1]
    [3]
    [3, 1]
    [3, 2]
    [3, 2, 1]

    >>> sequence = ["A", "B"]
    >>> current_subsequence = []
    >>> create_state_space_tree(sequence, current_subsequence, 0)
    []
    ['B']
    ['A']
    ['A', 'B']

    >>> sequence = []
    >>> current_subsequence = []
    >>> create_state_space_tree(sequence, current_subsequence, 0)
    []

    >>> sequence = [1, 2, 3, 4]
    >>> current_subsequence = []
    >>> create_state_space_tree(sequence, current_subsequence, 0)
    []
    [4]
    [3]
    [3, 4]
    [2]
    [2, 4]
    [2, 3]
    [2, 3, 4]
    [1]
    [1, 4]
    [1, 3]
    [1, 3, 4]
    [1, 2]
    [1, 2, 4]
    [1, 2, 3]
    [1, 2, 3, 4]
    """

    if index == len(sequence):
        print(current_subsequence)
        return

    create_state_space_tree(sequence, current_subsequence, index + 1)
    current_subsequence.append(sequence[index])
    create_state_space_tree(sequence, current_subsequence, index + 1)
    current_subsequence.pop()


if __name__ == "__main__":
    seq: list[Any] = [1, 2, 3]
    generate_all_subsequences(seq)

    seq.clear()
    seq.extend(["A", "B", "C"])
    generate_all_subsequences(seq)
