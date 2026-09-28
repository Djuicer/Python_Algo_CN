"""
递归 Program 到 创建一个 链表 从 序列 并且
打印 字符串 表示 的 它。
"""


class Node:
    def __init__(self, data=None) -> None:
        self.data = data
        self.next = None

    def __repr__(self) -> str:
        """返回值 visual 表示 的节点 并且 所有 其 following 节点。"""
        string_rep = ""
        temp = self
        while temp:
            string_rep += f"<{temp.data}> ---> "
            temp = temp.next
        string_rep += "<END>"
        return string_rep


def make_linked_list(elements_list: list | tuple) -> Node:
    """
    创建一个 链表 从 元素 的 给定 序列
    (list/tuple) and returns the head of the Linked List.

    >>> make_linked_list([])
    Traceback (most recent call last):
        ...
    ValueError: The Elements List is empty
    >>> make_linked_list(())
    Traceback (most recent call last):
        ...
    ValueError: The Elements List is empty
    >>> make_linked_list([1])
    <1> ---> <END>
    >>> make_linked_list((1,))
    <1> ---> <END>
    >>> make_linked_list([1, 3, 5, 32, 44, 12, 43])
    <1> ---> <3> ---> <5> ---> <32> ---> <44> ---> <12> ---> <43> ---> <END>
    >>> make_linked_list((1, 3, 5, 32, 44, 12, 43))
    <1> ---> <3> ---> <5> ---> <32> ---> <44> ---> <12> ---> <43> ---> <END>
    """

    # 如果 elements_list 为空
    if not elements_list:
        raise ValueError("The Elements List is empty")

    # 集合 第一个元素 作为 头节点
    head = Node(elements_list[0])
    current = head
    # 循环 通过 元素 从 位置 1
    for data in elements_list[1:]:
        current.next = Node(data)
        current = current.next
    return head
