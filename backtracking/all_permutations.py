"""
本问题要求确定给定序列的
所有可能排列。使用回溯法（Backtracking）求解。

时间复杂度：O(n! * n)，
其中 n 表示给定序列的长度。
"""

from __future__ import annotations


def generate_all_permutations(sequence: list[int | str]) -> None:
    """
    生成并输出给定序列的所有可能排列。

    >>> generate_all_permutations([1, 2])
    [1, 2]
    [2, 1]
    >>> generate_all_permutations(["A", "B"])
    ['A', 'B']
    ['B', 'A']
    """
    create_state_space_tree(sequence, [], 0, [0 for i in range(len(sequence))])


def create_state_space_tree(
    sequence: list[int | str],
    current_sequence: list[int | str],
    index: int,
    index_used: list[int],
) -> None:
    """
    创建状态空间树，使用深度优先搜索（DFS）遍历各分支。
    每个状态恰有 len(sequence) - index 个子节点。
    到达给定序列末尾时终止。

    :param sequence: 待生成排列的输入序列。
    :param current_sequence: 正在构建的当前排列。
    :param index: 序列中的当前索引。
    :param index_used: 记录排列中已使用元素的列表。

    示例 1：
    >>> sequence = [1, 2, 3]
    >>> current_sequence = []
    >>> index_used = [False, False, False]
    >>> create_state_space_tree(sequence, current_sequence, 0, index_used)
    [1, 2, 3]
    [1, 3, 2]
    [2, 1, 3]
    [2, 3, 1]
    [3, 1, 2]
    [3, 2, 1]

    示例 2：
    >>> sequence = ["A", "B", "C"]
    >>> current_sequence = []
    >>> index_used = [False, False, False]
    >>> create_state_space_tree(sequence, current_sequence, 0, index_used)
    ['A', 'B', 'C']
    ['A', 'C', 'B']
    ['B', 'A', 'C']
    ['B', 'C', 'A']
    ['C', 'A', 'B']
    ['C', 'B', 'A']

    示例 3：
    >>> sequence = [1]
    >>> current_sequence = []
    >>> index_used = [False]
    >>> create_state_space_tree(sequence, current_sequence, 0, index_used)
    [1]
    """

    if index == len(sequence):
        print(current_sequence)
        return

    for i in range(len(sequence)):
        if not index_used[i]:
            current_sequence.append(sequence[i])
            index_used[i] = True
            create_state_space_tree(sequence, current_sequence, index + 1, index_used)
            current_sequence.pop()
            index_used[i] = False


"""
移除注释即可接收用户输入

print("Enter the elements")
sequence = list(map(int, input().split()))
"""

sequence: list[int | str] = [3, 1, 2, 4]
generate_all_permutations(sequence)

sequence_2: list[int | str] = ["A", "B", "C"]
generate_all_permutations(sequence_2)
