from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(order=True)
class Node:
    """
    类 表示 一个节点 在 链表。

    属性：
        数据: 数据 存储 在 该节点。
        下一个: 引用 到 下一个节点 在 链表。

    >>> Node(1, Node(2, Node(3)))
    Node(data=1, next=Node(data=2, next=Node(data=3, next=None)))
    """

    data: int
    next: Node | None = None


class SortedLinkedList:
    """此 类  表示 已排序 链表。"""

    def __init__(self) -> None:
        """
        创建 并且 初始化 LinkedList 类 instance。
        >>> linked_list = SortedLinkedList()
        >>> linked_list.head is None
        True
        """
        self.head: Node | None = None
        self.tail: Node | None = None

    def __iter__(self) -> Iterator[int]:
        """迭代 超过 数据 的 节点 在 链表。

        >>> linked_list = SortedLinkedList()
        >>> linked_list.insert(3)
        >>> linked_list.insert(1)
        >>> linked_list.insert(2)
        >>> tuple(linked_list)
        (1, 2, 3)
        """
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        """返回以下对象的数量： 节点 在 链表。

        >>> linked_list = SortedLinkedList()
        >>> len(linked_list)
        0
        >>> linked_list.insert(3)
        >>> len(linked_list)
        1
        >>> linked_list.insert(1)
        >>> linked_list.insert(2)
        >>> len(linked_list)
        3
        """
        return len(tuple(self))

    def __contains__(self, data: int) -> bool:
        """检查是否 一个节点 带有 给定 数据 存在 在 链表。

        >>> linked_list = SortedLinkedList()
        >>> linked_list.insert(3)
        >>> 3 in linked_list
        True
        >>> 1 in linked_list
        False
        """
        return data in tuple(self)

    def insert(self, data: int) -> None:
        """插入一个 节点 在 其 已排序 位置
        此函数 可以 为 rewritten 用于 任意 数据 类型，但是
        comparator 此处 必须 为 changed

        参数：
            数据 (int): 数据 的 链表

        Doctests
        >>> linked_list = SortedLinkedList()
        >>> linked_list.insert(32)
        >>> linked_list.insert(57)
        >>> linked_list.insert(45)
        >>> tuple(linked_list)
        (32, 45, 57)
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        elif new_node < self.head:
            new_node.next = self.head
            self.head = new_node
        else:
            temp_node: Node | None = self.head
            if temp_node:
                while temp_node.next and temp_node.next.data < data:
                    temp_node = temp_node.next
                new_node.next = temp_node.next
                temp_node.next = new_node
                if new_node.next is None:
                    self.tail = new_node

    def delete(self, data: int) -> bool:
        """此函数 deletes 第一个 appearance 的 节点 带有
        数据 从 它's 已排序 位置

        此函数 可以 为 re written 用于 任意 数据 类型 但是
        comparator her 必须 具有 到 为 changed

        参数：
            数据 (int): 数据 的节点 该 是 需要 到 为 已删除

        返回值：
            bool: status 是否 该节点 got 已删除 或 不

        Doctests

        >>> linkedList=SortedLinkedList()
        >>> linkedList.insert(32)
        >>> linkedList.insert(57)
        >>> linkedList.insert(45)
        >>> tuple(linkedList)
        (32, 45, 57)
        >>> linkedList.delete(45)
        True
        >>> tuple(linkedList)
        (32, 57)
        """
        if self.head is None:
            return False

        if self.head.data == data:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            return True

        temp_node: Node | None = self.head
        if temp_node:
            while temp_node.next:
                if temp_node.next.data == data:
                    temp_node.next = temp_node.next.next
                    if temp_node.next is None:
                        self.tail = temp_node
                    return True
                temp_node = temp_node.next

        return False

    def search(self, data: int) -> bool:
        """此函数 searches 数据 给定 输入 从 user
        并且 返回 是否 数据 存在 或 不

        参数：
            数据 (int): 数据 到 为 已搜索

        返回值：
            bool: flag indicating 是否 数据 存在 或 不

        Doctests
        >>> linkedList=SortedLinkedList()
        >>> linkedList.insert(32)
        >>> linkedList.insert(57)
        >>> linkedList.insert(45)
        >>> tuple(linkedList)
        (32, 45, 57)
        >>> linkedList.search(45)
        True
        >>> linkedList.search(90)
        False
        """
        return data in self

    def is_empty(self) -> bool:
        """此函数 将 检查 是否 该列表 为空 或 不

        返回值：
            bool: flag indicating 是否 列表 为空 或 不

        Doctests

        >>> linkedList=SortedLinkedList()
        >>> linkedList.is_empty()
        True
        >>> linkedList.insert(32)
        >>> linkedList.insert(57)
        >>> linkedList.insert(45)
        >>> linkedList.is_empty()
        False
        """
        return not self

    def min_value(self) -> int | None:
        """此函数 将 返回 最小值 值

        返回值：
            int | None: 最小值 值 或 None 如果 列表 为空

        Doctests

        >>> linkedList=SortedLinkedList()
        >>> linkedList.min_value() is None
        True
        >>> linkedList.insert(32)
        >>> linkedList.insert(57)
        >>> linkedList.insert(45)
        >>> linkedList.min_value()
        32
        """
        return min(self) if self.head else None

    def max_value(self) -> int | None:
        """此函数  将 返回 最大值 值


        返回值：
            int | None: 最大值 值 或 None 如果 列表 为空

        Doctests

        >>> linkedList=SortedLinkedList()
        >>> linkedList.max_value() is None
        True
        >>> linkedList.insert(32)
        >>> linkedList.insert(57)
        >>> linkedList.insert(45)
        >>> linkedList.max_value()
        57
        """
        return max(self) if self.head else None

    def remove_duplicates(self) -> None:
        """
        此函数 将 移除 重复项 从 该列表

        Doctests

        >>> linkedList=SortedLinkedList()
        >>> linkedList.insert(32)
        >>> linkedList.insert(57)
        >>> linkedList.insert(45)
        >>> linkedList.insert(45)
        >>> tuple(linkedList)
        (32, 45, 45, 57)
        >>> linkedList.remove_duplicates()
        >>> tuple(linkedList)
        (32, 45, 57)
        """

        temp: Node | None = self.head
        while temp and temp.next:
            if temp.data == temp.next.data:
                temp.next = temp.next.next
            else:
                temp = temp.next

    def merge(self, other_list: SortedLinkedList) -> None:
        """此函数 将 合并 输入 列表 带有 当前 列表

        参数：
            other_list (SortedLinkedList): 该列表 到 为 合并后

        Doctests

        >>> linkedList=SortedLinkedList()
        >>> linkedList.insert(32)
        >>> linkedList.insert(57)
        >>> linkedList.insert(45)
        >>> tuple(linkedList)
        (32, 45, 57)
        >>> linkedList2=SortedLinkedList()
        >>> linkedList2.insert(23)
        >>> linkedList2.insert(47)
        >>> linkedList2.insert(95)
        >>> tuple(linkedList2)
        (23, 47, 95)
        >>> linkedList.merge(linkedList2)
        >>> tuple(linkedList)
        (23, 32, 45, 47, 57, 95)
        """
        if other_list.head is None:
            return
        elif self.head is None:
            self.head = other_list.head
            self.tail = other_list.tail
            return
        else:
            temp: Node | None = other_list.head

            while temp:
                self.insert(temp.data)
                temp = temp.next


if __name__ == "__main__":
    linked_list = SortedLinkedList()
    while True:
        print("Enter")
        print("1.  Insert")
        print("2.  Display")
        print("3.  Delete")
        print("4.  Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            node_data = int(input("Enter a number: "))
            linked_list.insert(node_data)
        elif choice == "2":
            linked_list.display()
        elif choice == "3":
            node_data = int(input("Enter the data to delete: "))
            if linked_list.delete(node_data):
                print(f"Node with data {node_data} deleted successfully")
            else:
                print(f"Node with data {node_data} not found in the list")
        elif choice == "4":
            break
        else:
            print("Wrong input")
