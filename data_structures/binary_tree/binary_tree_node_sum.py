"""
和 的 所有节点 在 二叉树。

Python 实现：
    O(n) 时间复杂度 - Recurses 通过 :meth:`depth_first_search`
                            带有 每个元素。
    O(n) 空间复杂度 - 在 任意 点 在 时间 最大值 数 的 栈
                            frames 该 could 为 在 memory 是 `n`
"""

from __future__ import annotations

from collections.abc import Iterator


class Node:
    """
    一个节点 具有 一个值 变量 并且 指针 到 节点 到 其 左 并且 右。
    """

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


class BinaryTreeNodeSum:
    r"""
    下方 树 看起来 类似 此
        10
       /  \
      5   -3
     /    / \
    12   8  0

    >>> tree = Node(10)
    >>> sum(BinaryTreeNodeSum(tree))
    10

    >>> tree.left = Node(5)
    >>> sum(BinaryTreeNodeSum(tree))
    15

    >>> tree.right = Node(-3)
    >>> sum(BinaryTreeNodeSum(tree))
    12

    >>> tree.left.left = Node(12)
    >>> sum(BinaryTreeNodeSum(tree))
    24

    >>> tree.right.left = Node(8)
    >>> tree.right.right = Node(0)
    >>> sum(BinaryTreeNodeSum(tree))
    32
    """

    def __init__(self, tree: Node) -> None:
        self.tree = tree

    def depth_first_search(self, node: Node | None) -> int:
        if node is None:
            return 0
        return node.value + (
            self.depth_first_search(node.left) + self.depth_first_search(node.right)
        )

    def __iter__(self) -> Iterator[int]:
        yield self.depth_first_search(self.tree)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
