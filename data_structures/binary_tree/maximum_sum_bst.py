from __future__ import annotations

import sys
from dataclasses import dataclass

INT_MIN = -sys.maxsize + 1
INT_MAX = sys.maxsize - 1


@dataclass
class TreeNode:
    val: int = 0
    left: TreeNode | None = None
    right: TreeNode | None = None


def max_sum_bst(root: TreeNode | None) -> int:
    """
    解 traverses 二叉树 到 查找 最大值 和 的
    键 在 任意 子树 该 是 二叉搜索树 (BST). 它 使用
    recursion 到 validate BST properties 并且 calculates sums，returning
    最高 和 找到 among 所有 有效 BST 子树。

    >>> t1 = TreeNode(4)
    >>> t1.left = TreeNode(3)
    >>> t1.left.left = TreeNode(1)
    >>> t1.left.right = TreeNode(2)
    >>> print(max_sum_bst(t1))
    2
    >>> t2 = TreeNode(-4)
    >>> t2.left = TreeNode(-2)
    >>> t2.right = TreeNode(-5)
    >>> print(max_sum_bst(t2))
    0
    >>> t3 = TreeNode(1)
    >>> t3.left = TreeNode(4)
    >>> t3.left.left = TreeNode(2)
    >>> t3.left.right = TreeNode(4)
    >>> t3.right = TreeNode(3)
    >>> t3.right.left = TreeNode(2)
    >>> t3.right.right = TreeNode(5)
    >>> t3.right.right.left = TreeNode(4)
    >>> t3.right.right.right = TreeNode(6)
    >>> print(max_sum_bst(t3))
    20
    """
    ans: int = 0

    def solver(node: TreeNode | None) -> tuple[bool, int, int, int]:
        """
        返回值 最大值 和 通过 making 递归 calls
        >>> t1 = TreeNode(1)
        >>> print(solver(t1))
        1
        """
        nonlocal ans

        if not node:
            return True, INT_MAX, INT_MIN, 0  # 有效 BST，最小值，最大值，和

        is_left_valid, min_left, max_left, sum_left = solver(node.left)
        is_right_valid, min_right, max_right, sum_right = solver(node.right)

        if is_left_valid and is_right_valid and max_left < node.val < min_right:
            total_sum = sum_left + sum_right + node.val
            ans = max(ans, total_sum)
            return True, min(min_left, node.val), max(max_right, node.val), total_sum

        return False, -1, -1, -1  # 不 有效 BST

    solver(root)
    return ans


if __name__ == "__main__":
    import doctest

    doctest.testmod()
