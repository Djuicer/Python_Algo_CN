class DynamicArray:
    def __init__(self) -> None:
        self.size = 0  # 数组中的元素数量
        self.capacity = 1  # 初始容量 的 该数组
        self.array = [None] * self.capacity  # 创建一个 数组 带有 初始容量

    def append(self, item: int) -> None:
        """
        该函数添加 元素 到 末尾 的 动态数组。

        运行时间 : O(1) 均摊
        空间: O(1) 均摊

        >>> arr = DynamicArray()
        >>> arr.append(1)
        >>> arr.append(2)
        >>> arr.append(3)
        >>> arr.array[:arr.size]  # Display only the filled part of the array
        [1, 2, 3]
        >>> arr.append(4)
        >>> arr.array[:arr.size]
        [1, 2, 3, 4]
        >>> arr.append(5)
        >>> arr.array[:arr.size]
        [1, 2, 3, 4, 5]
        """
        if self.size == self.capacity:
            self._resize(2 * self.capacity)  # Double 容量

        self.array[self.size] = item
        self.size += 1

    def _resize(self, new_capacity: int) -> None:
        """
        Resizes 该数组 到 新容量。

        运行时间 : O(n)
        空间: O(n)

        >>> arr = DynamicArray()
        >>> arr.append(1)
        >>> arr.append(2)
        >>> arr._resize(10)
        >>> arr.capacity
        10
        >>> arr.array[:arr.size]
        [1, 2]
        """
        new_array = [None] * new_capacity
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def get(self, index: int) -> int:
        """
        该函数返回 元素 在 指定索引。

        运行时间 : O(1)
        空间: O(1)

        >>> arr = DynamicArray()
        >>> arr.append(1)
        >>> arr.append(2)
        >>> arr.get(0)
        1
        >>> arr.get(1)
        2
        >>> arr.get(2)
        Traceback (most recent call last):
        ...
        IndexError: index out of range
        >>> arr.get(-1)
        Traceback (most recent call last):
        ...
        IndexError: index out of range
        """
        if index < 0 or index >= self.size:
            raise IndexError("index out of range")
        return self.array[index]

    def __setitem__(self, index: int, value: int) -> None:
        if index < 0 or index >= self.size:
            raise IndexError("index out of range")
        self.array[index] = value

    def __len__(self) -> int:
        """
        返回以下对象的数量： 元素 在 动态数组。

        运行时间 : O(1)
        空间: O(1)

        >>> arr = DynamicArray()
        >>> arr.append(1)
        >>> len(arr)
        1
        >>> arr.append(2)
        >>> len(arr)
        2
        >>> arr.append(3)
        >>> len(arr)
        3
        """
        return self.size

    def __str__(self) -> str:
        """
        返回以下对象的字符串表示： 动态数组。

        >>> arr = DynamicArray()
        >>> arr.append(1)
        >>> arr.append(2)
        >>> arr.append(3)
        >>> str(arr)
        '[1, 2, 3]'
        >>> arr.append(4)
        >>> str(arr)
        '[1, 2, 3, 4]'
        """
        return "[" + ", ".join(str(self.array[i]) for i in range(self.size)) + "]"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
