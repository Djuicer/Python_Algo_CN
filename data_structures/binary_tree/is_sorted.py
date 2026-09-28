"""
给定 根节点 的 二叉树，判断是否 它 是 有效 二叉搜索树 (BST)。

有效 二叉搜索树 是 定义 作为 follows：
- 左子树 的 一个节点 包含 仅 节点 带有 键 较小 比 该节点's 键。
- 右子树 的 一个节点 包含 仅 节点 带有 键 更大 比 该节点's 键。
- 两者 左 并且 右 子树 必须 也 为 binary 搜索 树。

在 effect，二叉树 是 有效 BST 如果 其 节点 是 已排序 在 升序。
leetcode: https://leetcode.com/problems/validate-binary-search-tree/

如果 n 是 节点数量 在 该树 则：
运行时间: O(n)
空间: O(1)
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    data: float
    left: Node | None = None
    right: Node | None = None

    def __iter__(self) -> Iterator[float]:
        """
        >>> root = Node(data=2.1)
        >>> list(root)
        [2.1]
        >>> root.left=Node(data=2.0)
        >>> list(root)
        [2.0, 2.1]
        >>> root.right=Node(data=2.2)
        >>> list(root)
        [2.0, 2.1, 2.2]
        """
        if self.left:
            yield from self.left
        yield self.data
        if self.right:
            yield from self.right

    @property
    def is_sorted(self) -> bool:
        """
        >>> Node(data='abc').is_sorted
        True
        >>> Node(data=2,
        ...      left=Node(data=1.999),
        ...      right=Node(data=3)).is_sorted
        True
        >>> Node(data=0,
        ...      left=Node(data=0),
        ...      right=Node(data=0)).is_sorted
        True
        >>> Node(data=0,
        ...      left=Node(data=-11),
        ...      right=Node(data=3)).is_sorted
        True
        >>> Node(data=5,
        ...      left=Node(data=1),
        ...      right=Node(data=4, left=Node(data=3))).is_sorted
        False
        >>> Node(data='a',
        ...      left=Node(data=1),
        ...      right=Node(data=4, left=Node(data=3))).is_sorted
        Traceback (most recent call last):
            ...
        TypeError: '<' not supported between instances of 'str' and 'int'
        >>> Node(data=2,
        ...      left=Node([]),
        ...      right=Node(data=4, left=Node(data=3))).is_sorted
        Traceback (most recent call last):
            ...
        TypeError: '<' not supported between instances of 'int' and 'list'
        """
        if self.left and (self.data < self.left.data or not self.left.is_sorted):
            return False
        return not (
            self.right and (self.data > self.right.data or not self.right.is_sorted)
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    tree = Node(data=2.1, left=Node(data=2.0), right=Node(data=2.2))
    print(f"Tree {list(tree)} is sorted: {tree.is_sorted = }.")
    assert tree.right
    tree.right.data = 2.0
    print(f"Tree {list(tree)} is sorted: {tree.is_sorted = }.")
    tree.right.data = 2.1
    print(f"Tree {list(tree)} is sorted: {tree.is_sorted = }.")
