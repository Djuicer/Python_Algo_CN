"""
Implementing 双端队列 使用 DoublyLinkedList ..。
操作：
    1. 插入 在 前端 -> O(1)
    2. 插入 在 末尾 -> O(1)
    3. 移除 从 前端 -> O(1)
    4. 移除 从 末尾 -> O(1)
"""


class _DoublyLinkedBase:
    """Private 类 (到 为 inherited)"""

    class _Node:
        __slots__ = "_data", "_next", "_prev"

        def __init__(self, link_p, element, link_n) -> None:
            self._prev = link_p
            self._data = element
            self._next = link_n

        def has_next_and_prev(self) -> str:
            return (
                f" Prev -> {self._prev is not None}, Next -> {self._next is not None}"
            )

    def __init__(self) -> None:
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self):
        return self.__len__() == 0

    def _insert(self, predecessor, e, successor):
        # 创建 new_node 通过 setting 它's prev.链接 -> header
        # setting 它's 下一个.链接 -> trailer
        new_node = self._Node(predecessor, e, successor)
        predecessor._next = new_node
        successor._prev = new_node
        self._size += 1
        return self

    def _delete(self, node):
        predecessor = node._prev
        successor = node._next

        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        temp = node._data
        node._prev = node._next = node._data = None
        del node
        return temp


class LinkedDeque(_DoublyLinkedBase):
    def first(self):
        """返回 第一个元素
        >>> d = LinkedDeque()
        >>> d.add_first('A').first()
        'A'
        >>> d.add_first('B').first()
        'B'
        """
        if self.is_empty():
            raise Exception("List is empty")
        return self._header._next._data

    def last(self):
        """返回 最后一个元素
        >>> d = LinkedDeque()
        >>> d.add_last('A').last()
        'A'
        >>> d.add_last('B').last()
        'B'
        """
        if self.is_empty():
            raise Exception("List is empty")
        return self._trailer._prev._data

    # 双端队列 插入 操作 (在队首，在 末尾)

    def add_first(self, element):
        """插入 在 前端
        >>> LinkedDeque().add_first('AV').first()
        'AV'
        """
        return self._insert(self._header, element, self._header._next)

    def add_last(self, element):
        """插入 在 末尾
        >>> LinkedDeque().add_last('B').last()
        'B'
        """
        return self._insert(self._trailer._prev, element, self._trailer)

    # DEqueu 移除 操作 (在队首，在 末尾)

    def remove_first(self):
        """removal 从 前端
        >>> d = LinkedDeque()
        >>> d.is_empty()
        True
        >>> d.remove_first()
        Traceback (most recent call last):
           ...
        IndexError: remove_first from empty list
        >>> d.add_first('A') # doctest: +ELLIPSIS
        <data_structures.linked_list.deque_doubly.LinkedDeque object at ...
        >>> d.remove_first()
        'A'
        >>> d.is_empty()
        True
        """
        if self.is_empty():
            raise IndexError("remove_first from empty list")
        return self._delete(self._header._next)

    def remove_last(self):
        """removal 在 末尾
        >>> d = LinkedDeque()
        >>> d.is_empty()
        True
        >>> d.remove_last()
        Traceback (most recent call last):
           ...
        IndexError: remove_first from empty list
        >>> d.add_first('A') # doctest: +ELLIPSIS
        <data_structures.linked_list.deque_doubly.LinkedDeque object at ...
        >>> d.remove_last()
        'A'
        >>> d.is_empty()
        True
        """
        if self.is_empty():
            raise IndexError("remove_first from empty list")
        return self._delete(self._trailer._prev)
