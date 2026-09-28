"""
给定 根节点 的 二叉树 并且 整数 target,
查找 数 的 paths 其中 和 的 值
along 路径 equals target。


Leetcode reference: https://leetcode.com/problems/path-sum-iii/
"""

from __future__ import annotations


class Node:
    """
    一个节点 具有 值 变量 并且 指针 到 节点 到 其 左 并且 右。
    """

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


class BinaryTreePathSum:
    r"""
    下方 树 看起来 类似 此
          10
         /  \
        5   -3
       / \    \
      3   2    11
     / \   \
    3  -2   1


    >>> tree = Node(10)
    >>> tree.left = Node(5)
    >>> tree.right = Node(-3)
    >>> tree.left.left = Node(3)
    >>> tree.left.right = Node(2)
    >>> tree.right.right = Node(11)
    >>> tree.left.left.left = Node(3)
    >>> tree.left.left.right = Node(-2)
    >>> tree.left.right.right = Node(1)

    >>> BinaryTreePathSum().path_sum(tree, 8)
    3
    >>> BinaryTreePathSum().path_sum(tree, 7)
    2
    >>> tree.right.right = Node(10)
    >>> BinaryTreePathSum().path_sum(tree, 8)
    2
    >>> BinaryTreePathSum().path_sum(None, 0)
    0
    >>> BinaryTreePathSum().path_sum(tree, 0)
    0

    第二个 树 看起来 类似 此
          0
         / \
        5   5

    >>> tree2 = Node(0)
    >>> tree2.left = Node(5)
    >>> tree2.right = Node(5)

    >>> BinaryTreePathSum().path_sum(tree2, 5)
    4
    >>> BinaryTreePathSum().path_sum(tree2, -1)
    0
    >>> BinaryTreePathSum().path_sum(tree2, 0)
    1
    """

    target: int

    def __init__(self) -> None:
        self.paths = 0

    def depth_first_search(self, node: Node | None, path_sum: int) -> None:
        if node is None:
            return

        if path_sum == self.target:
            self.paths += 1

        if node.left:
            self.depth_first_search(node.left, path_sum + node.left.value)
        if node.right:
            self.depth_first_search(node.right, path_sum + node.right.value)

    def path_sum(self, node: Node | None, target: int | None = None) -> int:
        if node is None:
            return 0
        if target is not None:
            self.target = target

        self.depth_first_search(node, node.value)
        self.path_sum(node.left)
        self.path_sum(node.right)

        return self.paths


if __name__ == "__main__":
    import doctest

    doctest.testmod()
