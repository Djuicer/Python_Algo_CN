"""
Pure Python implementations 的 Fixed 优先队列 并且 元素 优先队列
使用 Python 列表。
"""


class OverFlowError(Exception):
    pass


class UnderFlowError(Exception):
    pass


class FixedPriorityQueue:
    """
    Tasks 可以 为 added 到 优先队列 在 任意 时间 并且 在 任意 顺序 但是 当 Tasks
    是 removed 则 Task 带有 最高 优先级 是 removed 在 FIFO 顺序.  在
    代码 我们 将 使用 three levels 的 优先级 带有 优先级 zero Tasks being most
    urgent (high 优先级) 并且 优先级 2 tasks being least urgent。

    示例
    >>> fpq = FixedPriorityQueue()
    >>> fpq.enqueue(0, 10)
    >>> fpq.enqueue(1, 70)
    >>> fpq.enqueue(0, 100)
    >>> fpq.enqueue(2, 1)
    >>> fpq.enqueue(2, 5)
    >>> fpq.enqueue(1, 7)
    >>> fpq.enqueue(2, 4)
    >>> fpq.enqueue(1, 64)
    >>> fpq.enqueue(0, 128)
    >>> print(fpq)
    Priority 0: [10, 100, 128]
    Priority 1: [70, 7, 64]
    Priority 2: [1, 5, 4]
    >>> fpq.dequeue()
    10
    >>> fpq.dequeue()
    100
    >>> fpq.dequeue()
    128
    >>> fpq.dequeue()
    70
    >>> fpq.dequeue()
    7
    >>> print(fpq)
    Priority 0: []
    Priority 1: [64]
    Priority 2: [1, 5, 4]
    >>> fpq.dequeue()
    64
    >>> fpq.dequeue()
    1
    >>> fpq.dequeue()
    5
    >>> fpq.dequeue()
    4
    >>> fpq.dequeue()
    Traceback (most recent call last):
        ...
    data_structures.queues.priority_queue_using_list.UnderFlowError: All queues are empty
    >>> print(fpq)
    Priority 0: []
    Priority 1: []
    Priority 2: []
    """  # noqa: E501

    def __init__(self) -> None:
        self.queues = [
            [],
            [],
            [],
        ]

    def enqueue(self, priority: int, data: int) -> None:
        """
        添加 元素 到 队列 基于 在 其 优先级。
        如果 优先级 是 无效 ValueError 是 raised。
        如果 该队列 是 已满 OverFlowError 是 raised。
        """
        try:
            if len(self.queues[priority]) >= 100:
                raise OverflowError("Maximum queue size is 100")
            self.queues[priority].append(data)
        except IndexError:
            raise ValueError("Valid priorities are 0, 1, and 2")

    def dequeue(self) -> int:
        """
        返回 最高 优先级 元素 在 FIFO 顺序。
        如果 该队列 为空 则 under flow exception 是 raised。
        """
        for queue in self.queues:
            if queue:
                return queue.pop(0)
        raise UnderFlowError("All queues are empty")

    def __str__(self) -> str:
        return "\n".join(f"Priority {i}: {q}" for i, q in enumerate(self.queues))


class ElementPriorityQueue:
    """
    元素 优先队列 是 相同 作为 Fixed 优先队列 except 该 该值 的
    元素 自身 是 优先级. rules 用于 priorities 是 相同 作为
    Fixed 优先队列。

    >>> epq = ElementPriorityQueue()
    >>> epq.enqueue(10)
    >>> epq.enqueue(70)
    >>> epq.enqueue(4)
    >>> epq.enqueue(1)
    >>> epq.enqueue(5)
    >>> epq.enqueue(7)
    >>> epq.enqueue(4)
    >>> epq.enqueue(64)
    >>> epq.enqueue(128)
    >>> print(epq)
    [10, 70, 4, 1, 5, 7, 4, 64, 128]
    >>> epq.dequeue()
    1
    >>> epq.dequeue()
    4
    >>> epq.dequeue()
    4
    >>> epq.dequeue()
    5
    >>> epq.dequeue()
    7
    >>> epq.dequeue()
    10
    >>> print(epq)
    [70, 64, 128]
    >>> epq.dequeue()
    64
    >>> epq.dequeue()
    70
    >>> epq.dequeue()
    128
    >>> epq.dequeue()
    Traceback (most recent call last):
        ...
    data_structures.queues.priority_queue_using_list.UnderFlowError: The queue is empty
    >>> print(epq)
    []
    """

    def __init__(self) -> None:
        self.queue = []

    def enqueue(self, data: int) -> None:
        """
        此函数 enters 元素 到 该队列
        如果 该队列 是 已满 Exception 是 raised saying 超过 Flow!
        """
        if len(self.queue) == 100:
            raise OverFlowError("Maximum queue size is 100")
        self.queue.append(data)

    def dequeue(self) -> int:
        """
        返回 最高 优先级 元素 在 FIFO 顺序。
        如果 该队列 为空 则 under flow exception 是 raised。
        """
        if not self.queue:
            raise UnderFlowError("The queue is empty")
        data = min(self.queue)
        self.queue.remove(data)
        return data

    def __str__(self) -> str:
        """
        打印 所有 元素 之内 元素 优先队列
        """
        return str(self.queue)


def fixed_priority_queue() -> None:
    fpq = FixedPriorityQueue()
    fpq.enqueue(0, 10)
    fpq.enqueue(1, 70)
    fpq.enqueue(0, 100)
    fpq.enqueue(2, 1)
    fpq.enqueue(2, 5)
    fpq.enqueue(1, 7)
    fpq.enqueue(2, 4)
    fpq.enqueue(1, 64)
    fpq.enqueue(0, 128)
    print(fpq)
    print(fpq.dequeue())
    print(fpq.dequeue())
    print(fpq.dequeue())
    print(fpq.dequeue())
    print(fpq.dequeue())
    print(fpq)
    print(fpq.dequeue())
    print(fpq.dequeue())
    print(fpq.dequeue())
    print(fpq.dequeue())
    print(fpq.dequeue())


def element_priority_queue() -> None:
    epq = ElementPriorityQueue()
    epq.enqueue(10)
    epq.enqueue(70)
    epq.enqueue(100)
    epq.enqueue(1)
    epq.enqueue(5)
    epq.enqueue(7)
    epq.enqueue(4)
    epq.enqueue(64)
    epq.enqueue(128)
    print(epq)
    print(epq.dequeue())
    print(epq.dequeue())
    print(epq.dequeue())
    print(epq.dequeue())
    print(epq.dequeue())
    print(epq)
    print(epq.dequeue())
    print(epq.dequeue())
    print(epq.dequeue())
    print(epq.dequeue())
    print(epq.dequeue())


if __name__ == "__main__":
    fixed_priority_queue()
    element_priority_queue()
