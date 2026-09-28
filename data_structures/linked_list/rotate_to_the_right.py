from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    data: int
    next_node: Node | None = None


def print_linked_list(head: Node | None) -> None:
    """
        打印 整个 链表 迭代地。

        此函数 打印 元素 的 链表 separated 通过 '->'。

        参数：
            头节点 (节点 | None): 头节点 的 链表 到 为 printed,
    或 None 如果 链表 为空。

        >>> head = insert_node(None, 0)
        >>> head = insert_node(head, 2)
        >>> head = insert_node(head, 1)
        >>> print_linked_list(head)
        0->2->1
        >>> head = insert_node(head, 4)
        >>> head = insert_node(head, 5)
        >>> print_linked_list(head)
        0->2->1->4->5
    """
    if head is None:
        return
    while head.next_node is not None:
        print(head.data, end="->")
        head = head.next_node
    print(head.data)


def insert_node(head: Node | None, data: int) -> Node:
    """
    插入一个 新节点 在 末尾 的 链表 并且 返回 新 头节点。

    参数：
        头节点 (节点 | None): 头节点 的 链表。
        数据 (int): 数据 到 为 已插入 到 新节点。

    返回值：
        节点: 新 头节点 的 链表。

    >>> head = insert_node(None, 10)
    >>> head = insert_node(head, 9)
    >>> head = insert_node(head, 8)
    >>> print_linked_list(head)
    10->9->8
    """
    new_node = Node(data)
    # 如果 链表 为空，new_node 变为 头节点
    if head is None:
        return new_node

    temp_node = head
    while temp_node.next_node:
        temp_node = temp_node.next_node

    temp_node.next_node = new_node
    return head


def rotate_to_the_right(head: Node, places: int) -> Node:
    """
    旋转 链表 到 右 通过 位置 times。

    参数：
        头节点: 头节点 的 链表。
        位置: 数 的 位置 到 旋转。

    返回值：
        节点: 头节点 的 rotated 链表。

    >>> rotate_to_the_right(None, places=1)
    Traceback (most recent call last):
        ...
    ValueError: The linked list is empty.
    >>> head = insert_node(None, 1)
    >>> rotate_to_the_right(head, places=1) == head
    True
    >>> head = insert_node(None, 1)
    >>> head = insert_node(head, 2)
    >>> head = insert_node(head, 3)
    >>> head = insert_node(head, 4)
    >>> head = insert_node(head, 5)
    >>> new_head = rotate_to_the_right(head, places=2)
    >>> print_linked_list(new_head)
    4->5->1->2->3
    """
    # 检查是否 该列表 为空 或 具有 仅 一个 元素
    if not head:
        raise ValueError("The linked list is empty.")

    if head.next_node is None:
        return head

    # 计算 长度 的 链表
    length = 1
    temp_node = head
    while temp_node.next_node is not None:
        length += 1
        temp_node = temp_node.next_node

    # Adjust 该值 的 位置 到 avoid 位置 longer 比 该列表。
    places %= length

    if places == 0:
        return head  # 作为 没有 旋转 是 需要。

    # 查找 新 头节点 位置 之后 旋转。
    new_head_index = length - places

    # 遍历 到 新 头节点 位置
    temp_node = head
    for _ in range(new_head_index - 1):
        assert temp_node.next_node
        temp_node = temp_node.next_node

    # 更新 指针 到 执行 旋转
    assert temp_node.next_node
    new_head = temp_node.next_node
    temp_node.next_node = None
    temp_node = new_head
    while temp_node.next_node:
        temp_node = temp_node.next_node
    temp_node.next_node = head

    assert new_head
    return new_head


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    head = insert_node(None, 5)
    head = insert_node(head, 1)
    head = insert_node(head, 2)
    head = insert_node(head, 4)
    head = insert_node(head, 3)

    print("Original list: ", end="")
    print_linked_list(head)

    places = 3
    new_head = rotate_to_the_right(head, places)

    print(f"After {places} iterations: ", end="")
    print_linked_list(new_head)
