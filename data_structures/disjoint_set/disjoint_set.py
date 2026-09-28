"""
并查集。
Reference: https://en.wikipedia.org/wiki/Disjoint-set_data_structure
"""

from dataclasses import dataclass


@dataclass
class Node:
    data: int
    rank: int = 0
    parent: Node | None = None


def make_set(x: Node) -> None:
    """
    使 x 作为 集合。

    >>> node = Node(1)
    >>> make_set(node)
    >>> node.parent == node
    True
    >>> node.rank
    0
    >>> node.data
    1
    """
    # rank 是 距离 从 x 到 其' 父节点
    # 根节点's rank 是 0
    x.rank = 0
    x.parent = x


def union_set(x: Node, y: Node) -> None:
    """
    Union 的 两个 sets。
    集合 带有 bigger rank 应 为 父节点，因此 该
    并查集 树 将 为 更多 flat。

    >>> node1 = Node(1)
    >>> node2 = Node(2)
    >>> make_set(node1)
    >>> make_set(node2)
    >>> union_set(node1, node2)
    >>> find_set(node1) == find_set(node2)
    True
    >>> # Test union of already connected nodes
    >>> node3 = Node(3)
    >>> make_set(node3)
    >>> union_set(node1, node3)
    >>> find_set(node1) == find_set(node3)
    True
    >>> find_set(node2) == find_set(node3)
    True
    """
    x, y = find_set(x), find_set(y)
    if x == y:
        return

    elif x.rank > y.rank:
        y.parent = x
    else:
        x.parent = y
        if x.rank == y.rank:
            y.rank += 1


def find_set(x: Node) -> Node:
    """
    返回 父节点 的 x

    >>> node = Node(1)
    >>> make_set(node)
    >>> find_set(node) == node
    True
    >>> node1 = Node(1)
    >>> node2 = Node(2)
    >>> make_set(node1)
    >>> make_set(node2)
    >>> union_set(node1, node2)
    >>> find_set(node1) == find_set(node2)
    True
    >>> # Test path compression
    >>> node3 = Node(3)
    >>> make_set(node3)
    >>> union_set(node1, node3)
    >>> find_set(node1) == find_set(node3)
    True
    """
    if x != x.parent:
        x.parent = find_set(x.parent)
    return x.parent


def find_python_set(node: Node) -> set:
    """
    返回 Python Standard Library 集合 该 包含 i。

    >>> node = Node(1)
    >>> find_python_set(node)
    {0, 1, 2}
    >>> node = Node(4)
    >>> find_python_set(node)
    {3, 4, 5}
    >>> node = Node(6)
    >>> find_python_set(node)
    Traceback (most recent call last):
       ...
    ValueError: 6 is not in ({0, 1, 2}, {3, 4, 5})
    """
    sets = ({0, 1, 2}, {3, 4, 5})
    for s in sets:
        if node.data in s:
            return s
    msg = f"{node.data} is not in {sets}"
    raise ValueError(msg)


def test_disjoint_set() -> None:
    """
    测试 并查集 操作 带有 comprehensive 示例。
    Creates 两个 disjoint sets: {0，1，2} 并且 {3，4，5}

    >>> test_disjoint_set()
    """
    vertex = [Node(i) for i in range(6)]
    for v in vertex:
        make_set(v)

    union_set(vertex[0], vertex[1])
    union_set(vertex[1], vertex[2])
    union_set(vertex[3], vertex[4])
    union_set(vertex[3], vertex[5])

    for node0 in vertex:
        for node1 in vertex:
            if find_python_set(node0).isdisjoint(find_python_set(node1)):
                assert find_set(node0) != find_set(node1)
            else:
                assert find_set(node0) == find_set(node1)


if __name__ == "__main__":
    test_disjoint_set()
