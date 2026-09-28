"""
Segment_tree 创建一个 线段树 带有 给定 数组 并且 函数,
allowing queries 到 为 done later 在 log(N) 时间
函数 takes 2 值 并且 返回值 相同 类型 值
"""

from collections.abc import Sequence
from queue import Queue


class SegmentTreeNode:
    def __init__(self, start, end, val, left=None, right=None) -> None:
        self.start = start
        self.end = end
        self.val = val
        self.mid = (start + end) // 2
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"SegmentTreeNode(start={self.start}, end={self.end}, val={self.val})"


class SegmentTree:
    """
    >>> import operator
    >>> num_arr = SegmentTree([2, 1, 5, 3, 4], operator.add)
    >>> tuple(num_arr.traverse())  # doctest: +NORMALIZE_WHITESPACE
    (SegmentTreeNode(start=0, end=4, val=15),
        SegmentTreeNode(start=0, end=2, val=8),
        SegmentTreeNode(start=3, end=4, val=7),
        SegmentTreeNode(start=0, end=1, val=3),
        SegmentTreeNode(start=2, end=2, val=5),
        SegmentTreeNode(start=3, end=3, val=3),
        SegmentTreeNode(start=4, end=4, val=4),
        SegmentTreeNode(start=0, end=0, val=2),
        SegmentTreeNode(start=1, end=1, val=1))
    >>>
    >>> num_arr.update(1, 5)
    >>> tuple(num_arr.traverse())  # doctest: +NORMALIZE_WHITESPACE
    (SegmentTreeNode(start=0, end=4, val=19),
        SegmentTreeNode(start=0, end=2, val=12),
        SegmentTreeNode(start=3, end=4, val=7),
        SegmentTreeNode(start=0, end=1, val=7),
        SegmentTreeNode(start=2, end=2, val=5),
        SegmentTreeNode(start=3, end=3, val=3),
        SegmentTreeNode(start=4, end=4, val=4),
        SegmentTreeNode(start=0, end=0, val=2),
        SegmentTreeNode(start=1, end=1, val=5))
    >>>
    >>> num_arr.query_range(3, 4)
    7
    >>> num_arr.query_range(2, 2)
    5
    >>> num_arr.query_range(1, 3)
    13
    >>>
    >>> max_arr = SegmentTree([2, 1, 5, 3, 4], max)
    >>> for node in max_arr.traverse():
    ...     print(node)
    ...
    SegmentTreeNode(start=0, end=4, val=5)
    SegmentTreeNode(start=0, end=2, val=5)
    SegmentTreeNode(start=3, end=4, val=4)
    SegmentTreeNode(start=0, end=1, val=2)
    SegmentTreeNode(start=2, end=2, val=5)
    SegmentTreeNode(start=3, end=3, val=3)
    SegmentTreeNode(start=4, end=4, val=4)
    SegmentTreeNode(start=0, end=0, val=2)
    SegmentTreeNode(start=1, end=1, val=1)
    >>>
    >>> max_arr.update(1, 5)
    >>> for node in max_arr.traverse():
    ...     print(node)
    ...
    SegmentTreeNode(start=0, end=4, val=5)
    SegmentTreeNode(start=0, end=2, val=5)
    SegmentTreeNode(start=3, end=4, val=4)
    SegmentTreeNode(start=0, end=1, val=5)
    SegmentTreeNode(start=2, end=2, val=5)
    SegmentTreeNode(start=3, end=3, val=3)
    SegmentTreeNode(start=4, end=4, val=4)
    SegmentTreeNode(start=0, end=0, val=2)
    SegmentTreeNode(start=1, end=1, val=5)
    >>>
    >>> max_arr.query_range(3, 4)
    4
    >>> max_arr.query_range(2, 2)
    5
    >>> max_arr.query_range(1, 3)
    5
    >>>
    >>> min_arr = SegmentTree([2, 1, 5, 3, 4], min)
    >>> for node in min_arr.traverse():
    ...     print(node)
    ...
    SegmentTreeNode(start=0, end=4, val=1)
    SegmentTreeNode(start=0, end=2, val=1)
    SegmentTreeNode(start=3, end=4, val=3)
    SegmentTreeNode(start=0, end=1, val=1)
    SegmentTreeNode(start=2, end=2, val=5)
    SegmentTreeNode(start=3, end=3, val=3)
    SegmentTreeNode(start=4, end=4, val=4)
    SegmentTreeNode(start=0, end=0, val=2)
    SegmentTreeNode(start=1, end=1, val=1)
    >>>
    >>> min_arr.update(1, 5)
    >>> for node in min_arr.traverse():
    ...     print(node)
    ...
    SegmentTreeNode(start=0, end=4, val=2)
    SegmentTreeNode(start=0, end=2, val=2)
    SegmentTreeNode(start=3, end=4, val=3)
    SegmentTreeNode(start=0, end=1, val=2)
    SegmentTreeNode(start=2, end=2, val=5)
    SegmentTreeNode(start=3, end=3, val=3)
    SegmentTreeNode(start=4, end=4, val=4)
    SegmentTreeNode(start=0, end=0, val=2)
    SegmentTreeNode(start=1, end=1, val=5)
    >>>
    >>> min_arr.query_range(3, 4)
    3
    >>> min_arr.query_range(2, 2)
    5
    >>> min_arr.query_range(1, 3)
    3
    >>>
    """

    def __init__(self, collection: Sequence, function) -> None:
        self.collection = collection
        self.fn = function
        if self.collection:
            self.root = self._build_tree(0, len(collection) - 1)

    def update(self, i, val) -> None:
        """
        更新 元素 在 log(N) 时间
        :param i: 位置 到 为 更新
        :param val: 新 值
        >>> import operator
        >>> num_arr = SegmentTree([2, 1, 5, 3, 4], operator.add)
        >>> num_arr.update(1, 5)
        >>> num_arr.query_range(1, 3)
        13
        """
        self._update_tree(self.root, i, val)

    def query_range(self, i, j):
        """
        获取 范围 查询 值 在 log(N) 时间
        :param i: 左 元素 索引
        :param j: 右 元素 索引
        :返回: 元素 combined 在 范围 [i，j]
        >>> import operator
        >>> num_arr = SegmentTree([2, 1, 5, 3, 4], operator.add)
        >>> num_arr.update(1, 5)
        >>> num_arr.query_range(3, 4)
        7
        >>> num_arr.query_range(2, 2)
        5
        >>> num_arr.query_range(1, 3)
        13
        >>>
        """
        return self._query_range(self.root, i, j)

    def _build_tree(self, start, end):
        if start == end:
            return SegmentTreeNode(start, end, self.collection[start])
        mid = (start + end) // 2
        left = self._build_tree(start, mid)
        right = self._build_tree(mid + 1, end)
        return SegmentTreeNode(start, end, self.fn(left.val, right.val), left, right)

    def _update_tree(self, node, i, val) -> None:
        if node.start == i and node.end == i:
            node.val = val
            return
        if i <= node.mid:
            self._update_tree(node.left, i, val)
        else:
            self._update_tree(node.right, i, val)
        node.val = self.fn(node.left.val, node.right.val)

    def _query_range(self, node, i, j):
        if node.start == i and node.end == j:
            return node.val

        if i <= node.mid:
            if j <= node.mid:
                # 范围 在 左子节点 树
                return self._query_range(node.left, i, j)
            else:
                # 范围 在 左子节点 树 并且 右子节点 树
                return self.fn(
                    self._query_range(node.left, i, node.mid),
                    self._query_range(node.right, node.mid + 1, j),
                )
        else:
            # 范围 在 右子节点 树
            return self._query_range(node.right, i, j)

    def traverse(self):
        if self.root is not None:
            queue = Queue()
            queue.put(self.root)
            while not queue.empty():
                node = queue.get()
                yield node

                if node.left is not None:
                    queue.put(node.left)

                if node.right is not None:
                    queue.put(node.right)


if __name__ == "__main__":
    import operator

    for fn in [operator.add, max, min]:
        print("*" * 50)
        arr = SegmentTree([2, 1, 5, 3, 4], fn)
        for node in arr.traverse():
            print(node)
        print()

        arr.update(1, 5)
        for node in arr.traverse():
            print(node)
        print()

        print(arr.query_range(3, 4))  # 7
        print(arr.query_range(2, 2))  # 5
        print(arr.query_range(1, 3))  # 13
        print()
