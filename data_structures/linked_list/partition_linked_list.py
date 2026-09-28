from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    item: Any
    next: Node | Any = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
        self.size = 0

    def __str__(self) -> str:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.add(23)
        >>> linked_list.add(14)
        >>> linked_list.add(9)
        >>> print(linked_list)
        9 --> 14 --> 23
        """
        iterate = self.head
        item_str = ""
        item_list: list[str] = []
        while iterate:
            item_list.append(str(iterate.item))
            iterate = iterate.next

        item_str = " --> ".join(item_list)

        return item_str

    def __len__(self) -> int:
        """
        >>> linked_list = LinkedList()
        >>> len(linked_list)
        0
        >>> linked_list.add("a")
        >>> len(linked_list)
        1
        >>> linked_list.add("b")
        >>> len(linked_list)
        2
        """
        return self.size

    def add(self, item: Any, position: int = 0) -> None:
        """
        添加 元素 到 LinkedList 在 指定 位置。
        Default 位置 是 0 (头节点)。

        参数：
            元素 (任意): 元素 到 添加 到 LinkedList。
            位置 (int，可选): 位置 在 其 到 添加 元素。
                默认值 到 0。

        抛出异常：
            ValueError: 如果 位置 是 负 或 out 的 bounds。

        >>> linked_list = LinkedList()
        >>> linked_list.add(1)
        >>> linked_list.add(2)
        >>> linked_list.add(3)
        >>> linked_list.add(4, 2)
        >>> print(linked_list)
        3 --> 2 --> 4 --> 1

        # 测试 添加 到 负 位置
        >>> linked_list.add(5, -3)
        Traceback (most recent call last):
            ...
        ValueError: Position must be non-negative

        # 测试 添加 到 out-的-bounds 位置
        >>> linked_list.add(5,7)
        Traceback (most recent call last):
            ...
        ValueError: Out of bounds
        >>> linked_list.add(5, 4)
        >>> print(linked_list)
        3 --> 2 --> 4 --> 1 --> 5
        """
        if position < 0:
            raise ValueError("Position must be non-negative")

        if position == 0 or self.head is None:
            new_node = Node(item, self.head)
            self.head = new_node
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
                if current is None:
                    raise ValueError("Out of bounds")
            new_node = Node(item, current.next)
            current.next = new_node
        self.size += 1

    def partition_liked_list(self, value: int) -> None:
        """
        Partition 链表 基于 在 节点 元素 在 顺序。
        所有节点 带有 元素 较小 比 值 应 occur 在 左,
        当 those 更大 比 或 等于 到 值 应 occur 在 右。

        >>> linked_list = LinkedList()
        >>> linked_list.add(1)
        >>> linked_list.add(2)
        >>> linked_list.add(3)
        >>> linked_list.add(4, 2)
        >>> linked_list.add(5, 4)
        >>> print(linked_list)
        3 --> 2 --> 4 --> 1 --> 5
        >>> linked_list.partition_liked_list(3)
        >>> print(linked_list)
        2 --> 1 --> 3 --> 4 --> 5
        >>> linked_list = LinkedList()
        >>> linked_list.add(1)
        >>> linked_list.add(2)
        >>> linked_list.add(3)
        >>> print(linked_list)
        3 --> 2 --> 1
        >>> linked_list.partition_liked_list(3)
        >>> print(linked_list)
        2 --> 1 --> 3
        >>> linked_list = LinkedList()
        >>> linked_list.add(5)
        >>> linked_list.add(5)
        >>> linked_list.add(5)
        >>> print(linked_list)
        5 --> 5 --> 5
        >>> linked_list.partition_liked_list(5)
        >>> print(linked_list)
        5 --> 5 --> 5
        >>> linked_list = LinkedList()
        >>> linked_list.add(1, 0)
        >>> linked_list.add(2, 1)
        >>> linked_list.add(3, 2)
        >>> linked_list.add(4, 3)
        >>> linked_list.add(5, 4)
        >>> print(linked_list)
        1 --> 2 --> 3 --> 4 --> 5
        >>> linked_list.partition_liked_list(6)
        >>> print(linked_list)
        1 --> 2 --> 3 --> 4 --> 5
        >>> linked_list = LinkedList()
        >>> linked_list.add(1)
        >>> print(linked_list)
        1
        >>> linked_list.partition_liked_list(1)
        >>> print(linked_list)
        1
        """
        if self.head is None:
            return

        less_nodes, greater_nodes = Node(0), Node(0)
        current, current_less, current_greater = self.head, less_nodes, greater_nodes

        while current is not None:
            if current.item < value:
                current_less.next = current
                current_less = current_less.next
            else:
                current_greater.next = current
                current_greater = current_greater.next
            current = current.next

        current_less.next = greater_nodes.next
        current_greater.next = None
        self.head = less_nodes.next
