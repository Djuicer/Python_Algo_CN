from __future__ import annotations

from collections.abc import Iterator


class RedBlackTree:
    """
    红色-黑色 树，其 是 self-balancing BST (binary 搜索
    树)。
    此 树 具有 similar performance 到 AVL 树，但是 balancing 是
    较小 strict，因此 它 将 执行 faster 用于 writing/deleting 节点
    并且 slower 用于 reading 在 平均情况，though，因为 they're
    两者 balanced binary 搜索 树，两者 将 获取 相同 asymptotic
    performance.
    To read more about them, https://en.wikipedia.org/wiki/Red-black_tree
    Unless 否则 指定，所有 asymptotic runtimes 是 指定 在
    terms 的 大小 的树。
    """

    def __init__(
        self,
        label: int | None = None,
        color: int = 0,
        parent: RedBlackTree | None = None,
        left: RedBlackTree | None = None,
        right: RedBlackTree | None = None,
    ) -> None:
        """初始化 新 红色-黑色 树 节点 带有 给定 值：
        标签: 该值 associated 带有 此 节点
        color: 0 如果 黑色，1 如果 红色
        父节点: 父节点 到 此 节点
        左: 此 节点's 左子节点
        右: 此 节点's 右子节点
        """
        self.label = label
        self.parent = parent
        self.left = left
        self.right = right
        self.color = color

    # 此处 是 函数 其 是 specific 到 红色-黑色 树

    def rotate_left(self) -> RedBlackTree:
        """旋转 子树 rooted 在 此 节点 到 左 并且
        返回值 新 根节点 到 此 子树。
        Performing 一个 旋转 可以 为 done 在 O(1)。
        """
        parent = self.parent
        right = self.right
        if right is None:
            return self
        self.right = right.left
        if self.right:
            self.right.parent = self
        self.parent = right
        right.left = self
        if parent is not None:
            if parent.left == self:
                parent.left = right
            else:
                parent.right = right
        right.parent = parent
        return right

    def rotate_right(self) -> RedBlackTree:
        """旋转 子树 rooted 在 此 节点 到 右 并且
        返回值 新 根节点 到 此 子树。
        Performing 一个 旋转 可以 为 done 在 O(1)。
        """
        if self.left is None:
            return self
        parent = self.parent
        left = self.left
        self.left = left.right
        if self.left:
            self.left.parent = self
        self.parent = left
        left.right = self
        if parent is not None:
            if parent.right is self:
                parent.right = left
            else:
                parent.left = left
        left.parent = parent
        return left

    def insert(self, label: int) -> RedBlackTree:
        """Inserts 标签 到 子树 rooted 在 self，执行 任意
        rotations necessary 到 maintain balance，并且 则 返回值
        新 根节点 到 此 子树 (likely self)。
        此 是 保证 到 运行 在 O(log(n)) 时间。
        """
        if self.label is None:
            # 仅 可能 带有 空树
            self.label = label
            return self
        if self.label == label:
            return self
        elif self.label > label:
            if self.left:
                self.left.insert(label)
            else:
                self.left = RedBlackTree(label, 1, self)
                self.left._insert_repair()
        elif self.right:
            self.right.insert(label)
        else:
            self.right = RedBlackTree(label, 1, self)
            self.right._insert_repair()
        return self.parent or self

    def _insert_repair(self) -> None:
        """Repair coloring 从 inserting 到 树。"""
        if self.parent is None:
            # 此 节点 是 根节点，因此 它 仅 needs 到 为 黑色
            self.color = 0
        elif color(self.parent) == 0:
            # 如果 父节点 是 黑色，则 它 仅 needs 到 为 红色
            self.color = 1
        else:
            uncle = self.parent.sibling
            if color(uncle) == 0:
                if self.is_left() and self.parent.is_right():
                    self.parent.rotate_right()
                    if self.right:
                        self.right._insert_repair()
                elif self.is_right() and self.parent.is_left():
                    self.parent.rotate_left()
                    if self.left:
                        self.left._insert_repair()
                elif self.is_left():
                    if self.grandparent:
                        self.grandparent.rotate_right()
                        self.parent.color = 0
                    if self.parent.right:
                        self.parent.right.color = 1
                else:
                    if self.grandparent:
                        self.grandparent.rotate_left()
                        self.parent.color = 0
                    if self.parent.left:
                        self.parent.left.color = 1
            else:
                self.parent.color = 0
                if uncle and self.grandparent:
                    uncle.color = 0
                    self.grandparent.color = 1
                    self.grandparent._insert_repair()

    def remove(self, label: int) -> RedBlackTree:
        """移除 标签 从 此 树。"""
        if self.label == label:
            if self.left and self.right:
                # 它's easier 到 balance 一个节点 带有 在 most 一个 子节点,
                # 因此 我们 replace 此 节点 带有 greatest 一个 较小 比
                # 它 并且 移除 该。
                value = self.left.get_max()
                if value is not None:
                    self.label = value
                    self.left.remove(value)
            else:
                # 此 节点 具有 在 most 一个 非-None 子节点，因此 我们 don't
                # need 到 replace
                child = self.left or self.right
                if self.color == 1:
                    # 此 节点 是 红色，并且 其 子节点 是 黑色
                    # 仅 way 此 happens 到 一个节点 带有 一个 子节点
                    # 是 如果 两者 子节点 是 None 叶节点。
                    # 我们 可以 仅 移除 此 节点 并且 call 它 day。
                    if self.parent:
                        if self.is_left():
                            self.parent.left = None
                        else:
                            self.parent.right = None
                # 该节点 是 黑色
                elif child is None:
                    # 此 节点 并且 其 子节点 是 黑色
                    if self.parent is None:
                        # 该树 是 现在 空
                        return RedBlackTree(None)
                    else:
                        self._remove_repair()
                        if self.is_left():
                            self.parent.left = None
                        else:
                            self.parent.right = None
                        self.parent = None
                else:
                    # 此 节点 是 黑色 并且 其 子节点 是 红色
                    # 移动 子节点 此处 并且 使 它 黑色
                    self.label = child.label
                    self.left = child.left
                    self.right = child.right
                    if self.left:
                        self.left.parent = self
                    if self.right:
                        self.right.parent = self
        elif self.label is not None and self.label > label:
            if self.left:
                self.left.remove(label)
        elif self.right:
            self.right.remove(label)
        return self.parent or self

    def _remove_repair(self) -> None:
        """Repair coloring 的树 该 may 具有 been messed 向上。"""
        if (
            self.parent is None
            or self.sibling is None
            or self.parent.sibling is None
            or self.grandparent is None
        ):
            return
        if color(self.sibling) == 1:
            self.sibling.color = 0
            self.parent.color = 1
            if self.is_left():
                self.parent.rotate_left()
            else:
                self.parent.rotate_right()
        if (
            color(self.parent) == 0
            and color(self.sibling) == 0
            and color(self.sibling.left) == 0
            and color(self.sibling.right) == 0
        ):
            self.sibling.color = 1
            self.parent._remove_repair()
            return
        if (
            color(self.parent) == 1
            and color(self.sibling) == 0
            and color(self.sibling.left) == 0
            and color(self.sibling.right) == 0
        ):
            self.sibling.color = 1
            self.parent.color = 0
            return
        if (
            self.is_left()
            and color(self.sibling) == 0
            and color(self.sibling.right) == 0
            and color(self.sibling.left) == 1
        ):
            self.sibling.rotate_right()
            self.sibling.color = 0
            if self.sibling.right:
                self.sibling.right.color = 1
        if (
            self.is_right()
            and color(self.sibling) == 0
            and color(self.sibling.right) == 1
            and color(self.sibling.left) == 0
        ):
            self.sibling.rotate_left()
            self.sibling.color = 0
            if self.sibling.left:
                self.sibling.left.color = 1
        if (
            self.is_left()
            and color(self.sibling) == 0
            and color(self.sibling.right) == 1
        ):
            self.parent.rotate_left()
            self.grandparent.color = self.parent.color
            self.parent.color = 0
            self.parent.sibling.color = 0
        if (
            self.is_right()
            and color(self.sibling) == 0
            and color(self.sibling.left) == 1
        ):
            self.parent.rotate_right()
            self.grandparent.color = self.parent.color
            self.parent.color = 0
            self.parent.sibling.color = 0

    def check_color_properties(self) -> bool:
        """检查 coloring 的树，并且 返回 True iff 该树
        是 colored 在 way 其 matches 这些 five properties：
        (wording stolen from wikipedia article)
         1. 每个节点 是 任一 红色 或 黑色。
         2. 根节点 是 黑色。
         3. 所有 叶节点 是 黑色。
         4. 如果 一个节点 是 红色，则 两者 其 子节点 是 黑色。
         5. 每个 路径 从 任意 节点 到 所有 的 其 descendent NIL 节点
            具有 相同 数 的 黑色 节点。
        此函数 runs 在 O(n) 时间，因为 properties 4 并且 5 take
        该 long 到 检查。
        """
        # I assume property 1 到 hold 因为 其中 是 nothing 该 可以
        # 使 color 为 anything 另一个 比 0 或 1。
        # 性质 2
        if self.color:
            # 根节点 曾是 红色
            print("Property 2")
            return False
        # Property 3 does 不 need 到 为 checked，因为 None 是 assumed
        # 到 为 黑色 并且 是 所有 叶节点。
        # 性质 4
        if not self.check_coloring():
            print("Property 4")
            return False
        # 性质 5
        if self.black_height() is None:
            print("Property 5")
            return False
        # 所有 properties were met
        return True

    def check_coloring(self) -> bool:
        """helper 函数 到 递归地 检查 Property 4 的
        红色-黑色 树. See check_color_properties 用于 更多 info。
        """
        if self.color == 1 and 1 in (color(self.left), color(self.right)):
            return False
        if self.left and not self.left.check_coloring():
            return False
        return not (self.right and not self.right.check_coloring())

    def black_height(self) -> int | None:
        """返回以下对象的数量： 黑色 节点 从 此 节点 到
        叶节点 的树，或 None 如果 其中 isn't 一个 such 值 (
        树 是 color incorrectly)。
        """
        if self is None or self.left is None or self.right is None:
            # 如果 我们're 已经 在 叶节点，其中 是 没有 路径
            return 1
        left = RedBlackTree.black_height(self.left)
        right = RedBlackTree.black_height(self.right)
        if left is None or right is None:
            # 其中 是 issues 带有 coloring 下方 子节点 节点
            return None
        if left != right:
            # 两个 子节点 具有 unequal depths
            return None
        # 返回 黑色 深度 的 子节点，plus 一个 如果 此 节点 是
        # 黑色
        return left + (1 - self.color)

    # 此处 是 函数 其 是 general 到 所有 binary 搜索 树

    def __contains__(self, label: int) -> bool:
        """搜索 通过 该树 用于 标签，returning True iff 它 是
        找到 somewhere 在 该树。
        保证 到 运行 在 O(log(n)) 时间。
        """
        return self.search(label) is not None

    def search(self, label: int) -> RedBlackTree | None:
        """搜索 通过 该树 用于 标签，returning 其 节点 如果
        它's 找到，并且 None 否则。
        此方法 是 保证 到 运行 在 O(log(n)) 时间。
        """
        if self.label == label:
            return self
        elif self.label is not None and label > self.label:
            if self.right is None:
                return None
            else:
                return self.right.search(label)
        elif self.left is None:
            return None
        else:
            return self.left.search(label)

    def floor(self, label: int) -> int | None:
        """返回值 最大 元素 在 此 树 其 是 在 most 标签。
        此方法 是 保证 到 运行 在 O(log(n)) 时间。"""
        if self.label == label:
            return self.label
        elif self.label is not None and self.label > label:
            if self.left:
                return self.left.floor(label)
            else:
                return None
        else:
            if self.right:
                attempt = self.right.floor(label)
                if attempt is not None:
                    return attempt
            return self.label

    def ceil(self, label: int) -> int | None:
        """返回值 最小 元素 在 此 树 其 是 在 least 标签。
        此方法 是 保证 到 运行 在 O(log(n)) 时间。
        """
        if self.label == label:
            return self.label
        elif self.label is not None and self.label < label:
            if self.right:
                return self.right.ceil(label)
            else:
                return None
        else:
            if self.left:
                attempt = self.left.ceil(label)
                if attempt is not None:
                    return attempt
            return self.label

    def get_max(self) -> int | None:
        """返回值 最大 元素 在 此 树。
        此方法 是 保证 到 运行 在 O(log(n)) 时间。
        """
        if self.right:
            # 前进 作为 far 右 作为 可能
            return self.right.get_max()
        else:
            return self.label

    def get_min(self) -> int | None:
        """返回值 最小 元素 在 此 树。
        此方法 是 保证 到 运行 在 O(log(n)) 时间。
        """
        if self.left:
            # 前进 作为 far 左 作为 可能
            return self.left.get_min()
        else:
            return self.label

    @property
    def grandparent(self) -> RedBlackTree | None:
        """获取 当前节点's grandparent，或 None 如果 它 doesn't exist。"""
        if self.parent is None:
            return None
        else:
            return self.parent.parent

    @property
    def sibling(self) -> RedBlackTree | None:
        """获取 当前节点's sibling，或 None 如果 它 doesn't exist。"""
        if self.parent is None:
            return None
        elif self.parent.left is self:
            return self.parent.right
        else:
            return self.parent.left

    def is_left(self) -> bool:
        """返回值 true iff 此 节点 是 左子节点 的 其 父节点。"""
        if self.parent is None:
            return False
        return self.parent.left is self

    def is_right(self) -> bool:
        """返回值 true iff 此 节点 是 右子节点 的 其 父节点。"""
        if self.parent is None:
            return False
        return self.parent.right is self

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        """
        返回以下对象的数量： 节点 在 此 树。
        """
        ln = 1
        if self.left:
            ln += len(self.left)
        if self.right:
            ln += len(self.right)
        return ln

    def preorder_traverse(self) -> Iterator[int | None]:
        yield self.label
        if self.left:
            yield from self.left.preorder_traverse()
        if self.right:
            yield from self.right.preorder_traverse()

    def inorder_traverse(self) -> Iterator[int | None]:
        if self.left:
            yield from self.left.inorder_traverse()
        yield self.label
        if self.right:
            yield from self.right.inorder_traverse()

    def postorder_traverse(self) -> Iterator[int | None]:
        if self.left:
            yield from self.left.postorder_traverse()
        if self.right:
            yield from self.right.postorder_traverse()
        yield self.label

    def __repr__(self) -> str:
        from pprint import pformat

        if self.left is None and self.right is None:
            return f"'{self.label} {(self.color and 'red') or 'blk'}'"
        return pformat(
            {
                f"{self.label} {(self.color and 'red') or 'blk'}": (
                    self.left,
                    self.right,
                )
            },
            indent=1,
        )

    def __eq__(self, other: object) -> bool:
        """测试 如果 两个 树 是 等于。"""
        if not isinstance(other, RedBlackTree):
            return NotImplemented
        if self.label == other.label:
            return self.left == other.left and self.right == other.right
        else:
            return False


def color(node: RedBlackTree | None) -> int:
    """返回值 color 的 一个节点，allowing 用于 None 叶节点。"""
    if node is None:
        return 0
    else:
        return node.color


"""
Code for testing the various
functions of the red-black tree.
"""


def test_rotations() -> bool:
    """测试 该 rotate_left 并且 rotate_right 函数 work。"""
    # 使 树 到 测试 在
    tree = RedBlackTree(0)
    tree.left = RedBlackTree(-10, parent=tree)
    tree.right = RedBlackTree(10, parent=tree)
    tree.left.left = RedBlackTree(-20, parent=tree.left)
    tree.left.right = RedBlackTree(-5, parent=tree.left)
    tree.right.left = RedBlackTree(5, parent=tree.right)
    tree.right.right = RedBlackTree(20, parent=tree.right)
    # 使 右 旋转
    left_rot = RedBlackTree(10)
    left_rot.left = RedBlackTree(0, parent=left_rot)
    left_rot.left.left = RedBlackTree(-10, parent=left_rot.left)
    left_rot.left.right = RedBlackTree(5, parent=left_rot.left)
    left_rot.left.left.left = RedBlackTree(-20, parent=left_rot.left.left)
    left_rot.left.left.right = RedBlackTree(-5, parent=left_rot.left.left)
    left_rot.right = RedBlackTree(20, parent=left_rot)
    tree = tree.rotate_left()
    if tree != left_rot:
        return False
    tree = tree.rotate_right()
    tree = tree.rotate_right()
    # 使 左 旋转
    right_rot = RedBlackTree(-10)
    right_rot.left = RedBlackTree(-20, parent=right_rot)
    right_rot.right = RedBlackTree(0, parent=right_rot)
    right_rot.right.left = RedBlackTree(-5, parent=right_rot.right)
    right_rot.right.right = RedBlackTree(10, parent=right_rot.right)
    right_rot.right.right.left = RedBlackTree(5, parent=right_rot.right.right)
    right_rot.right.right.right = RedBlackTree(20, parent=right_rot.right.right)
    return tree == right_rot


def test_insertion_speed() -> bool:
    """测试 该 该树 balances inserts 到 O(log(n)) 通过 doing lot
    的 它们。
    """
    tree = RedBlackTree(-1)
    for i in range(300000):
        tree = tree.insert(i)
    return True


def test_insert() -> bool:
    """测试 插入() 方法 的树 correctly balances，colors,
    并且 inserts。
    """
    tree = RedBlackTree(0)
    tree.insert(8)
    tree.insert(-8)
    tree.insert(4)
    tree.insert(12)
    tree.insert(10)
    tree.insert(11)
    ans = RedBlackTree(0, 0)
    ans.left = RedBlackTree(-8, 0, ans)
    ans.right = RedBlackTree(8, 1, ans)
    ans.right.left = RedBlackTree(4, 0, ans.right)
    ans.right.right = RedBlackTree(11, 0, ans.right)
    ans.right.right.left = RedBlackTree(10, 1, ans.right.right)
    ans.right.right.right = RedBlackTree(12, 1, ans.right.right)
    return tree == ans


def test_insert_and_search() -> bool:
    """测试 搜索 通过 该树 用于 值。"""
    tree = RedBlackTree(0)
    tree.insert(8)
    tree.insert(-8)
    tree.insert(4)
    tree.insert(12)
    tree.insert(10)
    tree.insert(11)
    if any(i in tree for i in (5, -6, -10, 13)):
        # 找到 something 不 在 其中
        return False
    # 查找所有 这些 things 在 其中
    return all(i in tree for i in (11, 12, -8, 0))


def test_insert_delete() -> bool:
    """测试 插入() 并且 删除() 方法 的树，verifying
    插入 并且 removal 的 元素，并且 balancing 的树。
    """
    tree = RedBlackTree(0)
    tree = tree.insert(-12)
    tree = tree.insert(8)
    tree = tree.insert(-8)
    tree = tree.insert(15)
    tree = tree.insert(4)
    tree = tree.insert(12)
    tree = tree.insert(10)
    tree = tree.insert(9)
    tree = tree.insert(11)
    tree = tree.remove(15)
    tree = tree.remove(-12)
    tree = tree.remove(9)
    if not tree.check_color_properties():
        return False
    return list(tree.inorder_traverse()) == [-8, 0, 4, 8, 10, 11, 12]


def test_floor_ceil() -> bool:
    """测试 floor 并且 ceiling 函数 在 该树。"""
    tree = RedBlackTree(0)
    tree.insert(-16)
    tree.insert(16)
    tree.insert(8)
    tree.insert(24)
    tree.insert(20)
    tree.insert(22)
    tuples = [(-20, None, -16), (-10, -16, 0), (8, 8, 8), (50, 24, None)]
    for val, floor, ceil in tuples:
        if tree.floor(val) != floor or tree.ceil(val) != ceil:
            return False
    return True


def test_min_max() -> bool:
    """测试 最小值 并且 最大值 函数 在 该树。"""
    tree = RedBlackTree(0)
    tree.insert(-16)
    tree.insert(16)
    tree.insert(8)
    tree.insert(24)
    tree.insert(20)
    tree.insert(22)
    return not (tree.get_max() != 22 or tree.get_min() != -16)


def test_tree_traversal() -> bool:
    """测试 three 不同 树 遍历 函数。"""
    tree = RedBlackTree(0)
    tree = tree.insert(-16)
    tree.insert(16)
    tree.insert(8)
    tree.insert(24)
    tree.insert(20)
    tree.insert(22)
    if list(tree.inorder_traverse()) != [-16, 0, 8, 16, 20, 22, 24]:
        return False
    if list(tree.preorder_traverse()) != [0, -16, 16, 8, 22, 20, 24]:
        return False
    return list(tree.postorder_traverse()) == [-16, 8, 20, 24, 22, 16, 0]


def test_tree_chaining() -> bool:
    """测试 three 不同 树 chaining 函数。"""
    tree = RedBlackTree(0)
    tree = tree.insert(-16).insert(16).insert(8).insert(24).insert(20).insert(22)
    if list(tree.inorder_traverse()) != [-16, 0, 8, 16, 20, 22, 24]:
        return False
    if list(tree.preorder_traverse()) != [0, -16, 16, 8, 22, 20, 24]:
        return False
    return list(tree.postorder_traverse()) == [-16, 8, 20, 24, 22, 16, 0]


def print_results(msg: str, passes: bool) -> None:
    print(str(msg), "works!" if passes else "doesn't work :(")


def pytests() -> None:
    assert test_rotations()
    assert test_insert()
    assert test_insert_and_search()
    assert test_insert_delete()
    assert test_floor_ceil()
    assert test_tree_traversal()
    assert test_tree_chaining()


def main() -> None:
    """
    >>> pytests()
    """
    print_results("Rotating right and left", test_rotations())
    print_results("Inserting", test_insert())
    print_results("Searching", test_insert_and_search())
    print_results("Deleting", test_insert_delete())
    print_results("Floor and ceil", test_floor_ceil())
    print_results("Tree traversal", test_tree_traversal())
    print_results("Tree traversal", test_tree_chaining())
    print("Testing tree balancing...")
    print("This should only be a few seconds.")
    test_insertion_speed()
    print("Done!")


if __name__ == "__main__":
    main()
