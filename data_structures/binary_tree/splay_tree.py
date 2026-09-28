"""
Splay 树 - self-adjusting 二叉搜索树。

splay 树 是 二叉搜索树 带有 additional property 该
recently accessed 元素 是 quick 到 access again.  每个 access (搜索,
插入 或 删除) 移动 target 节点 到 根节点 通过 序列 的
rotations called "splaying".  此 gives 均摊 时间复杂度 的
O(log n) per 操作 并且 makes 该树 very efficient 当 access
模式 具有 locality 的 引用 (small 子集 的 键 是 touched often)。

Reference: https://en.wikipedia.org/wiki/Splay_tree
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass
class Node:
    """
    单个节点 的 splay 树。

    ``左`` 并且 ``右`` 子节点 是 excluded 从 ``repr`` 因此 该
    节点 打印 compactly instead 的 递归地 dumping whole 子树。

    >>> Node(10)
    Node(key=10)
    """

    key: int
    left: Node | None = field(default=None, repr=False)
    right: Node | None = field(default=None, repr=False)


class SplayTree:
    """
    self-adjusting 二叉搜索树。

    >>> tree = SplayTree()
    >>> tree.insert(10)
    >>> tree.insert(20)
    >>> tree.insert(30)
    >>> tree.root.key  # last inserted key is splayed to the root
    30
    >>> tree.search(10)
    True
    >>> tree.root.key  # the searched key is now the root
    10
    >>> tree.search(99)
    False
    >>> list(tree)
    [10, 20, 30]
    """

    def __init__(self) -> None:
        self.root: Node | None = None

    def _rotate_right(self, node: Node) -> Node:
        """
        执行 右 旋转 around ``节点`` 并且 返回 新 子树 根节点。

            节点            左
           /    \\          /    \\
         左    c   -->   节点
        /   \\                   /    \\
       a     b                 b      c
        """
        left = node.left
        assert left is not None
        node.left = left.right
        left.right = node
        return left

    def _rotate_left(self, node: Node) -> Node:
        """
        执行 左 旋转 around ``节点`` 并且 返回 新 子树 根节点。

           节点                 右
          /    \\               /     \\
         右   -->    节点     c
              /     \\        /    \\
             b       c       a      b
        """
        right = node.right
        assert right is not None
        node.right = right.left
        right.left = node
        return right

    def _splay(self, root: Node | None, key: int) -> Node | None:
        """
        Splay 该节点 带有 ``键`` (或 最后一个节点 在 搜索 路径 如果
        ``键`` 是 absent) 到 根节点 的 子树 并且 返回 新 根节点。
        此 使用 classic 底部-向上 递归 formulation。
        """
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                # Zig-Zig (左 左)
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                # Zig-Zag (左 右)
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)
            return root if root.left is None else self._rotate_right(root)
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                # Zig-Zig (右 右)
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                # Zig-Zag (右 左)
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)
            return root if root.right is None else self._rotate_left(root)

    def insert(self, key: int) -> None:
        """
        插入 ``键`` 到 该树 并且 splay 它 到 根节点。

        >>> tree = SplayTree()
        >>> for key in (5, 3, 8, 3):  # duplicate keys are ignored
        ...     tree.insert(key)
        >>> list(tree)
        [3, 5, 8]
        >>> tree.root.key  # the duplicate access splays 3 back to the root
        3
        """
        if self.root is None:
            self.root = Node(key)
            return

        self.root = self._splay(self.root, key)
        assert self.root is not None
        if self.root.key == key:
            return  # 键 已经 存在，它 是 现在 在 根节点

        node = Node(key)
        if key < self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
        self.root = node

    def search(self, key: int) -> bool:
        """
        返回 是否 ``键`` 是 存在 并且 splay 最后一个 accessed 节点。

        >>> tree = SplayTree()
        >>> tree.search(1)
        False
        >>> for key in (40, 20, 60):
        ...     tree.insert(key)
        >>> tree.search(20)
        True
        >>> tree.root.key
        20
        """
        self.root = self._splay(self.root, key)
        return self.root is not None and self.root.key == key

    def delete(self, key: int) -> None:
        """
        移除 ``键`` 从 该树 如果 它 是 存在。

        >>> tree = SplayTree()
        >>> for key in (10, 20, 30, 40):
        ...     tree.insert(key)
        >>> tree.delete(20)
        >>> list(tree)
        [10, 30, 40]
        >>> tree.delete(99)  # deleting an absent key is a no-op
        >>> list(tree)
        [10, 30, 40]
        >>> for key in (10, 30, 40):
        ...     tree.delete(key)
        >>> list(tree)
        []
        """
        if self.root is None:
            return

        self.root = self._splay(self.root, key)
        assert self.root is not None
        if self.root.key != key:
            return  # 键 未找到

        left, right = self.root.left, self.root.right
        if left is None:
            self.root = right
        else:
            # Splay 最大值 的 左子树 到 其 根节点; 它 具有 没有
            # 右子节点，因此 右子树 可以 为 attached 其中。
            left = self._splay(left, key)
            assert left is not None
            left.right = right
            self.root = left

    def __iter__(self) -> Iterator[int]:
        """
        Yield 键 的树 在 ascending (在-顺序) 顺序。

        >>> tree = SplayTree()
        >>> for key in (7, 2, 9, 4, 1):
        ...     tree.insert(key)
        >>> list(tree)
        [1, 2, 4, 7, 9]
        """

        def in_order(node: Node | None) -> Iterator[int]:
            if node is not None:
                yield from in_order(node.left)
                yield node.key
                yield from in_order(node.right)

        yield from in_order(self.root)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
