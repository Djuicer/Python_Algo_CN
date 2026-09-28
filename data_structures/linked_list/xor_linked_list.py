"""
XOR 链表 实现
memory-efficient 双向链表 该 使用 XOR 的 节点 addresses。
每个节点 存储 一个 指针 该 是 XOR 的 上一个 并且 下一个节点 addresses。
https://en.wikipedia.org/wiki/XOR_linked_list
示例：
>>> xor_list = XORLinkedList()
>>> xor_list.insert(10)
>>> xor_list.insert(20)
>>> xor_list.insert(30)
>>> xor_list.to_list()
[10, 20, 30]
"""

from dataclasses import dataclass


@dataclass
class Node:
    value: int
    both: int = 0  # XOR 的 prev 并且 下一个节点 IDs


class XORLinkedList:
    def __init__(self) -> None:
        """Initializes 空 XOR 链表。"""
        # 使用 '节点 | None' instead 的 '可选[节点]' (per ruff UP045)
        self.head: Node | None = None
        self.tail: Node | None = None
        # id -> 节点 map 到 simulate 指针 引用
        self._nodes: dict[int, Node] = {}

    def _xor(self, node_a: Node | None, node_b: Node | None) -> int:
        """
        Helper 函数 到 获取 XOR 的 两个 节点 IDs (simulated addresses)。
        Names 'node_a' 并且 'node_b' 是 使用 用于 descriptive 参数。
        """
        id_a = id(node_a) if node_a else 0
        id_b = id(node_b) if node_b else 0
        return id_a ^ id_b

    def insert(self, value: int) -> None:
        """插入一个 值 在 列表末尾。"""
        node = Node(value)
        self._nodes[id(node)] = node
        node_id = id(node)

        if self.head is None:
            # 如果 该列表 为空，头节点 并且 尾节点 是 新节点
            self.head = self.tail = node
        else:
            # 如果 该列表 非空，追加 到 尾节点
            # 新节点's 指针 是 仅 ID 的 old 尾节点
            node.both = id(self.tail)
            if self.tail:  # 类型 checker guard
                # old 尾节点's 指针 必须 为 updated 到 XOR
                # 其 上一个节点 ID 带有 新节点's ID。
                # self.尾节点.两者 曾是 (prev_id ^ 0)
                # self.尾节点.两者 变为 (prev_id ^ new_node_id)
                self.tail.both ^= node_id
            self.tail = node

    def to_list(self) -> list[int]:
        """转换 XOR 列表 到 standard Python 列表 (向前 遍历)。"""
        result = []
        prev_id = 0
        current = self.head
        while current:
            result.append(current.value)
            # 查找 下一个节点's ID：
            # 当前.两者 = prev_id ^ next_id
            # 因此，next_id = prev_id ^ 当前.两者
            current_id = id(current)
            next_id = prev_id ^ current.both

            # 移动 向前
            prev_id = current_id
            current = self._nodes.get(next_id)
        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
