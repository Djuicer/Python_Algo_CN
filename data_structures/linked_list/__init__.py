"""
连接 列表 consists 的 节点。
节点 包含 数据 并且 也 may 链接 到 另一个 节点：
    - 头节点 节点: 第一个节点，address 的
                 头节点 节点 gives us access 的 complete 列表
    - 最后一个节点: 点 到 null
"""

from __future__ import annotations

from typing import Any


class Node:
    def __init__(self, item: Any, next: Any) -> None:  # noqa: A002
        self.item = item
        self.next = next


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
        self.size = 0

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

    def remove(self) -> Any:
        # Switched 'self.is_empty()' 到 'self.头节点 是 None'
        # because mypy was considering the possibility that 'self.head'
        # 可以 为 None 在 下方 否则 part 并且 giving error
        if self.head is None:
            return None
        else:
            item = self.head.item
            self.head = self.head.next
            self.size -= 1
            return item

    def is_empty(self) -> bool:
        return self.head is None

    def __str__(self) -> str:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.add(23)
        >>> linked_list.add(14)
        >>> linked_list.add(9)
        >>> print(linked_list)
        9 --> 14 --> 23
        """
        if self.is_empty():
            return ""
        else:
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
        >>> _ = linked_list.remove()
        >>> len(linked_list)
        1
        >>> _ = linked_list.remove()
        >>> len(linked_list)
        0
        """
        return self.size
