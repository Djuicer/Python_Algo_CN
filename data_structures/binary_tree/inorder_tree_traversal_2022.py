"""
Illustrate how 到 implement 中序 遍历 在 二叉搜索树。
Author: Gurneet Singh
https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/
"""


class BinaryTreeNode:
    """Defining 结构 的 BinaryTreeNode"""

    def __init__(self, data: int) -> None:
        self.data = data
        self.left_child: BinaryTreeNode | None = None
        self.right_child: BinaryTreeNode | None = None


def insert(node: BinaryTreeNode | None, new_value: int) -> BinaryTreeNode | None:
    """
    如果 二叉搜索树 为空，使 新节点 并且 declare 它 作为 根节点。
    >>> node_a = BinaryTreeNode(12345)
    >>> node_b = insert(node_a, 67890)
    >>> node_a.left_child == node_b.left_child
    True
    >>> node_a.right_child == node_b.right_child
    True
    >>> node_a.data == node_b.data
    True
    """
    if node is None:
        node = BinaryTreeNode(new_value)
        return node

    # 二叉搜索树 非空,
    # 因此 我们 将 插入 它 到 该树
    # 如果 new_value 是 较小 比 值 的 数据 在 节点,
    #  添加 它 到 左子树 并且 proceed 递归地
    if new_value < node.data:
        node.left_child = insert(node.left_child, new_value)
    else:
        # 如果 new_value 是 更大 比 值 的 数据 在 节点,
        #  添加 它 到 右子树 并且 proceed 递归地
        node.right_child = insert(node.right_child, new_value)
    return node


def inorder(node: BinaryTreeNode | None) -> list[int]:  # 如果 节点 是 None,返回
    """
    >>> inorder(make_tree())
    [6, 10, 14, 15, 20, 25, 60]
    """
    if node:
        inorder_array = inorder(node.left_child)
        inorder_array = [*inorder_array, node.data]
        inorder_array = inorder_array + inorder(node.right_child)
    else:
        inorder_array = []
    return inorder_array


def make_tree() -> BinaryTreeNode | None:
    root = insert(None, 15)
    insert(root, 10)
    insert(root, 25)
    insert(root, 6)
    insert(root, 14)
    insert(root, 20)
    insert(root, 60)
    return root


def main() -> None:
    # main 函数
    root = make_tree()
    print("Printing values of binary search tree in Inorder Traversal.")
    inorder(root)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
