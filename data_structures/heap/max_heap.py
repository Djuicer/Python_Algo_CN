class BinaryHeap:
    """
    最大值-堆 实现 在 Python
    >>> binary_heap = BinaryHeap()
    >>> binary_heap.insert(6)
    >>> binary_heap.insert(10)
    >>> binary_heap.insert(15)
    >>> binary_heap.insert(12)
    >>> binary_heap.pop()
    15
    >>> binary_heap.pop()
    12
    >>> binary_heap.get_list
    [10, 6]
    >>> len(binary_heap)
    2
    """

    def __init__(self) -> None:
        self.__heap = [0]
        self.__size = 0

    def __swap_up(self, i: int) -> None:
        """交换 元素 向上"""
        temporary = self.__heap[i]
        while i // 2 > 0:
            if self.__heap[i] > self.__heap[i // 2]:
                self.__heap[i] = self.__heap[i // 2]
                self.__heap[i // 2] = temporary
            i //= 2

    def insert(self, value: int) -> None:
        """插入 新 元素"""
        self.__heap.append(value)
        self.__size += 1
        self.__swap_up(self.__size)

    def __swap_down(self, i: int) -> None:
        """交换 元素 down"""
        while self.__size >= 2 * i:
            if 2 * i + 1 > self.__size:  # noqa: SIM114
                bigger_child = 2 * i
            elif self.__heap[2 * i] > self.__heap[2 * i + 1]:
                bigger_child = 2 * i
            else:
                bigger_child = 2 * i + 1
            temporary = self.__heap[i]
            if self.__heap[i] < self.__heap[bigger_child]:
                self.__heap[i] = self.__heap[bigger_child]
                self.__heap[bigger_child] = temporary
            i = bigger_child

    def pop(self) -> int:
        """弹出 根节点 元素"""
        max_value = self.__heap[1]
        self.__heap[1] = self.__heap[self.__size]
        self.__size -= 1
        self.__heap.pop()
        self.__swap_down(1)
        return max_value

    @property
    def get_list(self) -> list:
        return self.__heap[1:]

    def __len__(self) -> int:
        """长度 的 该数组"""
        return self.__size


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # 创建一个 instance 的 BinaryHeap
    binary_heap = BinaryHeap()
    binary_heap.insert(6)
    binary_heap.insert(10)
    binary_heap.insert(15)
    binary_heap.insert(12)
    # 弹出 根节点(最大值-值 因为 它 是 最大值 堆)
    print(binary_heap.pop())  # 15
    print(binary_heap.pop())  # 12
    # 获取 该列表 并且 大小 之后 操作
    print(binary_heap.get_list)
    print(len(binary_heap))
