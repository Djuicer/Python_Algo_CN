"""
极小极大算法（Minimax）通过检查所有可能的走法，帮助在游戏中获得最大得分
depth 是博弈树的当前深度。

nodeIndex 是当前节点在 scores[] 中的索引。
若轮到最大化方行动，则返回 true，否则返回 false
博弈树的叶节点存储在 scores[] 中
height 是博弈树的最大高度
"""

from __future__ import annotations

import math


def minimax(
    depth: int, node_index: int, is_max: bool, scores: list[int], height: float
) -> int:
    """
    实现极小极大算法，通过检查所有可能的走法，
    帮助双人游戏中的玩家获得最优得分。
    若玩家是最大化方，则最大化得分。
    若玩家是最小化方，则最小化得分。

    Parameters:
    - depth: 博弈树的当前深度。
    - node_index: 当前节点在 scores 列表中的索引。
    - is_max: 布尔值，表示当前轮次属于
              最大化方（True）还是最小化方（False）。
    - scores: 包含博弈树叶节点得分的列表。
    - height: 博弈树的最大高度。

    Returns:
    - 表示当前玩家最优得分的整数。

    >>> import math
    >>> scores = [90, 23, 6, 33, 21, 65, 123, 34423]
    >>> height = math.log(len(scores), 2)
    >>> minimax(0, 0, True, scores, height)
    65
    >>> minimax(-1, 0, True, scores, height)
    Traceback (most recent call last):
        ...
    ValueError: Depth cannot be less than 0
    >>> minimax(0, 0, True, [], 2)
    Traceback (most recent call last):
        ...
    ValueError: Scores cannot be empty
    >>> minimax(0, 0, True, [1, 2, 3], 2)
    Traceback (most recent call last):
        ...
    ValueError: Number of scores must be a power of 2
    >>> scores = [3, 5, 2, 9, 12, 5, 23, 23]
    >>> height = math.log(len(scores), 2)
    >>> minimax(0, 0, True, scores, height)
    12
    """

    if depth < 0:
        raise ValueError("Depth cannot be less than 0")
    if len(scores) == 0:
        raise ValueError("Scores cannot be empty")
    if len(scores) & (len(scores) - 1) != 0:
        raise ValueError("Number of scores must be a power of 2")

    # 递归终止条件：当前深度等于树高时，
    # 返回当前节点的得分。
    if depth == height:
        return scores[node_index]

    # 若轮到最大化方，则从两种可能的走法中
    # 选择最大得分。
    if is_max:
        return max(
            minimax(depth + 1, node_index * 2, False, scores, height),
            minimax(depth + 1, node_index * 2 + 1, False, scores, height),
        )

    # 若轮到最小化方，则从两种可能的走法中
    # 选择最小得分。
    return min(
        minimax(depth + 1, node_index * 2, True, scores, height),
        minimax(depth + 1, node_index * 2 + 1, True, scores, height),
    )


def main() -> None:
    # 示例得分和树高计算
    scores = [90, 23, 6, 33, 21, 65, 123, 34423]
    height = math.log(len(scores), 2)

    # 使用极小极大算法计算并输出最优值
    print("Optimal value : ", end="")
    print(minimax(0, 0, True, scores, height))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
