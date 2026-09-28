# complete working Python program 到 demonstrate 所有
# 栈 操作 使用 双向链表

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


class Node[T]:
    def __init__(self, data: T) -> None:
        self.data = data  # Assign 数据
        self.next: Node[T] | None = None  # 初始化 下一个 作为 null
        self.prev: Node[T] | None = None  # 初始化 prev 作为 null


class Stack[T]:
    """
    >>> stack = Stack()
    >>> stack.is_empty()
    True
    >>> stack.print_stack()
    stack elements are:
    >>> for i in range(4):
    ...     stack.push(i)
    ...
    >>> stack.is_empty()
    False
    >>> stack.print_stack()
    stack elements are:
    3->2->1->0->
    >>> stack.top()
    3
    >>> len(stack)
    4
    >>> stack.pop()
    3
    >>> stack.print_stack()
    stack elements are:
    2->1->0->
    """

    def __init__(self) -> None:
        self.head: Node[T] | None = None

    def push(self, data: T) -> None:
        """add a Node to the stack"""
        if self.head is None:
            self.head = Node(data)
        else:
            new_node = Node(data)
            self.head.prev = new_node
            new_node.next = self.head
            new_node.prev = None
            self.head = new_node

    def pop(self) -> T | None:
        """pop the top element off the stack"""
        if self.head is None:
            return None
        else:
            assert self.head is not None
            temp = self.head.data
            self.head = self.head.next
            if self.head is not None:
                self.head.prev = None
            return temp

    def top(self) -> T | None:
        """return the top element of the stack"""
        return self.head.data if self.head is not None else None

    def __len__(self) -> int:
        temp = self.head
        count = 0
        while temp is not None:
            count += 1
            temp = temp.next
        return count

    def is_empty(self) -> bool:
        return self.head is None

    def print_stack(self) -> None:
        print("stack elements are:")
        temp = self.head
        while temp is not None:
            print(temp.data, end="->")
            temp = temp.next


# 代码 execution starts 此处
if __name__ == "__main__":
    # 开始 带有 空栈
    stack: Stack[int] = Stack()

    # 插入 4 在 开头. 因此 栈 变为 4->None
    print("Stack operations using Doubly LinkedList")
    stack.push(4)

    # 插入 5 在 开头. 因此 栈 变为 4->5->None
    stack.push(5)

    # 插入 6 在 开头. 因此 栈 变为 4->5->6->None
    stack.push(6)

    # 插入 7 在 开头. 因此 栈 变为 4->5->6->7->None
    stack.push(7)

    # 打印 栈
    stack.print_stack()

    # 打印 顶部 元素
    print("\nTop element is ", stack.top())

    # 打印 栈 大小
    print("Size of the stack is ", len(stack))

    # 弹出 顶部 元素
    stack.pop()

    # 弹出 顶部 元素
    stack.pop()

    # 两个 元素 具有 现在 been popped off
    stack.print_stack()

    # 打印 True 如果 该栈 为空 否则 False
    print("\nstack is empty:", stack.is_empty())
