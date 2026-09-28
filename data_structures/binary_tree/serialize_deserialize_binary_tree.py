from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class TreeNode:
    """
    二叉树 节点 具有 一个值，左子节点，并且 右子节点。

    Props:
        值: 该值 的 该节点。
        左: 左子节点 的 该节点。
        右: 右子节点 的 该节点。
    """

    value: int = 0
    left: TreeNode | None = None
    right: TreeNode | None = None

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise TypeError("Value must be an integer.")

    def __iter__(self) -> Iterator[TreeNode]:
        """
        迭代 通过 该树 在 前序。

        返回值：
            迭代器 的树 节点。

        >>> list(TreeNode(1))
        [1,null,null]
        >>> tuple(TreeNode(1, TreeNode(2), TreeNode(3)))
        (1,2,null,null,3,null,null, 2,null,null, 3,null,null)
        """
        yield self
        yield from self.left or ()
        yield from self.right or ()

    def __len__(self) -> int:
        """
        Count 节点数量 在 该树。

        返回值：
            节点数量 在 该树。

        >>> len(TreeNode(1))
        1
        >>> len(TreeNode(1, TreeNode(2), TreeNode(3)))
        3
        """
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        """
        Represent 该树 作为 字符串。

        返回值：
            字符串 表示 的 该树。

        >>> repr(TreeNode(1))
        '1,null,null'
        >>> repr(TreeNode(1, TreeNode(2), TreeNode(3)))
        '1,2,null,null,3,null,null'
        >>> repr(TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5))))
        '1,2,null,null,3,4,null,null,5,null,null'
        """
        return f"{self.value},{self.left!r},{self.right!r}".replace("None", "null")

    @classmethod
    def five_tree(cls) -> TreeNode:
        """
        >>> repr(TreeNode.five_tree())
        '1,2,null,null,3,4,null,null,5,null,null'
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.right.left = TreeNode(4)
        root.right.right = TreeNode(5)
        return root


def deserialize(data: str) -> TreeNode | None:
    """
    Deserialize 字符串 到 二叉树。

    参数：
        数据(str): serialized 字符串。

    返回值：
        根节点 的 二叉树。

    >>> root = TreeNode.five_tree()
    >>> serialzed_data = repr(root)
    >>> deserialized = deserialize(serialzed_data)
    >>> root == deserialized
    True
    >>> root is deserialized  # two separate trees
    False
    >>> root.right.right.value = 6
    >>> root == deserialized
    False
    >>> serialzed_data = repr(root)
    >>> deserialized = deserialize(serialzed_data)
    >>> root == deserialized
    True
    >>> deserialize("")
    Traceback (most recent call last):
        ...
    ValueError: Data cannot be empty.
    """

    if not data:
        raise ValueError("Data cannot be empty.")

    # 拆分 serialized 字符串 通过 comma 到 获取 节点 值
    nodes = data.split(",")

    def build_tree() -> TreeNode | None:
        # 获取 下一个 值 从 该列表
        value = nodes.pop(0)

        if value == "null":
            return None

        node = TreeNode(int(value))
        node.left = build_tree()  # 递归地 构建 左子树
        node.right = build_tree()  # 递归地 构建 右子树
        return node

    return build_tree()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
