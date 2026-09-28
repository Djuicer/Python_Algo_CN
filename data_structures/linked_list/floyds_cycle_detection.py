"""
Floyd's 环 detection 算法 是 popular 算法 使用 到 detect cycles
在 链表. 它 使用 两个 指针，慢 指针 并且 fast 指针,
到 遍历 链表. 慢 指针 移动 一个 节点 在 时间 当 fast
指针 移动 两个 节点 在 时间. 如果 其中 是 环 在 链表,
fast 指针 将 eventually catch 向上 到 慢 指针 并且 they 将
meet 在 相同 节点. 如果 其中 是 没有 环，fast 指针 将 reach 末尾 的
链表 并且 算法 将 terminate。

For more information: https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare
"""

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Self


@dataclass
class Node:
    """
    类 表示 一个节点 在 单向链表。
    """

    data: Any
    next_node: Self | None = None


@dataclass
class LinkedList:
    """
    类 表示 单向链表。
    """

    head: Node | None = None

    def __iter__(self) -> Iterator:
        """
        Iterates 通过 链表。

        返回值：
            迭代器: 迭代器 超过 链表。

        示例：
        >>> linked_list = LinkedList()
        >>> list(linked_list)
        []
        >>> linked_list.add_node(1)
        >>> tuple(linked_list)
        (1,)
        """
        visited = []
        node = self.head
        while node:
            # Avoid infinite 循环 在 其中's 环
            if node in visited:
                return
            visited.append(node)
            yield node.data
            node = node.next_node

    def add_node(self, data: Any) -> None:
        """
        Adds 新节点 到 末尾 的 链表。

        参数：
            数据 (任意): 数据 到 为 存储 在 新节点。

        示例：
        >>> linked_list = LinkedList()
        >>> linked_list.add_node(1)
        >>> linked_list.add_node(2)
        >>> linked_list.add_node(3)
        >>> linked_list.add_node(4)
        >>> tuple(linked_list)
        (1, 2, 3, 4)
        """
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current_node = self.head
        while current_node.next_node is not None:
            current_node = current_node.next_node

        current_node.next_node = new_node

    def detect_cycle(self) -> bool:
        """
        Detects 如果 其中 是 环 在 链表 使用
        Floyd's 环 detection 算法。

        返回值：
            bool: True 如果 其中 是 环，False 否则。

        示例：
        >>> linked_list = LinkedList()
        >>> linked_list.add_node(1)
        >>> linked_list.add_node(2)
        >>> linked_list.add_node(3)
        >>> linked_list.add_node(4)

        >>> linked_list.detect_cycle()
        False

        # 创建一个 环 在 链表
        >>> linked_list.head.next_node.next_node.next_node = linked_list.head.next_node

        >>> linked_list.detect_cycle()
        True
        """
        if self.head is None:
            return False

        slow_pointer: Node | None = self.head
        fast_pointer: Node | None = self.head

        while fast_pointer is not None and fast_pointer.next_node is not None:
            slow_pointer = slow_pointer.next_node if slow_pointer else None
            fast_pointer = fast_pointer.next_node.next_node
            if slow_pointer == fast_pointer:
                return True

        return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    linked_list = LinkedList()
    linked_list.add_node(1)
    linked_list.add_node(2)
    linked_list.add_node(3)
    linked_list.add_node(4)

    # 创建一个 环 在 链表
    # 它 第一个 检查是否 头节点，next_node，并且 next_node.next_node 属性 的
    # 链表 是 不 None 到 avoid 任意 potential 类型 errors。
    if (
        linked_list.head
        and linked_list.head.next_node
        and linked_list.head.next_node.next_node
    ):
        linked_list.head.next_node.next_node.next_node = linked_list.head.next_node

    has_cycle = linked_list.detect_cycle()
    print(has_cycle)  # 输出: True
