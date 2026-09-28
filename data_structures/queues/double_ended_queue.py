"""
实现 的 double ended 队列。
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


class Deque:
    """
    双端队列 数据 结构。
    操作
    ----------
    追加(val: 任意) -> None
    appendleft(val: 任意) -> None
    extend(可迭代对象: 可迭代对象) -> None
    extendleft(可迭代对象: 可迭代对象) -> None
    弹出() -> 任意
    popleft() -> 任意
    Observers
    ---------
    is_empty() -> bool
    属性
    ----------
    _front: _Node
        前端 的 双端队列 .k.. 第一个元素
    _back: _Node
        后端 的 元素 .k.. 最后一个元素
    _len: int
        节点数量
    """

    __slots__ = ("_back", "_front", "_len")

    @dataclass
    class _Node:
        """
        表示 的 一个节点。
        包含 一个值 并且 指针 到 下一个节点 作为 well 作为 到 上一个。
        """

        val: Any = None
        next_node: Deque._Node | None = None
        prev_node: Deque._Node | None = None

    class _Iterator:
        """
        Helper 类 用于 迭代. 将 为 使用 到 implement 迭代。
        属性
        ----------
        _cur: _Node
            当前节点 的 迭代。
        """

        __slots__ = ("_cur",)

        def __init__(self, cur: Deque._Node | None) -> None:
            self._cur = cur

        def __iter__(self) -> Deque._Iterator:
            """
            >>> our_deque = Deque([1, 2, 3])
            >>> iterator = iter(our_deque)
            """
            return self

        def __next__(self) -> Any:
            """
            >>> our_deque = Deque([1, 2, 3])
            >>> iterator = iter(our_deque)
            >>> next(iterator)
            1
            >>> next(iterator)
            2
            >>> next(iterator)
            3
            """
            if self._cur is None:
                # 迭代完成
                raise StopIteration
            val = self._cur.val
            self._cur = self._cur.next_node

            return val

    def __init__(self, iterable: Iterable[Any] | None = None) -> None:
        self._front: Any = None
        self._back: Any = None
        self._len: int = 0

        if iterable is not None:
            # 追加 每个 值 到 双端队列
            for val in iterable:
                self.append(val)

    def append(self, val: Any) -> None:
        """
        Adds val 到 末尾 的 双端队列。
        时间复杂度: O(1)
        >>> our_deque_1 = Deque([1, 2, 3])
        >>> our_deque_1.append(4)
        >>> our_deque_1
        [1, 2, 3, 4]
        >>> our_deque_2 = Deque('ab')
        >>> our_deque_2.append('c')
        >>> our_deque_2
        ['a', 'b', 'c']
        >>> from collections import deque
        >>> deque_collections_1 = deque([1, 2, 3])
        >>> deque_collections_1.append(4)
        >>> deque_collections_1
        deque([1, 2, 3, 4])
        >>> deque_collections_2 = deque('ab')
        >>> deque_collections_2.append('c')
        >>> deque_collections_2
        deque(['a', 'b', 'c'])
        >>> list(our_deque_1) == list(deque_collections_1)
        True
        >>> list(our_deque_2) == list(deque_collections_2)
        True
        """
        node = self._Node(val, None, None)
        if self.is_empty():
            # 前端 = 后端
            self._front = self._back = node
            self._len = 1
        else:
            # connect 节点
            self._back.next_node = node
            node.prev_node = self._back
            self._back = node  # assign 新 后端 到 新节点

            self._len += 1

            # 使 确保 其中 were 没有 errors
            assert not self.is_empty(), "Error on appending value."

    def appendleft(self, val: Any) -> None:
        """
        Adds val 到 开头 的 双端队列。
        时间复杂度: O(1)
        >>> our_deque_1 = Deque([2, 3])
        >>> our_deque_1.appendleft(1)
        >>> our_deque_1
        [1, 2, 3]
        >>> our_deque_2 = Deque('bc')
        >>> our_deque_2.appendleft('a')
        >>> our_deque_2
        ['a', 'b', 'c']
        >>> from collections import deque
        >>> deque_collections_1 = deque([2, 3])
        >>> deque_collections_1.appendleft(1)
        >>> deque_collections_1
        deque([1, 2, 3])
        >>> deque_collections_2 = deque('bc')
        >>> deque_collections_2.appendleft('a')
        >>> deque_collections_2
        deque(['a', 'b', 'c'])
        >>> list(our_deque_1) == list(deque_collections_1)
        True
        >>> list(our_deque_2) == list(deque_collections_2)
        True
        """
        node = self._Node(val, None, None)
        if self.is_empty():
            # 前端 = 后端
            self._front = self._back = node
            self._len = 1
        else:
            # connect 节点
            node.next_node = self._front
            self._front.prev_node = node
            self._front = node  # assign 新 前端 到 新节点

            self._len += 1

            # 使 确保 其中 were 没有 errors
            assert not self.is_empty(), "Error on appending value."

    def extend(self, iterable: Iterable[Any]) -> None:
        """
        Appends 每个 值 的 可迭代对象 到 末尾 的 双端队列。
        时间复杂度: O(n)
        >>> our_deque_1 = Deque([1, 2, 3])
        >>> our_deque_1.extend([4, 5])
        >>> our_deque_1
        [1, 2, 3, 4, 5]
        >>> our_deque_2 = Deque('ab')
        >>> our_deque_2.extend('cd')
        >>> our_deque_2
        ['a', 'b', 'c', 'd']
        >>> from collections import deque
        >>> deque_collections_1 = deque([1, 2, 3])
        >>> deque_collections_1.extend([4, 5])
        >>> deque_collections_1
        deque([1, 2, 3, 4, 5])
        >>> deque_collections_2 = deque('ab')
        >>> deque_collections_2.extend('cd')
        >>> deque_collections_2
        deque(['a', 'b', 'c', 'd'])
        >>> list(our_deque_1) == list(deque_collections_1)
        True
        >>> list(our_deque_2) == list(deque_collections_2)
        True
        """
        for val in iterable:
            self.append(val)

    def extendleft(self, iterable: Iterable[Any]) -> None:
        """
        Appends 每个 值 的 可迭代对象 到 开头 的 双端队列。
        时间复杂度: O(n)
        >>> our_deque_1 = Deque([1, 2, 3])
        >>> our_deque_1.extendleft([0, -1])
        >>> our_deque_1
        [-1, 0, 1, 2, 3]
        >>> our_deque_2 = Deque('cd')
        >>> our_deque_2.extendleft('ba')
        >>> our_deque_2
        ['a', 'b', 'c', 'd']
        >>> from collections import deque
        >>> deque_collections_1 = deque([1, 2, 3])
        >>> deque_collections_1.extendleft([0, -1])
        >>> deque_collections_1
        deque([-1, 0, 1, 2, 3])
        >>> deque_collections_2 = deque('cd')
        >>> deque_collections_2.extendleft('ba')
        >>> deque_collections_2
        deque(['a', 'b', 'c', 'd'])
        >>> list(our_deque_1) == list(deque_collections_1)
        True
        >>> list(our_deque_2) == list(deque_collections_2)
        True
        """
        for val in iterable:
            self.appendleft(val)

    def pop(self) -> Any:
        """
        移除 最后一个元素 的 双端队列 并且 返回值 它。
        时间复杂度: O(1)
        @返回值 topop.val: 该值 的节点 到 弹出。
        >>> our_deque1 = Deque([1])
        >>> our_popped1 = our_deque1.pop()
        >>> our_popped1
        1
        >>> our_deque1
        []

        >>> our_deque2 = Deque([1, 2, 3, 15182])
        >>> our_popped2 = our_deque2.pop()
        >>> our_popped2
        15182
        >>> our_deque2
        [1, 2, 3]

        >>> from collections import deque
        >>> deque_collections = deque([1, 2, 3, 15182])
        >>> collections_popped = deque_collections.pop()
        >>> collections_popped
        15182
        >>> deque_collections
        deque([1, 2, 3])
        >>> list(our_deque2) == list(deque_collections)
        True
        >>> our_popped2 == collections_popped
        True
        """
        # 使 确保 双端队列 具有 元素 到 弹出
        assert not self.is_empty(), "Deque is empty."

        topop = self._back
        # 如果 仅 一个 元素 在 该队列: 点 前端 并且 后端 到 None
        # 否则 移除 一个 元素 从 后端
        if self._front == self._back:
            self._front = None
            self._back = None
        else:
            self._back = self._back.prev_node  # 集合 新 后端
            # drop 最后一个节点，python 将 deallocate memory automatically
            self._back.next_node = None

        self._len -= 1

        return topop.val

    def popleft(self) -> Any:
        """
        移除 第一个元素 的 双端队列 并且 返回值 它。
        时间复杂度: O(1)
        @返回值 topop.val: 该值 的节点 到 弹出。
        >>> our_deque1 = Deque([1])
        >>> our_popped1 = our_deque1.pop()
        >>> our_popped1
        1
        >>> our_deque1
        []
        >>> our_deque2 = Deque([15182, 1, 2, 3])
        >>> our_popped2 = our_deque2.popleft()
        >>> our_popped2
        15182
        >>> our_deque2
        [1, 2, 3]
        >>> from collections import deque
        >>> deque_collections = deque([15182, 1, 2, 3])
        >>> collections_popped = deque_collections.popleft()
        >>> collections_popped
        15182
        >>> deque_collections
        deque([1, 2, 3])
        >>> list(our_deque2) == list(deque_collections)
        True
        >>> our_popped2 == collections_popped
        True
        """
        # 使 确保 双端队列 具有 元素 到 弹出
        assert not self.is_empty(), "Deque is empty."

        topop = self._front
        # 如果 仅 一个 元素 在 该队列: 点 前端 并且 后端 到 None
        # 否则 移除 一个 元素 从 前端
        if self._front == self._back:
            self._front = None
            self._back = None
        else:
            self._front = self._front.next_node  # 集合 新 前端 并且 drop 第一个节点
            self._front.prev_node = None

        self._len -= 1

        return topop.val

    def is_empty(self) -> bool:
        """
        检查是否 双端队列 为空。
        时间复杂度: O(1)
        >>> our_deque = Deque([1, 2, 3])
        >>> our_deque.is_empty()
        False
        >>> our_empty_deque = Deque()
        >>> our_empty_deque.is_empty()
        True
        >>> from collections import deque
        >>> empty_deque_collections = deque()
        >>> list(our_empty_deque) == list(empty_deque_collections)
        True
        """
        return self._front is None

    def __len__(self) -> int:
        """
        Implements len() 函数. 返回值 长度 的 双端队列。
        时间复杂度: O(1)
        >>> our_deque = Deque([1, 2, 3])
        >>> len(our_deque)
        3
        >>> our_empty_deque = Deque()
        >>> len(our_empty_deque)
        0
        >>> from collections import deque
        >>> deque_collections = deque([1, 2, 3])
        >>> len(deque_collections)
        3
        >>> empty_deque_collections = deque()
        >>> len(empty_deque_collections)
        0
        >>> len(our_empty_deque) == len(empty_deque_collections)
        True
        """
        return self._len

    def __eq__(self, other: object) -> bool:
        """
        Implements "==" 运算符. 返回值 如果 *self* 是 等于 到 *另一个*。
        时间复杂度: O(n)
        >>> our_deque_1 = Deque([1, 2, 3])
        >>> our_deque_2 = Deque([1, 2, 3])
        >>> our_deque_1 == our_deque_2
        True
        >>> our_deque_3 = Deque([1, 2])
        >>> our_deque_1 == our_deque_3
        False
        >>> from collections import deque
        >>> deque_collections_1 = deque([1, 2, 3])
        >>> deque_collections_2 = deque([1, 2, 3])
        >>> deque_collections_1 == deque_collections_2
        True
        >>> deque_collections_3 = deque([1, 2])
        >>> deque_collections_1 == deque_collections_3
        False
        >>> (our_deque_1 == our_deque_2) == (deque_collections_1 == deque_collections_2)
        True
        >>> (our_deque_1 == our_deque_3) == (deque_collections_1 == deque_collections_3)
        True
        """

        if not isinstance(other, Deque):
            return NotImplemented

        me = self._front
        oth = other._front

        # 如果 长度 的 dequeues 是 不 相同，they 是 不 等于
        if len(self) != len(other):
            return False

        while me is not None and oth is not None:
            # 比较 每个 值
            if me.val != oth.val:
                return False
            me = me.next_node
            oth = oth.next_node

        return True

    def __iter__(self) -> Deque._Iterator:
        """
        Implements 迭代。
        时间复杂度: O(1)
        >>> our_deque = Deque([1, 2, 3])
        >>> for v in our_deque:
        ...     print(v)
        1
        2
        3
        >>> from collections import deque
        >>> deque_collections = deque([1, 2, 3])
        >>> for v in deque_collections:
        ...     print(v)
        1
        2
        3
        """
        return Deque._Iterator(self._front)

    def __repr__(self) -> str:
        """
        Implements 表示 的 双端队列。
        表示 它 作为 一个列表，带有 其 值 之间 '[' 并且 ']'。
        时间复杂度: O(n)
        >>> our_deque = Deque([1, 2, 3])
        >>> our_deque
        [1, 2, 3]
        """
        values_list = []
        aux = self._front
        while aux is not None:
            # 追加 值 在 一个列表 到 显示
            values_list.append(aux.val)
            aux = aux.next_node

        return f"[{', '.join(repr(val) for val in values_list)}]"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    dq = Deque([3])
    dq.pop()
