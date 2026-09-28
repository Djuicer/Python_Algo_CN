from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    """
    创建 并且 初始化 节点 类 instance。
    >>> Node(20)
    Node(20)
    >>> Node("Hello, world!")
    Node(Hello, world!)
    >>> Node(None)
    Node(None)
    >>> Node(True)
    Node(True)
    """

    data: Any
    next_node: Node | None = None

    def __repr__(self) -> str:
        """
        获取 字符串 表示 的 此 节点。
        >>> Node(10).__repr__()
        'Node(10)'
        >>> repr(Node(10))
        'Node(10)'
        >>> str(Node(10))
        'Node(10)'
        >>> Node(10)
        Node(10)
        """
        return f"Node({self.data})"


class LinkedList:
    def __init__(self) -> None:
        """
        创建 并且 初始化 LinkedList 类 instance。
        >>> linked_list = LinkedList()
        >>> linked_list.head is None
        True
        """
        self.head: Node | None = None

    def __iter__(self) -> Iterator[Any]:
        """
        此函数 是 intended 用于 迭代器 到 access
        并且 迭代 通过 数据 inside 链表。
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("tail")
        >>> linked_list.insert_tail("tail_1")
        >>> linked_list.insert_tail("tail_2")
        >>> for node in linked_list: # __iter__ used here.
        ...     node
        'tail'
        'tail_1'
        'tail_2'
        """
        node = self.head
        while node:
            yield node.data
            node = node.next_node

    def __len__(self) -> int:
        """
        返回 长度 的 链表 i.e. 节点数量
        >>> linked_list = LinkedList()
        >>> len(linked_list)
        0
        >>> linked_list.insert_tail("tail")
        >>> len(linked_list)
        1
        >>> linked_list.insert_head("head")
        >>> len(linked_list)
        2
        >>> _ = linked_list.delete_tail()
        >>> len(linked_list)
        1
        >>> _ = linked_list.delete_head()
        >>> len(linked_list)
        0
        """
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        """
        字符串 表示/visualization 的 连接 列表
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail(1)
        >>> linked_list.insert_tail(3)
        >>> linked_list.__repr__()
        '1 -> 3'
        >>> repr(linked_list)
        '1 -> 3'
        >>> str(linked_list)
        '1 -> 3'
        >>> linked_list.insert_tail(5)
        >>> f"{linked_list}"
        '1 -> 3 -> 5'
        """
        return " -> ".join([str(item) for item in self])

    def __getitem__(self, index: int) -> Any:
        """
        Indexing Support. 使用 到 获取 一个节点 在 particular 位置
        >>> linked_list = LinkedList()
        >>> for i in range(0, 10):
        ...     linked_list.insert_nth(i, i)
        >>> all(str(linked_list[i]) == str(i) for i in range(0, 10))
        True
        >>> linked_list[-10]
        Traceback (most recent call last):
            ...
        ValueError: list index out of range.
        >>> linked_list[len(linked_list)]
        Traceback (most recent call last):
            ...
        ValueError: list index out of range.
        """
        if not 0 <= index < len(self):
            raise ValueError("list index out of range.")
        for i, node in enumerate(self):
            if i == index:
                return node
        return None

    # 使用 到 更改 数据 的 particular 节点
    def __setitem__(self, index: int, data: Any) -> None:
        """
        >>> linked_list = LinkedList()
        >>> for i in range(0, 10):
        ...     linked_list.insert_nth(i, i)
        >>> linked_list[0] = 666
        >>> linked_list[0]
        666
        >>> linked_list[5] = -666
        >>> linked_list[5]
        -666
        >>> linked_list[-10] = 666
        Traceback (most recent call last):
            ...
        ValueError: list index out of range.
        >>> linked_list[len(linked_list)] = 666
        Traceback (most recent call last):
            ...
        ValueError: list index out of range.
        """
        if not 0 <= index < len(self):
            raise ValueError("list index out of range.")
        current = self.head
        assert current is not None
        for _ in range(index):
            current = current.next_node
            assert current is not None
        current.data = data

    def insert_tail(self, data: Any) -> None:
        """
        插入 数据 到 末尾 的 链表。
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("tail")
        >>> linked_list
        tail
        >>> linked_list.insert_tail("tail_2")
        >>> linked_list
        tail -> tail_2
        >>> linked_list.insert_tail("tail_3")
        >>> linked_list
        tail -> tail_2 -> tail_3
        """
        self.insert_nth(len(self), data)

    def insert_head(self, data: Any) -> None:
        """
        插入 数据 到 开头 的 链表。
        >>> linked_list = LinkedList()
        >>> linked_list.insert_head("head")
        >>> linked_list
        head
        >>> linked_list.insert_head("head_2")
        >>> linked_list
        head_2 -> head
        >>> linked_list.insert_head("head_3")
        >>> linked_list
        head_3 -> head_2 -> head
        """
        self.insert_nth(0, data)

    def insert_nth(self, index: int, data: Any) -> None:
        """
        插入 数据 在 给定 索引。
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.insert_tail("third")
        >>> linked_list
        first -> second -> third
        >>> linked_list.insert_nth(1, "fourth")
        >>> linked_list
        first -> fourth -> second -> third
        >>> linked_list.insert_nth(3, "fifth")
        >>> linked_list
        first -> fourth -> second -> fifth -> third
        """
        if not 0 <= index <= len(self):
            raise IndexError("list index out of range")
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        elif index == 0:
            new_node.next_node = self.head  # 链接 new_node 到 头节点
            self.head = new_node
        else:
            temp = self.head
            assert temp is not None
            for _ in range(index - 1):
                temp = temp.next_node
                assert temp is not None
            new_node.next_node = temp.next_node
            temp.next_node = new_node

    def print_list(self) -> None:  # 打印 每个 节点 数据
        """
        此方法 打印 每个 节点 数据。
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.insert_tail("third")
        >>> linked_list
        first -> second -> third
        """
        print(self)

    def delete_head(self) -> Any:
        """
        删除 第一个节点 并且 返回
        节点's 数据。
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.insert_tail("third")
        >>> linked_list
        first -> second -> third
        >>> linked_list.delete_head()
        'first'
        >>> linked_list
        second -> third
        >>> linked_list.delete_head()
        'second'
        >>> linked_list
        third
        >>> linked_list.delete_head()
        'third'
        >>> linked_list.delete_head()
        Traceback (most recent call last):
            ...
        IndexError: List index out of range.
        """
        return self.delete_nth(0)

    def delete_tail(self) -> Any:  # 删除 从 尾节点
        """
        删除 尾节点 末尾 节点 并且 返回
        节点's 数据。
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.insert_tail("third")
        >>> linked_list
        first -> second -> third
        >>> linked_list.delete_tail()
        'third'
        >>> linked_list
        first -> second
        >>> linked_list.delete_tail()
        'second'
        >>> linked_list
        first
        >>> linked_list.delete_tail()
        'first'
        >>> linked_list.delete_tail()
        Traceback (most recent call last):
            ...
        IndexError: List index out of range.
        """
        return self.delete_nth(len(self) - 1)

    def delete_nth(self, index: int = 0) -> Any:
        """
        删除 节点 在 给定 索引 并且 返回
        节点's 数据。
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.insert_tail("third")
        >>> linked_list
        first -> second -> third
        >>> linked_list.delete_nth(1) # delete middle
        'second'
        >>> linked_list
        first -> third
        >>> linked_list.delete_nth(5) # this raises error
        Traceback (most recent call last):
            ...
        IndexError: List index out of range.
        >>> linked_list.delete_nth(-1) # this also raises error
        Traceback (most recent call last):
            ...
        IndexError: List index out of range.
        """
        if not 0 <= index <= len(self) - 1:  # 测试 如果 索引 是 有效
            raise IndexError("List index out of range.")
        delete_node = self.head  # default 第一个节点
        if index == 0:
            self.head = self.head.next_node
        else:
            temp = self.head
            assert temp is not None
            for _ in range(index - 1):
                temp = temp.next_node
                assert temp is not None
            delete_node = temp.next_node
            assert delete_node is not None
            temp.next_node = delete_node.next_node
        return delete_node.data

    def is_empty(self) -> bool:
        """
        检查是否 链表 为空。
        >>> linked_list = LinkedList()
        >>> linked_list.is_empty()
        True
        >>> linked_list.insert_head("first")
        >>> linked_list.is_empty()
        False
        """
        return self.head is None

    def reverse(self) -> None:
        """
        此 反转 链表 顺序。
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.insert_tail("third")
        >>> linked_list
        first -> second -> third
        >>> linked_list.reverse()
        >>> linked_list
        third -> second -> first
        """
        prev = None
        current = self.head

        while current:
            # 存储 当前节点's 下一个节点。
            next_node = current.next_node
            # 使 当前节点's next_node 点 backwards
            current.next_node = prev
            # 使 上一个节点 为 当前节点
            prev = current
            # 使 当前节点 next_node 节点 (到 progress 迭代)
            current = next_node
        # 返回 prev 在 顺序 到 put 头节点 在 末尾
        self.head = prev


def test_singly_linked_list() -> None:
    """
    >>> test_singly_linked_list()
    """
    linked_list = LinkedList()
    assert linked_list.is_empty() is True
    assert str(linked_list) == ""

    try:
        linked_list.delete_head()
        raise AssertionError  # 此 应 不 发生。
    except IndexError:
        assert True  # 此 应 发生。

    try:
        linked_list.delete_tail()
        raise AssertionError  # 此 应 不 发生。
    except IndexError:
        assert True  # 此 应 发生。

    for i in range(10):
        assert len(linked_list) == i
        linked_list.insert_nth(i, i + 1)
    assert str(linked_list) == " -> ".join(str(i) for i in range(1, 11))

    linked_list.insert_head(0)
    linked_list.insert_tail(11)
    assert str(linked_list) == " -> ".join(str(i) for i in range(12))

    assert linked_list.delete_head() == 0
    assert linked_list.delete_nth(9) == 10
    assert linked_list.delete_tail() == 11
    assert len(linked_list) == 9
    assert str(linked_list) == " -> ".join(str(i) for i in range(1, 10))

    assert all(linked_list[i] == i + 1 for i in range(9)) is True

    for i in range(9):
        linked_list[i] = -i
    assert all(linked_list[i] == -i for i in range(9)) is True

    linked_list.reverse()
    assert str(linked_list) == " -> ".join(str(i) for i in range(-8, 1))


def test_singly_linked_list_2() -> None:
    """
    此 section 的 测试 使用 varying 数据 types 用于 输入。
    >>> test_singly_linked_list_2()
    """
    test_input = [
        -9,
        100,
        Node(77345112),
        "dlrow olleH",
        7,
        5555,
        0,
        -192.55555,
        "Hello, world!",
        77.9,
        Node(10),
        None,
        None,
        12.20,
    ]
    linked_list = LinkedList()

    for i in test_input:
        linked_list.insert_tail(i)

    # 检查是否 它's 空 或 不
    assert linked_list.is_empty() is False
    assert (
        str(linked_list)
        == "-9 -> 100 -> Node(77345112) -> dlrow olleH -> 7 -> 5555 -> "
        "0 -> -192.55555 -> Hello, world! -> 77.9 -> Node(10) -> None -> None -> 12.2"
    )

    # 删除 头节点
    result = linked_list.delete_head()
    assert result == -9
    assert (
        str(linked_list) == "100 -> Node(77345112) -> dlrow olleH -> 7 -> 5555 -> 0 -> "
        "-192.55555 -> Hello, world! -> 77.9 -> Node(10) -> None -> None -> 12.2"
    )

    # 删除 尾节点
    result = linked_list.delete_tail()
    assert result == 12.2
    assert (
        str(linked_list) == "100 -> Node(77345112) -> dlrow olleH -> 7 -> 5555 -> 0 -> "
        "-192.55555 -> Hello, world! -> 77.9 -> Node(10) -> None -> None"
    )

    # 删除一个 节点 在 specific location 在 链表
    result = linked_list.delete_nth(10)
    assert result is None
    assert (
        str(linked_list) == "100 -> Node(77345112) -> dlrow olleH -> 7 -> 5555 -> 0 -> "
        "-192.55555 -> Hello, world! -> 77.9 -> Node(10) -> None"
    )

    # 添加 一个节点 instance 到 其 头节点
    linked_list.insert_head(Node("Hello again, world!"))
    assert (
        str(linked_list)
        == "Node(Hello again, world!) -> 100 -> Node(77345112) -> dlrow olleH -> "
        "7 -> 5555 -> 0 -> -192.55555 -> Hello, world! -> 77.9 -> Node(10) -> None"
    )

    # 添加 None 到 其 尾节点
    linked_list.insert_tail(None)
    assert (
        str(linked_list)
        == "Node(Hello again, world!) -> 100 -> Node(77345112) -> dlrow olleH -> 7 -> "
        "5555 -> 0 -> -192.55555 -> Hello, world! -> 77.9 -> Node(10) -> None -> None"
    )

    # 反转 链表
    linked_list.reverse()
    assert (
        str(linked_list)
        == "None -> None -> Node(10) -> 77.9 -> Hello, world! -> -192.55555 -> 0 -> "
        "5555 -> 7 -> dlrow olleH -> Node(77345112) -> 100 -> Node(Hello again, world!)"
    )


def main() -> None:
    from doctest import testmod

    testmod()

    linked_list = LinkedList()
    linked_list.insert_head(input("Inserting 1st at head ").strip())
    linked_list.insert_head(input("Inserting 2nd at head ").strip())
    print("\nPrint list:")
    linked_list.print_list()
    linked_list.insert_tail(input("\nInserting 1st at tail ").strip())
    linked_list.insert_tail(input("Inserting 2nd at tail ").strip())
    print("\nPrint list:")
    linked_list.print_list()
    print("\nDelete head")
    linked_list.delete_head()
    print("Delete tail")
    linked_list.delete_tail()
    print("\nPrint list:")
    linked_list.print_list()
    print("\nReverse linked list")
    linked_list.reverse()
    print("\nPrint list:")
    linked_list.print_list()
    print("\nString representation of linked list:")
    print(linked_list)
    print("\nReading/changing Node data using indexing:")
    print(f"Element at Position 1: {linked_list[1]}")
    linked_list[1] = input("Enter New Value: ").strip()
    print("New list:")
    print(linked_list)
    print(f"length of linked_list is : {len(linked_list)}")


if __name__ == "__main__":
    main()
