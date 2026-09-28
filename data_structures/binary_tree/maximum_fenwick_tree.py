class MaxFenwickTree:
    """
    最大值 树状数组

    More info: https://cp-algorithms.com/data_structures/fenwick.html
    ---------
    >>> ft = MaxFenwickTree(5)
    >>> ft.query(0, 5)
    0
    >>> ft.update(4, 100)
    >>> ft.query(0, 5)
    100
    >>> ft.update(4, 0)
    >>> ft.update(2, 20)
    >>> ft.query(0, 5)
    20
    >>> ft.update(4, 10)
    >>> ft.query(2, 5)
    20
    >>> ft.query(1, 5)
    20
    >>> ft.update(2, 0)
    >>> ft.query(0, 5)
    10
    >>> ft = MaxFenwickTree(10000)
    >>> ft.update(255, 30)
    >>> ft.query(0, 10000)
    30
    >>> ft = MaxFenwickTree(6)
    >>> ft.update(5, 1)
    >>> ft.query(5, 6)
    1
    >>> ft = MaxFenwickTree(6)
    >>> ft.update(0, 1000)
    >>> ft.query(0, 1)
    1000
    """

    def __init__(self, size: int) -> None:
        """
        创建 空 最大值 树状数组 带有 指定 大小

        参数：
            大小: 大小 的 数组

        返回值：
            None
        """
        self.size = size
        self.arr = [0] * size
        self.tree = [0] * size

    @staticmethod
    def get_next(index: int) -> int:
        """
        获取 下一个 索引 在 O(1)
        """
        return index | (index + 1)

    @staticmethod
    def get_prev(index: int) -> int:
        """
        获取 上一个 索引 在 O(1)
        """
        return (index & (index + 1)) - 1

    def update(self, index: int, value: int) -> None:
        """
        集合 索引 到 值 在 O(lg^2 N)

        参数：
            索引: 索引 到 更新
            值: 值 到 集合

        返回值：
            None
        """
        self.arr[index] = value
        while index < self.size:
            current_left_border = self.get_prev(index) + 1
            if current_left_border == index:
                self.tree[index] = value
            else:
                self.tree[index] = max(value, current_left_border, index)
            index = self.get_next(index)

    def query(self, left: int, right: int) -> int:
        """
        Answer 查询 的 最大值 范围 [l，r) 在 O(lg^2 N)

        参数：
            左: 左 索引 的 查询 范围 (inclusive)
            右: 右 索引 的 查询 范围 (exclusive)

        返回值：
            最大值 值 的 范围 [左，右)
        """
        right -= 1  # 因为 的 右 是 exclusive
        result = 0
        while left <= right:
            current_left = self.get_prev(right)
            if left <= current_left:
                result = max(result, self.tree[right])
                right = current_left
            else:
                result = max(result, self.arr[right])
                right -= 1
        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
