# 实现 的 Circular 队列 (使用 Python 列表)


class CircularQueue:
    """Circular FIFO 队列 带有 fixed 容量"""

    def __init__(self, n: int) -> None:
        self.n = n
        self.array = [None] * self.n
        self.front = 0  # 索引 的 第一个元素
        self.rear = 0
        self.size = 0

    def __len__(self) -> int:
        """
        >>> cq = CircularQueue(5)
        >>> len(cq)
        0
        >>> cq.enqueue("A")  # doctest: +ELLIPSIS
        <data_structures.queues.circular_queue.CircularQueue object at ...>
        >>> cq.array
        ['A', None, None, None, None]
        >>> len(cq)
        1
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Checks 是否 该队列 为空 或 不
        >>> cq = CircularQueue(5)
        >>> cq.is_empty()
        True
        >>> cq.enqueue("A").is_empty()
        False
        """
        return self.size == 0

    def first(self):
        """
        返回值 第一个元素 的 该队列
        >>> cq = CircularQueue(5)
        >>> cq.first()
        False
        >>> cq.enqueue("A").first()
        'A'
        """
        return False if self.is_empty() else self.array[self.front]

    def enqueue(self, data) -> "CircularQueue":
        """
        此函数 inserts 元素 在 末尾 的队列 使用 self.rear 值
        作为 一个索引。

        >>> cq = CircularQueue(5)
        >>> cq.enqueue("A")  # doctest: +ELLIPSIS
        <data_structures.queues.circular_queue.CircularQueue object at ...>
        >>> (cq.size, cq.first())
        (1, 'A')
        >>> cq.enqueue("B")  # doctest: +ELLIPSIS
        <data_structures.queues.circular_queue.CircularQueue object at ...>
        >>> cq.array
        ['A', 'B', None, None, None]
        >>> (cq.size, cq.first())
        (2, 'A')
        >>> cq.enqueue("C").enqueue("D").enqueue("E")  # doctest: +ELLIPSIS
        <data_structures.queues.circular_queue.CircularQueue object at ...>
        >>> cq.enqueue("F")
        Traceback (most recent call last):
           ...
        Exception: QUEUE IS FULL
        """
        if self.size >= self.n:
            raise Exception("QUEUE IS FULL")

        self.array[self.rear] = data
        self.rear = (self.rear + 1) % self.n
        self.size += 1
        return self

    def dequeue(self):
        """
        此函数 removes 元素 从 该队列 使用 在 self.前端 值 作为
        索引 并且 返回值 它

        >>> cq = CircularQueue(5)
        >>> cq.dequeue()
        Traceback (most recent call last):
           ...
        Exception: UNDERFLOW
        >>> cq.enqueue("A").enqueue("B").dequeue()
        'A'
        >>> (cq.size, cq.first())
        (1, 'B')
        >>> cq.dequeue()
        'B'
        >>> cq.dequeue()
        Traceback (most recent call last):
           ...
        Exception: UNDERFLOW
        """
        if self.size == 0:
            raise Exception("UNDERFLOW")

        temp = self.array[self.front]
        self.array[self.front] = None
        self.front = (self.front + 1) % self.n
        self.size -= 1
        return temp
