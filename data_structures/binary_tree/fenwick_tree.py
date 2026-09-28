from copy import deepcopy


class FenwickTree:
    """
    树状数组

    More info: https://en.wikipedia.org/wiki/Fenwick_tree
    """

    def __init__(self, arr: list[int] | None = None, size: int | None = None) -> None:
        """
        Constructor 用于 树状数组

        参数：
            arr (列表): 列表 的 元素 到 初始化 该树 带有 (可选)
            大小 (int): 大小 的 树状数组 (如果 arr 是 None)
        """

        if arr is None and size is not None:
            self.size = size
            self.tree = [0] * size
        elif arr is not None:
            self.init(arr)
        else:
            raise ValueError("Either arr or size must be specified")

    def init(self, arr: list[int]) -> None:
        """
        初始化 树状数组 带有 arr 在 O(N)

        参数：
            arr (列表): 列表 的 元素 到 初始化 该树 带有

        返回值：
            None

        >>> a = [1, 2, 3, 4, 5]
        >>> f1 = FenwickTree(a)
        >>> f2 = FenwickTree(size=len(a))
        >>> for index, value in enumerate(a):
        ...     f2.add(index, value)
        >>> f1.tree == f2.tree
        True
        """
        self.size = len(arr)
        self.tree = deepcopy(arr)
        for i in range(1, self.size):
            j = self.next_(i)
            if j < self.size:
                self.tree[j] += self.tree[i]

    def get_array(self) -> list[int]:
        """
        获取 Normal 数组 的 树状数组 在 O(N)

        返回值：
            列表: Normal 数组 的 树状数组

        >>> a = [i for i in range(128)]
        >>> f = FenwickTree(a)
        >>> f.get_array() == a
        True
        """
        arr = self.tree[:]
        for i in range(self.size - 1, 0, -1):
            j = self.next_(i)
            if j < self.size:
                arr[j] -= arr[i]
        return arr

    @staticmethod
    def next_(index: int) -> int:
        return index + (index & (-index))

    @staticmethod
    def prev(index: int) -> int:
        return index - (index & (-index))

    def add(self, index: int, value: int) -> None:
        """
        添加 一个值 到 索引 在 O(lg N)

        参数：
            索引 (int): 索引 到 添加 值 到
            值 (int): 值 到 添加 到 索引

        返回值：
            None

        >>> f = FenwickTree([1, 2, 3, 4, 5])
        >>> f.add(0, 1)
        >>> f.add(1, 2)
        >>> f.add(2, 3)
        >>> f.add(3, 4)
        >>> f.add(4, 5)
        >>> f.get_array()
        [2, 4, 6, 8, 10]
        """
        if index == 0:
            self.tree[0] += value
            return
        while index < self.size:
            self.tree[index] += value
            index = self.next_(index)

    def update(self, index: int, value: int) -> None:
        """
        集合 该值 的 索引 在 O(lg N)

        参数：
            索引 (int): 索引 到 集合 值 到
            值 (int): 值 到 集合 在 索引

        返回值：
            None

        >>> f = FenwickTree([5, 4, 3, 2, 1])
        >>> f.update(0, 1)
        >>> f.update(1, 2)
        >>> f.update(2, 3)
        >>> f.update(3, 4)
        >>> f.update(4, 5)
        >>> f.get_array()
        [1, 2, 3, 4, 5]
        """
        self.add(index, value - self.get(index))

    def prefix(self, right: int) -> int:
        """
        前缀 和 的 所有元素 在 [0，右) 在 O(lg N)

        参数：
            右 (int): 右 bound 的 查询 (exclusive)

        返回值：
            int: 和 的 所有元素 在 [0，右)

        >>> a = [i for i in range(128)]
        >>> f = FenwickTree(a)
        >>> res = True
        >>> for i in range(len(a)):
        ...     res = res and f.prefix(i) == sum(a[:i])
        >>> res
        True
        """
        if right == 0:
            return 0
        result = self.tree[0]
        right -= 1  # 使 右 inclusive
        while right > 0:
            result += self.tree[right]
            right = self.prev(right)
        return result

    def query(self, left: int, right: int) -> int:
        """
        查询 和 的 所有元素 在 [左，右) 在 O(lg N)

        参数：
            左 (int): 左 bound 的 查询 (inclusive)
            右 (int): 右 bound 的 查询 (exclusive)

        返回值：
            int: 和 的 所有元素 在 [左，右)

        >>> a = [i for i in range(128)]
        >>> f = FenwickTree(a)
        >>> res = True
        >>> for i in range(len(a)):
        ...     for j in range(i + 1, len(a)):
        ...         res = res and f.query(i, j) == sum(a[i:j])
        >>> res
        True
        """
        return self.prefix(right) - self.prefix(left)

    def get(self, index: int) -> int:
        """
        获取 值 在 索引 在 O(lg N)

        参数：
            索引 (int): 索引 到 获取 该值

        返回值：
            int: 值 的 元素 在 索引

        >>> a = [i for i in range(128)]
        >>> f = FenwickTree(a)
        >>> res = True
        >>> for i in range(len(a)):
        ...     res = res and f.get(i) == a[i]
        >>> res
        True
        """
        return self.query(index, index + 1)

    def rank_query(self, value: int) -> int:
        """
        查找 最大 索引 带有 前缀(i) <= 值 在 O(lg N)
        NOTE: Requires 该 所有 值 是 非-负!

        参数：
            值 (int): 值 到 查找 最大 索引 的

        返回值：
            -1: 如果 值 是 更小 比 所有元素 在 前缀 和
            int: 最大 索引 带有 前缀(i) <= 值

        >>> f = FenwickTree([1, 2, 0, 3, 0, 5])
        >>> f.rank_query(0)
        -1
        >>> f.rank_query(2)
        0
        >>> f.rank_query(1)
        0
        >>> f.rank_query(3)
        2
        >>> f.rank_query(5)
        2
        >>> f.rank_query(6)
        4
        >>> f.rank_query(11)
        5
        """
        value -= self.tree[0]
        if value < 0:
            return -1

        j = 1  # 最大 power 的 2 <= 大小
        while j * 2 < self.size:
            j *= 2

        i = 0

        while j > 0:
            if i + j < self.size and self.tree[i + j] <= value:
                value -= self.tree[i + j]
                i += j
            j //= 2
        return i


if __name__ == "__main__":
    import doctest

    doctest.testmod()
