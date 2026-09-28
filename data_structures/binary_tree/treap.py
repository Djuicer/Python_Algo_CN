from __future__ import annotations

from random import random


class Node:
    """
    Treap's 节点
    Treap 是 二叉树 通过 值 并且 堆 通过 优先级
    """

    def __init__(self, value: int | None = None) -> None:
        self.value = value
        self.prior = random()
        self.left: Node | None = None
        self.right: Node | None = None

    def __repr__(self) -> str:
        from pprint import pformat

        if self.left is None and self.right is None:
            return f"'{self.value}: {self.prior:.5}'"
        else:
            return pformat(
                {f"{self.value}: {self.prior:.5}": (self.left, self.right)}, indent=1
            )

    def __str__(self) -> str:
        value = str(self.value) + " "
        left = str(self.left or "")
        right = str(self.right or "")
        return value + left + right


def split(root: Node | None, value: int) -> tuple[Node | None, Node | None]:
    """
    我们 拆分 当前 树 到 2 树 带有 值：

    左 树 包含 所有 值 较小 比 拆分 值。
    右 树 包含 所有 值 更大 或 等于，比 拆分 值
    """
    if root is None or root.value is None:  # None 树 是 拆分 到 2 Nones
        return None, None
    elif value <= root.value:
        """
        Right tree's root will be current node.
        Now we split(with the same value) current node's left son
        Left tree: left part of that split
        Right tree's left son: right part of that split
        """
        left, root.left = split(root.left, value)
        return left, root
    else:
        """
        Just symmetric to previous case
        """
        root.right, right = split(root.right, value)
        return root, right


def merge(left: Node | None, right: Node | None) -> Node | None:
    """
    我们 合并 2 树 到 一个。
    Note: 所有 左 树's 值 必须 为 较小 比 所有 右 树's
    """
    if (not left) or (not right):  # 如果 一个 节点 是 None，返回 另一个
        return left or right
    elif left.prior > right.prior:
        """
        Left will be root because it has more priority
        Now we need to merge left's right son and right tree
        """
        left.right = merge(left.right, right)
        return left
    else:
        """
        Symmetric as well
        """
        right.left = merge(left, right.left)
        return right


def insert(root: Node | None, value: int) -> Node | None:
    """
    插入 元素

    拆分 当前 树 带有 一个值 到 左，右,
    插入 新节点 到 middle
    合并 左，节点，右 到 根节点
    """
    node = Node(value)
    left, right = split(root, value)
    return merge(merge(left, node), right)


def erase(root: Node | None, value: int) -> Node | None:
    """
    Erase 元素

    拆分 所有节点 带有 值 较小 到 左,
    拆分 所有节点 带有 值 更大 到 右。
    合并 左，右
    """
    left, right = split(root, value)
    _, right = split(right, value + 1)
    return merge(left, right)


def inorder(root: Node | None) -> None:
    """
    仅 递归 打印 的 树
    """
    if not root:  # None
        return
    else:
        inorder(root.left)
        print(root.value, end=",")
        inorder(root.right)


def interact_treap(root: Node | None, args: str) -> Node | None:
    """
    Commands:
    + 值 到 添加 值 到 treap
    - 值 到 erase 所有节点 带有 值

        >>> root = interact_treap(None, "+1")
        >>> inorder(root)
        1,
        >>> root = interact_treap(root, "+3 +5 +17 +19 +2 +16 +4 +0")
        >>> inorder(root)
        0,1,2,3,4,5,16,17,19,
        >>> root = interact_treap(root, "+4 +4 +4")
        >>> inorder(root)
        0,1,2,3,4,4,4,4,5,16,17,19,
        >>> root = interact_treap(root, "-0")
        >>> inorder(root)
        1,2,3,4,4,4,4,5,16,17,19,
        >>> root = interact_treap(root, "-4")
        >>> inorder(root)
        1,2,3,5,16,17,19,
        >>> root = interact_treap(root, "=0")
        Unknown command
    """
    for arg in args.split():
        if arg[0] == "+":
            root = insert(root, int(arg[1:]))

        elif arg[0] == "-":
            root = erase(root, int(arg[1:]))

        else:
            print("Unknown command")

    return root


def main() -> None:
    """之后 每个 命令，program 打印 treap"""
    root = None
    print(
        "enter numbers to create a tree, + value to add value into treap, "
        "- value to erase all nodes with value. 'q' to quit. "
    )

    args = input()
    while args != "q":
        root = interact_treap(root, args)
        print(root)
        args = input()

    print("good by!")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
