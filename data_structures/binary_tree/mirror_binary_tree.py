"""
给定 根节点 的 二叉树，镜像 该树，并且 返回 其 根节点。

Leetcode problem reference: https://leetcode.com/problems/mirror-binary-tree/
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    """
    一个节点 具有 值 变量 并且 指针 到 节点 到 其 左 并且 右。
    """

    value: int
    left: Node | None = None
    right: Node | None = None

    def __iter__(self) -> Iterator[int]:
        if self.left:
            yield from self.left
        yield self.value
        if self.right:
            yield from self.right

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def mirror(self) -> Node:
        """
        镜像 二叉树 rooted 在 此 节点 通过 swapping 左 并且 右 子节点。

        >>> tree = Node(0)
        >>> list(tree)
        [0]
        >>> list(tree.mirror())
        [0]
        >>> tree = Node(1, Node(0), Node(3, Node(2), Node(4, None, Node(5))))
        >>> tuple(tree)
        (0, 1, 2, 3, 4, 5)
        >>> tuple(tree.mirror())
        (5, 4, 3, 2, 1, 0)
        """
        self.left, self.right = self.right, self.left
        if self.left:
            self.left.mirror()
        if self.right:
            self.right.mirror()
        return self


def make_tree_seven() -> Node:
    r"""
    返回 二叉树 带有 7 节点 该 看起来 类似 此：
    ::

           1
         /   \
        2     3
       / \   / \
      4   5 6   7

    >>> tree_seven = make_tree_seven()
    >>> len(tree_seven)
    7
    >>> list(tree_seven)
    [4, 2, 5, 1, 6, 3, 7]
    """
    tree = Node(1)
    tree.left = Node(2)
    tree.right = Node(3)
    tree.left.left = Node(4)
    tree.left.right = Node(5)
    tree.right.left = Node(6)
    tree.right.right = Node(7)
    return tree


def make_tree_nine() -> Node:
    r"""
    返回 二叉树 带有 9 节点 该 看起来 类似 此：
    ::

            1
           / \
          2   3
         / \   \
        4   5   6
       / \   \
      7   8   9

    >>> tree_nine = make_tree_nine()
    >>> len(tree_nine)
    9
    >>> list(tree_nine)
    [7, 4, 8, 2, 5, 9, 1, 3, 6]
    """
    tree = Node(1)
    tree.left = Node(2)
    tree.right = Node(3)
    tree.left.left = Node(4)
    tree.left.right = Node(5)
    tree.right.right = Node(6)
    tree.left.left.left = Node(7)
    tree.left.left.right = Node(8)
    tree.left.right.right = Node(9)
    return tree


def main() -> None:
    r"""
    镜像 binary 树 带有 给定 根节点 并且 返回值 根节点

    >>> tree = make_tree_nine()
    >>> tuple(tree)
    (7, 4, 8, 2, 5, 9, 1, 3, 6)
    >>> tuple(tree.mirror())
    (6, 3, 1, 9, 5, 2, 8, 4, 7)

    nine_tree::

            1
           / \
          2   3
         / \   \
        4   5   6
       / \   \
      7   8   9

    mirrored 树 看起来 类似 此:：

          1
         / \
        3   2
       /   / \
      6   5   4
         /   / \
        9   8   7
    """
    trees = {"zero": Node(0), "seven": make_tree_seven(), "nine": make_tree_nine()}
    for name, tree in trees.items():
        print(f"      The {name} tree: {tuple(tree)}")
        # (0,)
        # (4, 2, 5, 1, 6, 3, 7)
        # (7, 4, 8, 2, 5, 9, 1, 3, 6)
        print(f"Mirror of {name} tree: {tuple(tree.mirror())}")
        # (0,)
        # (7, 3, 6, 1, 5, 2, 4)
        # (6, 3, 1, 9, 5, 2, 8, 4, 7)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
