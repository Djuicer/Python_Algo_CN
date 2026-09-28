"""
给定 根节点 的 二叉树，检查 是否 它 是 镜像 的 自身
(i.e., symmetric around its center).

Leetcode reference: https://leetcode.com/problems/symmetric-tree/
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    """
    一个节点 表示 元素 的 二叉树，其 包含：

    属性：
    数据: 该值 存储 在 该节点 (int)。
    左: 指针 到 左 子节点 (节点 或 None)。
    右: 指针 到 右子节点 节点 (节点 或 None)。

    示例：
    >>> node = Node(1, Node(2), Node(3))
    >>> node.data
    1
    >>> node.left.data
    2
    >>> node.right.data
    3
    """

    data: int
    left: Node | None = None
    right: Node | None = None


def make_symmetric_tree() -> Node:
    r"""
    创建一个 对称 树 用于 testing。

    该树 看起来 类似 此：
           1
         /   \
        2     2
      / \    / \
     3   4   4  3

    返回值：
    节点: 根节点 的 对称 树。

    示例：
    >>> tree = make_symmetric_tree()
    >>> tree.data
    1
    >>> tree.left.data == tree.right.data
    True
    >>> tree.left.left.data == tree.right.right.data
    True
    """
    root = Node(1)
    root.left = Node(2)
    root.right = Node(2)
    root.left.left = Node(3)
    root.left.right = Node(4)
    root.right.left = Node(4)
    root.right.right = Node(3)
    return root


def make_asymmetric_tree() -> Node:
    r"""
    创建一个 asymmetric 树 用于 testing。

    该树 看起来 类似 此：
           1
         /   \
        2     2
      / \    / \
     3   4   3  4

    返回值：
    节点: 根节点 的 asymmetric 树。

    示例：
    >>> tree = make_asymmetric_tree()
    >>> tree.data
    1
    >>> tree.left.data == tree.right.data
    True
    >>> tree.left.left.data == tree.right.right.data
    False
    """
    root = Node(1)
    root.left = Node(2)
    root.right = Node(2)
    root.left.left = Node(3)
    root.left.right = Node(4)
    root.right.left = Node(3)
    root.right.right = Node(4)
    return root


def is_symmetric_tree(tree: Node) -> bool:
    """
    检查是否 二叉树 是 对称 (i.e.，镜像 的 自身)。

    参数：
    树: 根节点 的 二叉树。

    返回值：
    bool: True 如果 该树 是 对称，False 否则。

    示例：
    >>> is_symmetric_tree(make_symmetric_tree())
    True
    >>> is_symmetric_tree(make_asymmetric_tree())
    False
    """
    if tree:
        return is_mirror(tree.left, tree.right)
    return True  # 空树 是 considered 对称。


def is_mirror(left: Node | None, right: Node | None) -> bool:
    """
    检查是否 两个 子树 是 镜像 images 的 每个 另一个。

    参数：
    左: 根节点 的 左子树。
    右: 根节点 的 右子树。

    返回值：
    bool: True 如果 两个 子树 是 mirrors 的 每个 另一个，False 否则。

    示例：
    >>> tree1 = make_symmetric_tree()
    >>> is_mirror(tree1.left, tree1.right)
    True
    >>> tree2 = make_asymmetric_tree()
    >>> is_mirror(tree2.left, tree2.right)
    False
    """
    if left is None and right is None:
        # 两者 sides 是 空，其 是 对称。
        return True
    if left is None or right is None:
        # 一个 一侧 为空 当 另一个 是 不，其 是 不 对称。
        return False
    if left.data == right.data:
        # 值 match，因此 检查 子树 递归地。
        return is_mirror(left.left, right.right) and is_mirror(left.right, right.left)
    return False


if __name__ == "__main__":
    from doctest import testmod

    testmod()
