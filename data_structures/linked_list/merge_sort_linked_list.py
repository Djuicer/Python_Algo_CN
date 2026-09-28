from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(order=True)
class Node:
    """
    类 表示 一个节点 在 链表。

    属性：
        数据: 数据 存储 在 该节点。
        下一个: 引用 到 下一个节点 在 链表。
    """

    data: int
    next: Node | None = None


def iter_linked_list(head: Node | None) -> Iterable[Node]:
    """
    迭代 超过 节点 的 链表。

    参数：
        头节点: 头节点 节点 的 链表。

    Yields:
        每个节点 在 链表，一个 通过 一个。

    示例：
    >>> head = Node(3, Node(1, Node(2)))
    >>> head  # dataclasses provide a nice .__repr__().
    Node(data=3, next=Node(data=1, next=Node(data=2, next=None)))
    >>> tuple(iter_linked_list(head))
    (3, 1, 2)
    """
    current = head
    while current:
        yield current.data
        current = current.next


def get_middle(head: Node | None) -> Node | None:
    """
    查找 节点 之前 middle 的 链表
    使用 慢 并且 fast 指针 technique。

    参数：
        头节点: 头节点 节点 的 链表。

    返回值：
        该节点 之前 middle 的 链表,
        或 None 如果 该列表 具有 fewer 比 2 节点。

    示例：
    >>> head = Node(1)
    >>> head.next = Node(2)
    >>> head.next.next = Node(3)
    >>> middle = get_middle(head)
    >>> middle.data
    2
    """
    if head is None or head.next is None:
        return None

    slow: Node | None = head
    fast: Node | None = head.next

    while fast is not None and fast.next is not None:
        if slow is None:
            return None
        slow = slow.next
        fast = fast.next.next

    return slow


def merge(left: Node | None, right: Node | None) -> Node | None:
    """
    合并两个 已排序 连接 列表 到 一个 已排序 链表。

    参数：
        左: 头节点 的 第一个 已排序 链表。
        右: 头节点 的 第二个 已排序 链表。

    返回值：
        头节点 的 合并后 已排序 链表。

    示例：
    >>> left = Node(1)
    >>> left.next = Node(3)
    >>> tuple(iter_linked_list(left))
    (1, 3)
    >>> right = Node(2)
    >>> right.next = Node(4)
    >>> tuple(iter_linked_list(right))
    (2, 4)
    >>> merged = merge(left, right)
    >>> tuple(iter_linked_list(merged))
    (1, 2, 3, 4)
    """

    if left is None:
        return right
    if right is None:
        return left

    if left <= right:
        result = left
        result.next = merge(left.next, right)
    else:
        result = right
        result.next = merge(left, right.next)

    return result


def merge_sort_linked_list(head: Node | None) -> Node | None:
    """
    排序 链表 使用 合并 排序 算法。

    参数：
        头节点: 头节点 节点 的 链表 到 为 已排序。

    返回值：
        头节点 节点 的 已排序 链表。

    示例：
    >>> head = Node(4)
    >>> head.next = Node(2)
    >>> head.next.next = Node(1)
    >>> head.next.next.next = Node(3)
    >>> tuple(iter_linked_list(head))
    (4, 2, 1, 3)
    >>> sorted_head = merge_sort_linked_list(head)
    >>> tuple(iter_linked_list(sorted_head))
    (1, 2, 3, 4)
    """

    # 基本情况: 0 或 1 节点
    if head is None or head.next is None:
        return head

    # 拆分 链表 到 两个 halves
    middle = get_middle(head)
    if middle is None or middle.next is None:
        return head

    next_to_middle = middle.next
    middle.next = None  # 拆分 该列表 到 两个 parts

    # 递归地 排序 两者 halves
    left = merge_sort_linked_list(head)
    right = merge_sort_linked_list(next_to_middle)

    # 合并 已排序 halves
    return merge(left, right)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
