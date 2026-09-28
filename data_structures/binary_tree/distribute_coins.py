"""
Author  : Alexander Pantyukhin
Date    : November 7, 2022

Task:
You 是 给定 树 根节点 的 二叉树 带有 n 节点，其中 每个节点 具有
节点.数据 coins. 其中 是 exactly n coins 在 whole 树。

在 一个 移动，我们 may choose 两个 adjacent 节点 并且 移动 一个 coin 从 一个 节点
到 另一个. 移动 may 为 从 父节点 到 子节点，或 从 子节点 到 父节点。

返回 最小值 数 的 移动 所需 到 使 每个 节点 具有 exactly 一个 coin。

示例 1：

   3
  / \
 0   0

结果: 2

示例 2：

   0
  / \
 3   0

结果 3

leetcode: https://leetcode.com/problems/distribute-coins-in-binary-tree/

实现 notes：
User 深度-第一个 搜索 方法。

Let n 是 节点数量 在 树
运行时间: O(n)
空间: O(1)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class TreeNode:
    data: int
    left: TreeNode | None = None
    right: TreeNode | None = None


class CoinsDistribResult(NamedTuple):
    moves: int
    excess: int


def distribute_coins(root: TreeNode | None) -> int:
    """
    >>> distribute_coins(TreeNode(3, TreeNode(0), TreeNode(0)))
    2
    >>> distribute_coins(TreeNode(0, TreeNode(3), TreeNode(0)))
    3
    >>> distribute_coins(TreeNode(0, TreeNode(0), TreeNode(3)))
    3
    >>> distribute_coins(None)
    0
    >>> distribute_coins(TreeNode(0, TreeNode(0), TreeNode(0)))
    Traceback (most recent call last):
     ...
    ValueError: The nodes number should be same as the number of coins
    >>> distribute_coins(TreeNode(0, TreeNode(1), TreeNode(1)))
    Traceback (most recent call last):
     ...
    ValueError: The nodes number should be same as the number of coins
    """

    if root is None:
        return 0

    # 验证
    def count_nodes(node: TreeNode | None) -> int:
        """
        >>> count_nodes(None)
        0
        """
        if node is None:
            return 0

        return count_nodes(node.left) + count_nodes(node.right) + 1

    def count_coins(node: TreeNode | None) -> int:
        """
        >>> count_coins(None)
        0
        """
        if node is None:
            return 0

        return count_coins(node.left) + count_coins(node.right) + node.data

    if count_nodes(root) != count_coins(root):
        raise ValueError("The nodes number should be same as the number of coins")

    # 主要计算
    def get_distrib(node: TreeNode | None) -> CoinsDistribResult:
        """
        >>> get_distrib(None)
        namedtuple("CoinsDistribResult", "0 2")
        """

        if node is None:
            return CoinsDistribResult(0, 1)

        left_distrib_moves, left_distrib_excess = get_distrib(node.left)
        right_distrib_moves, right_distrib_excess = get_distrib(node.right)

        coins_to_left = 1 - left_distrib_excess
        coins_to_right = 1 - right_distrib_excess

        result_moves = (
            left_distrib_moves
            + right_distrib_moves
            + abs(coins_to_left)
            + abs(coins_to_right)
        )
        result_excess = node.data - coins_to_left - coins_to_right

        return CoinsDistribResult(result_moves, result_excess)

    return get_distrib(root)[0]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
