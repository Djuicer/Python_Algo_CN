"""
Binomial 堆
引用: Advanced 数据 Structures，Peter Brass
"""


class Node:
    """
    节点 在 doubly-连接 binomial 树，包含：
        - 值
        - 大小 的 左子树
        - 链接 到 左，右 并且 父节点 节点
    """

    def __init__(self, val) -> None:
        self.val = val
        # 节点数量 在 左子树
        self.left_tree_size = 0
        self.left = None
        self.right = None
        self.parent = None

    def merge_trees(self, other):
        """
        在-位置 合并 的 两个 binomial 树 的 等于 大小。
        返回值 根节点 的 得到 树
        """
        assert self.left_tree_size == other.left_tree_size, "Unequal Sizes of Blocks"

        if self.val < other.val:
            other.left = self.right
            other.parent = None
            if self.right:
                self.right.parent = other
            self.right = other
            self.left_tree_size = self.left_tree_size * 2 + 1
            return self
        else:
            self.left = other.right
            self.parent = None
            if other.right:
                other.right.parent = self
            other.right = self
            other.left_tree_size = other.left_tree_size * 2 + 1
            return other


class BinomialHeap:
    r"""
    最小值-oriented 优先队列 implemented 带有 Binomial 堆 数据
    结构 implemented 带有 BinomialHeap 类. 它 supports：
        - 插入 元素 在 堆 带有 n 元素: 保证 logn，amoratized 1
        - 合并 (meld) heaps 的 大小 m 并且 n: O(logn + logm)
        - 删除 最小值: O(logn)
        - Peek (返回 最小值 不使用 deleting 它): O(1)

    示例：

    创建一个 随机 permutation 的 30 整数 到 为 已插入 并且 19 的 它们 已删除
    >>> import numpy as np
    >>> permutation = np.random.permutation(list(range(30)))

    创建一个 堆 并且 插入 30 整数
    __init__() 测试
    >>> first_heap = BinomialHeap()

    30 inserts - 插入() 测试
    >>> for number in permutation:
    ...     first_heap.insert(number)

    大小 测试
    >>> first_heap.size
    30

    Deleting - 删除() 测试
    >>> [int(first_heap.delete_min()) for _ in range(20)]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    创建一个 新 堆
    >>> second_heap = BinomialHeap()
    >>> vals = [17, 20, 31, 34]
    >>> for value in vals:
    ...     second_heap.insert(value)


    该堆 应 具有 following 结构：

                    17
                   /  \
                  #    31
                      /  \
                    20    34
                   /  \  /  \
                  #    # #   #

    前序() 测试
    >>> " ".join(str(x) for x in second_heap.pre_order())
    "(17, 0) ('#', 1) (31, 1) (20, 2) ('#', 3) ('#', 3) (34, 2) ('#', 3) ('#', 3)"

    printing 堆 - __str__() 测试
    >>> print(second_heap)
    17
    -#
    -31
    --20
    ---#
    ---#
    --34
    ---#
    ---#

    mergeHeaps() 测试
    >>>
    >>> merged = second_heap.merge_heaps(first_heap)
    >>> merged.peek()
    17

    值 在 合并后 堆; (合并 是 inplace)
    >>> results = []
    >>> while not first_heap.is_empty():
    ...     results.append(int(first_heap.delete_min()))
    >>> results
    [17, 20, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 34]
    """

    def __init__(self, bottom_root=None, min_node=None, heap_size=0) -> None:
        self.size = heap_size
        self.bottom_root = bottom_root
        self.min_node = min_node

    def merge_heaps(self, other):
        """
        在-位置 合并 的 两个 binomial heaps。
        两者 的 它们 become 得到 合并后 堆
        """

        # 空 heaps corner 情况
        if other.size == 0:
            return None
        if self.size == 0:
            self.size = other.size
            self.bottom_root = other.bottom_root
            self.min_node = other.min_node
            return None
        # 更新 大小
        self.size = self.size + other.size

        # 更新 最小值.节点
        if self.min_node.val > other.min_node.val:
            self.min_node = other.min_node
        # 合并

        # 顺序 roots 通过 left_subtree_size
        combined_roots_list = []
        i, j = self.bottom_root, other.bottom_root
        while i or j:
            if i and ((not j) or i.left_tree_size < j.left_tree_size):
                combined_roots_list.append((i, True))
                i = i.parent
            else:
                combined_roots_list.append((j, False))
                j = j.parent
        # 插入 links 之间 它们
        for i in range(len(combined_roots_list) - 1):
            if combined_roots_list[i][1] != combined_roots_list[i + 1][1]:
                combined_roots_list[i][0].parent = combined_roots_list[i + 1][0]
                combined_roots_list[i + 1][0].left = combined_roots_list[i][0]
        # Consecutively 合并 roots 带有 相同 left_tree_size
        i = combined_roots_list[0][0]
        while i.parent:
            if (
                (i.left_tree_size == i.parent.left_tree_size) and (not i.parent.parent)
            ) or (
                i.left_tree_size == i.parent.left_tree_size
                and i.left_tree_size != i.parent.parent.left_tree_size
            ):
                # Neighbouring 节点
                previous_node = i.left
                next_node = i.parent.parent

                # Merging 树
                i = i.merge_trees(i.parent)

                # 更新链接
                i.left = previous_node
                i.parent = next_node
                if previous_node:
                    previous_node.parent = i
                if next_node:
                    next_node.left = i
            else:
                i = i.parent
        # 更新 self.bottom_root
        while i.left:
            i = i.left
        self.bottom_root = i

        # 更新 另一个
        other.size = self.size
        other.bottom_root = self.bottom_root
        other.min_node = self.min_node

        # 返回 合并后 堆
        return self

    def insert(self, val) -> None:
        """
        插入一个 值 在 该堆
        """
        if self.size == 0:
            self.bottom_root = Node(val)
            self.size = 1
            self.min_node = self.bottom_root
        else:
            # 创建 新节点
            new_node = Node(val)

            # 更新 大小
            self.size += 1

            # 更新 min_node
            if val < self.min_node.val:
                self.min_node = new_node
            # Put new_node 作为 bottom_root 在 堆
            assert self.bottom_root is not None
            self.bottom_root.left = new_node
            new_node.parent = self.bottom_root
            self.bottom_root = new_node

            # Consecutively 合并 roots 带有 相同 left_tree_size
            while (
                self.bottom_root.parent
                and self.bottom_root.left_tree_size
                == self.bottom_root.parent.left_tree_size
            ):
                # 下一个节点
                next_node = self.bottom_root.parent.parent

                # 合并
                self.bottom_root = self.bottom_root.merge_trees(self.bottom_root.parent)

                # 更新 Links
                self.bottom_root.parent = next_node
                self.bottom_root.left = None
                if next_node:
                    next_node.left = self.bottom_root

    def peek(self):
        """
        返回 最小值 元素 不使用 deleting 它
        """
        return self.min_node.val

    def is_empty(self) -> bool:
        return self.size == 0

    def delete_min(self):
        """
        删除 最小值 元素 并且 返回 它
        """
        # assert 不 self.isEmpty()，"空 堆"

        # Save minimal 值
        min_value = self.min_node.val

        # 最后一个元素 在 堆 corner 情况
        if self.size == 1:
            # 更新 大小
            self.size = 0

            # 更新 底部 根节点
            self.bottom_root = None

            # 更新 min_node
            self.min_node = None

            return min_value
        # 没有 右子树 corner 情况
        # 结构 的树 implies 该 此 应 为 底部 根节点
        # 并且 其中 是 在 least 一个 另一个 根节点
        if self.min_node.right is None:
            # 更新 大小
            self.size -= 1

            # 更新 底部 根节点
            self.bottom_root = self.bottom_root.parent
            assert self.bottom_root is not None
            self.bottom_root.left = None

            # 更新 min_node
            self.min_node = self.bottom_root
            i = self.bottom_root.parent
            while i:
                if i.val < self.min_node.val:
                    self.min_node = i
                i = i.parent
            return min_value
        # General 情况
        # 查找 BinomialHeap 的 右子树 的 min_node
        bottom_of_new = self.min_node.right
        bottom_of_new.parent = None
        min_of_new = bottom_of_new
        size_of_new = 1

        # 大小，min_node 并且 bottom_root
        while bottom_of_new.left:
            size_of_new = size_of_new * 2 + 1
            bottom_of_new = bottom_of_new.left
            if bottom_of_new.val < min_of_new.val:
                min_of_new = bottom_of_new
        # Corner 情况 的 single 根节点 在 顶部 左 路径
        if (not self.min_node.left) and (not self.min_node.parent):
            self.size = size_of_new
            self.bottom_root = bottom_of_new
            self.min_node = min_of_new
            # 打印("Single 根节点，multiple 节点 情况")
            return min_value
        # 剩余 情况
        # Construct 堆 的 右子树
        new_heap = BinomialHeap(
            bottom_root=bottom_of_new, min_node=min_of_new, heap_size=size_of_new
        )

        # 更新 大小
        self.size = self.size - 1 - size_of_new

        # Neighbour 节点
        previous_node = self.min_node.left
        next_node = self.min_node.parent

        # 初始化 新 bottom_root 并且 min_node
        self.min_node = previous_node or next_node
        self.bottom_root = next_node

        # 更新 links 的 previous_node 并且 搜索 下方 用于 新 min_node 并且
        # bottom_root
        if previous_node:
            previous_node.parent = next_node

            # 更新 bottom_root 并且 搜索 min_node 下方
            self.bottom_root = previous_node
            self.min_node = previous_node
            while self.bottom_root.left:
                self.bottom_root = self.bottom_root.left
                if self.bottom_root.val < self.min_node.val:
                    self.min_node = self.bottom_root
        if next_node:
            next_node.left = previous_node

            # 搜索 新 min_node above min_node
            i = next_node
            while i:
                if i.val < self.min_node.val:
                    self.min_node = i
                i = i.parent
        # 合并 heaps
        self.merge_heaps(new_heap)

        return int(min_value)

    def pre_order(self):
        """
        返回值 Pre-顺序 表示 的堆 包括
        值 的 节点 plus 它们的 层级 距离 从 根节点;
        空 节点 appear 作为 #
        """
        # 查找 顶部 根节点
        top_root = self.bottom_root
        while top_root.parent:
            top_root = top_root.parent
        # 前序
        heap_pre_order = []
        self.__traversal(top_root, heap_pre_order)
        return heap_pre_order

    def __traversal(self, curr_node, preorder, level=0) -> None:
        """
        前序遍历 的 节点
        """
        if curr_node:
            preorder.append((curr_node.val, level))
            self.__traversal(curr_node.left, preorder, level + 1)
            self.__traversal(curr_node.right, preorder, level + 1)
        else:
            preorder.append(("#", level))

    def __str__(self) -> str:
        """
        Overwriting str 用于 pre-顺序 打印 的 节点 在 堆;
        Performance 是 poor，因此 使用 仅 用于 small 示例
        """
        if self.is_empty():
            return ""
        preorder_heap = self.pre_order()

        return "\n".join(("-" * level + str(value)) for value, level in preorder_heap)


# Unit 测试
if __name__ == "__main__":
    import doctest

    doctest.testmod()
