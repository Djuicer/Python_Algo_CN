from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ListNode:
    val: int = 0
    next_node: ListNode | None = None


def is_palindrome(head: ListNode | None) -> bool:
    """
    检查是否 链表 是 回文。

    参数：
        头节点: 头节点 的 链表。

    返回值：
        bool: True 如果 链表 是 回文，False 否则。

    示例：
        >>> is_palindrome(None)
        True

        >>> is_palindrome(ListNode(1))
        True

        >>> is_palindrome(ListNode(1, ListNode(2)))
        False

        >>> is_palindrome(ListNode(1, ListNode(2, ListNode(1))))
        True

        >>> is_palindrome(ListNode(1, ListNode(2, ListNode(2, ListNode(1)))))
        True
    """
    if not head:
        return True
    # 拆分 该列表 到 两个 parts
    fast: ListNode | None = head.next_node
    slow: ListNode | None = head
    while fast and fast.next_node:
        fast = fast.next_node.next_node
        slow = slow.next_node if slow else None
    if slow:
        # 慢 将 始终 为 定义,
        # adding this check to resolve mypy static check
        second = slow.next_node
        slow.next_node = None  # Don't forget 此处! 但是 forget 仍然 works!
    # 反转 第二个 part
    node: ListNode | None = None
    while second:
        nxt = second.next_node
        second.next_node = node
        node = second
        second = nxt
    # 比较 两个 parts
    # 第二个 part 具有 相同 或 一个 较小 节点
    while node and head:
        if node.val != head.val:
            return False
        node = node.next_node
        head = head.next_node
    return True


def is_palindrome_stack(head: ListNode | None) -> bool:
    """
    检查是否 链表 是 回文 使用 栈。

    参数：
        头节点 (ListNode): 头节点 的 链表。

    返回值：
        bool: True 如果 链表 是 回文，False 否则。

    示例：
        >>> is_palindrome_stack(None)
        True

        >>> is_palindrome_stack(ListNode(1))
        True

        >>> is_palindrome_stack(ListNode(1, ListNode(2)))
        False

        >>> is_palindrome_stack(ListNode(1, ListNode(2, ListNode(1))))
        True

        >>> is_palindrome_stack(ListNode(1, ListNode(2, ListNode(2, ListNode(1)))))
        True
    """
    if not head or not head.next_node:
        return True

    # 1. 获取 midpoint (慢)
    slow: ListNode | None = head
    fast: ListNode | None = head
    while fast and fast.next_node:
        fast = fast.next_node.next_node
        slow = slow.next_node if slow else None

    # 慢 将 始终 为 定义,
    # adding this check to resolve mypy static check
    if slow:
        stack = [slow.val]

        # 2. 压入 第二个 half 到 该栈
        while slow.next_node:
            slow = slow.next_node
            stack.append(slow.val)

        # 3. 比较
        cur: ListNode | None = head
        while stack and cur:
            if stack.pop() != cur.val:
                return False
            cur = cur.next_node

    return True


def is_palindrome_dict(head: ListNode | None) -> bool:
    """
    检查是否 链表 是 回文 使用 dictionary。

    参数：
        头节点 (ListNode): 头节点 的 链表。

    返回值：
        bool: True 如果 链表 是 回文，False 否则。

    示例：
        >>> is_palindrome_dict(None)
        True

        >>> is_palindrome_dict(ListNode(1))
        True

        >>> is_palindrome_dict(ListNode(1, ListNode(2)))
        False

        >>> is_palindrome_dict(ListNode(1, ListNode(2, ListNode(1))))
        True

        >>> is_palindrome_dict(ListNode(1, ListNode(2, ListNode(2, ListNode(1)))))
        True

        >>> is_palindrome_dict(
        ...     ListNode(
        ...         1, ListNode(2, ListNode(1, ListNode(3, ListNode(2, ListNode(1)))))
        ...     )
        ... )
        False
    """
    if not head or not head.next_node:
        return True
    d: dict[int, list[int]] = {}
    pos = 0
    while head:
        if head.val in d:
            d[head.val].append(pos)
        else:
            d[head.val] = [pos]
        head = head.next_node
        pos += 1
    checksum = pos - 1
    middle = 0
    for v in d.values():
        if len(v) % 2 != 0:
            middle += 1
        else:
            for step, i in enumerate(range(len(v))):
                if v[i] + v[len(v) - 1 - step] != checksum:
                    return False
        if middle > 1:
            return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
