from __future__ import annotations

from dataclasses import dataclass


# Leetcode Reference : https://leetcode.com/problems/binary-tree-maximum-path-sum/
@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


class GetMaxPathSum:
    r"""

    GetMaxPathSum takes 根节点 的 树 作为 初始 argument。
    Upon calling max_path_sum()，它 返回值 最大值 路径
    和 从 该树。

    # 测试

    下方 树 看起来 类似 此
          10
         /  \
        5   -3
       / \    \
      3   2    11
     / \   \
    3  -2   1

    结果 将 为 计算得出 类似 : 3 -> 3 -> 5 -> 10 -> -3 -> 11
    作为 它 是 最大值 路径 可能。


    >>> root = TreeNode(10)
    >>> root.left = TreeNode(5)
    >>> root.right = TreeNode(-3)
    >>> root.left.left = TreeNode(3)
    >>> root.left.right = TreeNode(2)
    >>> root.right.right = TreeNode(11)
    >>> root.left.left.left = TreeNode(3)
    >>> root.left.left.right = TreeNode(-2)
    >>> root.left.right.right = TreeNode(1)

    >>> GetMaxPathSum(root).max_path_sum()
    29
    """

    def __init__(self, root: TreeNode) -> None:
        self.sum = -9999999999
        self.root = root

    def traverse(self, root: TreeNode | None) -> int:
        """
        返回值 最大值 路径 和 通过 递归地 taking max_path_sum 从 左
        并且 max_path_sum 从 右 如果 当前节点 具有 左 或 右 节点。

        :param 根节点 -> 树 根节点：
        :返回 int：
        """

        if root is None:
            return 0

        right_sum = max(self.traverse(root.right), 0)
        left_sum = max(self.traverse(root.left), 0)

        val = root.val + right_sum + left_sum
        self.sum = max(val, self.sum)

        return root.val + max(right_sum, left_sum)

    def max_path_sum(self) -> int:
        """
        Driver 方法 到 获取 max_path_sum 通过 calling 遍历 方法。
        :返回 max_path_sum：
        """
        self.traverse(self.root)
        return self.sum


def construct_tree() -> TreeNode:
    r"""
    下方 树
       -10
       / \
      9   20
         /  \
       15    7

    >>> root = TreeNode(-10)
    >>> root.left = TreeNode(9)
    >>> root.right = TreeNode(20)
    >>> root.right.left = TreeNode(15)
    >>> root.right.right = TreeNode(7)

    >>> GetMaxPathSum(construct_tree()).max_path_sum()
    42
    """

    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    return root


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    tree = GetMaxPathSum(construct_tree())
    print(f"{tree.max_path_sum() = }")
