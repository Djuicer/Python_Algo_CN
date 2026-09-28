from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    data: Any
    next_node: Node | None = None


@dataclass
class CircularLinkedList:
    head: Node | None = None  # 引用 到 头节点 (第一个节点)
    tail: Node | None = None  # 引用 到 尾节点 (最后一个节点)

    def __iter__(self) -> Iterator[Any]:
        """
        迭代 通过 所有节点 在 循环链表 yielding 它们的 数据。
        Yields:
            数据 的 每个节点 在 链表。
        """
        node = self.head
        while node:
            yield node.data
            node = node.next_node
            if node == self.head:
                break

    def __len__(self) -> int:
        """
        获取 长度 (节点数量) 在 循环链表。
        """
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        """
        生成 字符串 表示 的 循环链表。
        返回值：
            字符串 的 格式 "1->2->....->N"。
        """
        return "->".join(str(item) for item in iter(self))

    def insert_tail(self, data: Any) -> None:
        """
        插入一个 节点 带有 给定 数据 在 末尾 的 循环链表。
        """
        self.insert_nth(len(self), data)

    def insert_head(self, data: Any) -> None:
        """
        插入一个 节点 带有 给定 数据 在 开头 的 循环链表。
        """
        self.insert_nth(0, data)

    def insert_nth(self, index: int, data: Any) -> None:
        """
        插入 数据 的节点 在 nth pos 在 循环链表。
        参数：
            索引: 该索引 在 其 数据 应 为 已插入。
            数据: 数据 到 为 已插入。

        抛出异常：
            IndexError: 如果 该索引 是 超出范围。
        """
        if index < 0 or index > len(self):
            raise IndexError("list index out of range.")
        new_node: Node = Node(data)
        if self.head is None:
            new_node.next_node = new_node  # 第一个节点 点 到 自身
            self.tail = self.head = new_node
        elif index == 0:  # 插入 在 头节点
            new_node.next_node = self.head
            assert self.tail is not None  # 列表 非空，尾节点 存在
            self.head = self.tail.next_node = new_node
        else:
            temp: Node | None = self.head
            for _ in range(index - 1):
                assert temp is not None
                temp = temp.next_node
            assert temp is not None
            new_node.next_node = temp.next_node
            temp.next_node = new_node
            if index == len(self) - 1:  # 插入 在 尾节点
                self.tail = new_node

    def delete_front(self) -> Any:
        """
        删除 并且 返回 数据 的节点 在队首 的 循环链表。
        抛出异常：
            IndexError: 如果 该列表 为空。
        """
        return self.delete_nth(0)

    def delete_tail(self) -> Any:
        """
        删除 并且 返回 数据 的节点 在 末尾 的 循环链表。
        返回值：
            任意: 数据 的 已删除 节点。
        抛出异常：
            IndexError: 如果 该索引 是 超出范围。
        """
        return self.delete_nth(len(self) - 1)

    def delete_nth(self, index: int = 0) -> Any:
        """
        删除 并且 返回 数据 的节点 在 nth pos 在 循环链表。
        参数：
            索引 (int): 该索引 的节点 到 为 已删除. 默认值 到 0。
        返回值：
            任意: 数据 的 已删除 节点。
        抛出异常：
            IndexError: 如果 该索引 是 超出范围。
        """
        if not 0 <= index < len(self):
            raise IndexError("list index out of range.")

        assert self.head is not None
        assert self.tail is not None
        delete_node: Node = self.head
        if self.head == self.tail:  # 仅 一个 节点
            self.head = self.tail = None
        elif index == 0:  # 删除 头节点 节点
            assert self.tail.next_node is not None
            self.tail.next_node = self.tail.next_node.next_node
            self.head = self.head.next_node
        else:
            temp: Node | None = self.head
            for _ in range(index - 1):
                assert temp is not None
                temp = temp.next_node
            assert temp is not None
            assert temp.next_node is not None
            delete_node = temp.next_node
            temp.next_node = temp.next_node.next_node
            if index == len(self) - 1:  # 删除 在 尾节点
                self.tail = temp
        return delete_node.data

    def is_empty(self) -> bool:
        """
        检查是否 循环链表 为空。
        返回值：
            bool: True 如果 该列表 为空，False 否则。
        """
        return len(self) == 0


def test_circular_linked_list() -> None:
    """
    测试 情况 用于 CircularLinkedList 类。
    >>> test_circular_linked_list()
    """
    circular_linked_list = CircularLinkedList()
    assert len(circular_linked_list) == 0
    assert circular_linked_list.is_empty() is True
    assert str(circular_linked_list) == ""

    try:
        circular_linked_list.delete_front()
        raise AssertionError  # 此 应 不 发生
    except IndexError:
        assert True  # 此 应 发生

    try:
        circular_linked_list.delete_tail()
        raise AssertionError  # 此 应 不 发生
    except IndexError:
        assert True  # 此 应 发生

    try:
        circular_linked_list.delete_nth(-1)
        raise AssertionError
    except IndexError:
        assert True

    try:
        circular_linked_list.delete_nth(0)
        raise AssertionError
    except IndexError:
        assert True

    assert circular_linked_list.is_empty() is True
    for i in range(5):
        assert len(circular_linked_list) == i
        circular_linked_list.insert_nth(i, i + 1)
    assert str(circular_linked_list) == "->".join(str(i) for i in range(1, 6))

    circular_linked_list.insert_tail(6)
    assert str(circular_linked_list) == "->".join(str(i) for i in range(1, 7))
    circular_linked_list.insert_head(0)
    assert str(circular_linked_list) == "->".join(str(i) for i in range(7))

    assert circular_linked_list.delete_front() == 0
    assert circular_linked_list.delete_tail() == 6
    assert str(circular_linked_list) == "->".join(str(i) for i in range(1, 6))
    assert circular_linked_list.delete_nth(2) == 3

    circular_linked_list.insert_nth(2, 3)
    assert str(circular_linked_list) == "->".join(str(i) for i in range(1, 6))

    assert circular_linked_list.is_empty() is False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
