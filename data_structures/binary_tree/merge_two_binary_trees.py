#!/usr/local/bin/python3
"""
Problem Description: 给定 两个 二叉树，返回 合并后 树。
rule 用于 merging 是 该 如果 两个 节点 overlap，则 put 该值 和 的
两者 节点 到 新 值 的 合并后 节点. 否则，不 null 节点
将 为 使用 作为 该节点 的 新 树。
"""

from __future__ import annotations


class Node:
    """
    binary 节点 具有 值 变量 并且 指针 到 其 左 并且 右 节点。
    """

    def __init__(self, value: int = 0) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


def merge_two_binary_trees(tree1: Node | None, tree2: Node | None) -> Node | None:
    """
    返回值 根节点 的 合并后 树。

    >>> tree1 = Node(5)
    >>> tree1.left = Node(6)
    >>> tree1.right = Node(7)
    >>> tree1.left.left = Node(2)
    >>> tree2 = Node(4)
    >>> tree2.left = Node(5)
    >>> tree2.right = Node(8)
    >>> tree2.left.right = Node(1)
    >>> tree2.right.right = Node(4)
    >>> merged_tree = merge_two_binary_trees(tree1, tree2)
    >>> print_preorder(merged_tree)
    9
    11
    2
    1
    15
    4
    """
    if tree1 is None:
        return tree2
    if tree2 is None:
        return tree1

    tree1.value = tree1.value + tree2.value
    tree1.left = merge_two_binary_trees(tree1.left, tree2.left)
    tree1.right = merge_two_binary_trees(tree1.right, tree2.right)
    return tree1


def print_preorder(root: Node | None) -> None:
    """
    打印 前序遍历 的 该树。

    >>> root = Node(1)
    >>> root.left = Node(2)
    >>> root.right = Node(3)
    >>> print_preorder(root)
    1
    2
    3
    >>> print_preorder(root.right)
    3
    """
    if root:
        print(root.value)
        print_preorder(root.left)
        print_preorder(root.right)


if __name__ == "__main__":
    tree1 = Node(1)
    tree1.left = Node(2)
    tree1.right = Node(3)
    tree1.left.left = Node(4)

    tree2 = Node(2)
    tree2.left = Node(4)
    tree2.right = Node(6)
    tree2.left.right = Node(9)
    tree2.right.right = Node(5)

    print("Tree1 is: ")
    print_preorder(tree1)
    print("Tree2 is: ")
    print_preorder(tree2)
    merged_tree = merge_two_binary_trees(tree1, tree2)
    print("Merged Tree is: ")
    print_preorder(merged_tree)
