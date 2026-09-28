"""
二叉树 Flattening 算法

此 代码 defines 算法 到 flatten 二叉树 到 链表
表示 使用 右 指针 的树 节点. 它 使用 在-位置
flattening 并且 demonstrates flattening process along 带有 显示
函数 到 visualize flattened 链表。
https://www.geeksforgeeks.org/flatten-a-binary-tree-into-linked-list

Author: Arunkumar A
Date: 04/09/2023
"""

from __future__ import annotations


class TreeNode:
    """
    TreeNode 具有 数据 变量 并且 指针 到 TreeNode objects
    用于 其 左 并且 右 子节点。
    """

    def __init__(self, data: int) -> None:
        self.data = data
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


def build_tree() -> TreeNode:
    """
    构建 并且 返回 sample 二叉树。

    返回值：
        TreeNode: 根节点 的 二叉树。

    示例：
        >>> root = build_tree()
        >>> root.data
        1
        >>> root.left.data
        2
        >>> root.right.data
        5
        >>> root.left.left.data
        3
        >>> root.left.right.data
        4
        >>> root.right.right.data
        6
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(5)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(6)
    return root


def flatten(root: TreeNode | None) -> None:
    """
    Flatten 二叉树 到 链表 在-位置，其中 链表 是
    表示 使用 右 指针 的树 节点。

    参数：
        根节点 (TreeNode): 根节点 的 二叉树 到 为 flattened。

    示例：
        >>> root = TreeNode(1)
        >>> root.left = TreeNode(2)
        >>> root.right = TreeNode(5)
        >>> root.left.left = TreeNode(3)
        >>> root.left.right = TreeNode(4)
        >>> root.right.right = TreeNode(6)
        >>> flatten(root)
        >>> root.data
        1
        >>> root.right.right is None
        False
        >>> root.right.right = TreeNode(3)
        >>> root.right.right.right is None
        True
    """
    if not root:
        return

    # Flatten 左子树
    flatten(root.left)

    # Save 右子树
    right_subtree = root.right

    # 使 左子树 新 右子树
    root.right = root.left
    root.left = None

    # 查找 末尾 的 新 右子树
    current = root
    while current.right:
        current = current.right

    # 追加 原始 右子树 到 末尾
    current.right = right_subtree

    # Flatten updated 右子树
    flatten(right_subtree)


def display_linked_list(root: TreeNode | None) -> None:
    """
    显示 flattened 链表。

    参数：
        根节点 (TreeNode | None): 根节点 的 flattened 链表。

    示例：
        >>> root = TreeNode(1)
        >>> root.right = TreeNode(2)
        >>> root.right.right = TreeNode(3)
        >>> display_linked_list(root)
        1 2 3
        >>> root = None
        >>> display_linked_list(root)

    """
    current = root
    while current:
        if current.right is None:
            print(current.data, end="")
            break
        print(current.data, end=" ")
        current = current.right


if __name__ == "__main__":
    print("Flattened Linked List:")
    root = build_tree()
    flatten(root)
    display_linked_list(root)
