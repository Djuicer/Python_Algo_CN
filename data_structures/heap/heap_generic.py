from collections.abc import Callable


class Heap:
    """
    generic 堆 类，可以 为 使用 作为 最小值 或 最大值 通过 passing 该键 函数
    accordingly.
    """

    def __init__(self, key: Callable | None = None) -> None:
        # 存储 actual 堆 元素。
        self.arr: list = []
        # 存储 indexes 的 每个 元素 用于 supporting updates 并且 删除。
        self.pos_map: dict = {}
        # 存储 当前 大小 的 堆。
        self.size = 0
        # 存储 函数 使用 到 evaluate score 的 元素 在 其 basis ordering
        # 将 为 done。
        self.key = key or (lambda x: x)

    def _parent(self, i: int) -> int | None:
        """返回值 父节点 索引 的 给定 索引 如果 存在 否则 None"""
        return int((i - 1) / 2) if i > 0 else None

    def _left(self, i: int) -> int | None:
        """返回值 左-子节点-索引 的 给定 索引 如果 存在 否则 None"""
        left = int(2 * i + 1)
        return left if 0 < left < self.size else None

    def _right(self, i: int) -> int | None:
        """返回值 右-子节点-索引 的 给定 索引 如果 存在 否则 None"""
        right = int(2 * i + 2)
        return right if 0 < right < self.size else None

    def _swap(self, i: int, j: int) -> None:
        """执行 changes 所需 用于 swapping 两个 元素 在 该堆"""
        # 第一个 更新 indexes 的 元素 在 索引 map。
        self.pos_map[self.arr[i][0]], self.pos_map[self.arr[j][0]] = (
            self.pos_map[self.arr[j][0]],
            self.pos_map[self.arr[i][0]],
        )
        # 则 交换 元素 在 该列表。
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    def _cmp(self, i: int, j: int) -> bool:
        """Compares 两个 元素 使用 default 比较"""
        return self.arr[i][1] < self.arr[j][1]

    def _get_valid_parent(self, i: int) -> int:
        """
        返回值 索引 的 有效 父节点 作为 per 所需 ordering among 给定 索引 并且
        两者 它's 子节点
        """
        left = self._left(i)
        right = self._right(i)
        valid_parent = i

        if left is not None and not self._cmp(left, valid_parent):
            valid_parent = left
        if right is not None and not self._cmp(right, valid_parent):
            valid_parent = right

        return valid_parent

    def _heapify_up(self, index: int) -> None:
        """Fixes 该堆 在 upward 方向 的 给定 索引"""
        parent = self._parent(index)
        while parent is not None and not self._cmp(index, parent):
            self._swap(index, parent)
            index, parent = parent, self._parent(parent)

    def _heapify_down(self, index: int) -> None:
        """Fixes 该堆 在 downward 方向 的 给定 索引"""
        valid_parent = self._get_valid_parent(index)
        while valid_parent != index:
            self._swap(index, valid_parent)
            index, valid_parent = valid_parent, self._get_valid_parent(valid_parent)

    def update_item(self, item: int, item_value: int) -> None:
        """Updates 给定 元素 值 在 堆 如果 存在"""
        if item not in self.pos_map:
            return
        index = self.pos_map[item]
        self.arr[index] = [item, self.key(item_value)]
        # 使 确保 堆 是 右 在 两者 向上 并且 down 方向。
        # Ideally 仅 一个 的 它们 将 使 任意 更改。
        self._heapify_up(index)
        self._heapify_down(index)

    def delete_item(self, item: int) -> None:
        """Deletes 给定 元素 从 堆 如果 存在"""
        if item not in self.pos_map:
            return
        index = self.pos_map[item]
        del self.pos_map[item]
        self.arr[index] = self.arr[self.size - 1]
        self.pos_map[self.arr[self.size - 1][0]] = index
        self.size -= 1
        # 使 确保 堆 是 右 在 两者 向上 并且 down 方向. Ideally 仅 一个
        # 的 它们 将 使 任意 更改- 因此 没有 performance loss 在 calling 两者。
        if self.size > index:
            self._heapify_up(index)
            self._heapify_down(index)

    def insert_item(self, item: int, item_value: int) -> None:
        """Inserts 给定 元素 带有 给定 值 在 堆"""
        arr_len = len(self.arr)
        if arr_len == self.size:
            self.arr.append([item, self.key(item_value)])
        else:
            self.arr[self.size] = [item, self.key(item_value)]
        self.pos_map[item] = self.size
        self.size += 1
        self._heapify_up(self.size - 1)

    def get_top(self) -> tuple | None:
        """返回值 顶部 元素 元组 (计算得出 值，元素) 从 堆 如果 存在"""
        return self.arr[0] if self.size else None

    def extract_top(self) -> tuple | None:
        """
        返回 顶部 元素 元组 (计算得出 值，元素) 从 堆 并且 removes 它 作为 well
        如果 存在
        """
        top_item_tuple = self.get_top()
        if top_item_tuple:
            self.delete_item(top_item_tuple[0])
        return top_item_tuple


def test_heap() -> None:
    """
    >>> h = Heap()  # Max-heap
    >>> h.insert_item(5, 34)
    >>> h.insert_item(6, 31)
    >>> h.insert_item(7, 37)
    >>> h.get_top()
    [7, 37]
    >>> h.extract_top()
    [7, 37]
    >>> h.extract_top()
    [5, 34]
    >>> h.extract_top()
    [6, 31]
    >>> h = Heap(key=lambda x: -x)  # Min heap
    >>> h.insert_item(5, 34)
    >>> h.insert_item(6, 31)
    >>> h.insert_item(7, 37)
    >>> h.get_top()
    [6, -31]
    >>> h.extract_top()
    [6, -31]
    >>> h.extract_top()
    [5, -34]
    >>> h.extract_top()
    [7, -37]
    >>> h.insert_item(8, 45)
    >>> h.insert_item(9, 40)
    >>> h.insert_item(10, 50)
    >>> h.get_top()
    [9, -40]
    >>> h.update_item(10, 30)
    >>> h.get_top()
    [10, -30]
    >>> h.delete_item(10)
    >>> h.get_top()
    [9, -40]
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
