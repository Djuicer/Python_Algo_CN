from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    data: Any
    next_node: Node | None = None


@dataclass
class LinkedList:
    head: Node | None = None

    def __iter__(self) -> Iterator:
        """
        >>> linked_list = LinkedList()
        >>> list(linked_list)
        []
        >>> linked_list.push(0)
        >>> tuple(linked_list)
        (0,)
        """
        node = self.head
        while node:
            yield node.data
            node = node.next_node

    def __len__(self) -> int:
        """
        >>> linked_list = LinkedList()
        >>> len(linked_list)
        0
        >>> linked_list.push(0)
        >>> len(linked_list)
        1
        """
        return sum(1 for _ in self)

    def push(self, new_data: Any) -> None:
        """
        添加 新节点 带有 给定 数据 到 开头 的 链表。

        参数：
            new_data (任意): 数据 到 为 added 到 新节点。

        返回值：
            None

        示例：
            >>> linked_list = LinkedList()
            >>> linked_list.push(5)
            >>> linked_list.push(4)
            >>> linked_list.push(3)
            >>> linked_list.push(2)
            >>> linked_list.push(1)
            >>> list(linked_list)
            [1, 2, 3, 4, 5]
        """
        new_node = Node(new_data)
        new_node.next_node = self.head
        self.head = new_node

    def swap_nodes(self, node_data_1: Any, node_data_2: Any) -> None:
        """
        交换 位置 的 两个 节点 在 链表 基于 在 它们的 数据 值。

        参数：
            node_data_1: 数据 值 的 第一个节点 到 为 swapped。
            node_data_2: 数据 值 的 第二个 节点 到 为 swapped。


        Note:
            如果 任一 的 指定 数据 值 isn't 找到 则，没有 swapping occurs。

        示例：
        当 两者 值 是 存在 在 链表。
            >>> linked_list = LinkedList()
            >>> linked_list.push(5)
            >>> linked_list.push(4)
            >>> linked_list.push(3)
            >>> linked_list.push(2)
            >>> linked_list.push(1)
            >>> list(linked_list)
            [1, 2, 3, 4, 5]
            >>> linked_list.swap_nodes(1, 5)
            >>> tuple(linked_list)
            (5, 2, 3, 4, 1)

        当 一个 值 是 存在 并且 另一个 isn't 在 链表。
            >>> second_list = LinkedList()
            >>> second_list.push(6)
            >>> second_list.push(7)
            >>> second_list.push(8)
            >>> second_list.push(9)
            >>> second_list.swap_nodes(1, 6) is None
            True

        当 两者 值 是 absent 在 链表。
            >>> second_list = LinkedList()
            >>> second_list.push(10)
            >>> second_list.push(9)
            >>> second_list.push(8)
            >>> second_list.push(7)
            >>> second_list.swap_nodes(1, 3) is None
            True

        当 linkedlist 为空。
            >>> second_list = LinkedList()
            >>> second_list.swap_nodes(1, 3) is None
            True

        返回值：
            None
        """
        if node_data_1 == node_data_2:
            return

        node_1 = self.head
        while node_1 and node_1.data != node_data_1:
            node_1 = node_1.next_node
        node_2 = self.head
        while node_2 and node_2.data != node_data_2:
            node_2 = node_2.next_node
        if node_1 is None or node_2 is None:
            return
        # 交换 数据 值 的 两个 节点
        node_1.data, node_2.data = node_2.data, node_1.data


if __name__ == "__main__":
    """
    Python script that outputs the swap of nodes in a linked list.
    """
    from doctest import testmod

    testmod()
    linked_list = LinkedList()
    for i in range(5, 0, -1):
        linked_list.push(i)

    print(f"Original Linked List: {list(linked_list)}")
    linked_list.swap_nodes(1, 4)
    print(f"Modified Linked List: {list(linked_list)}")
    print("After swapping the nodes whose data is 1 and 4.")
