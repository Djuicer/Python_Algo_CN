"""
Prim 算法（也称为 Jarník 算法）是一种贪心算法，可找到最小值
加权无向图的生成树。这意味着它找到了
形成包含每个顶点的树的边，其中所有顶点的总权重
树中的边被最小化。该算法通过构建这棵树的一个顶点来运行
一次，从任意起始顶点，在每一步添加尽可能便宜的
从树到另一个顶点的连接。
"""

from __future__ import annotations

from sys import maxsize
from typing import TypeVar

T = TypeVar("T")


def get_parent_position(position: int) -> int:
    """
    堆辅助函数获取当前节点父节点的位置

    >>> get_parent_position(1)
    0
    >>> get_parent_position(2)
    0
    """
    return (position - 1) // 2


def get_child_left_position(position: int) -> int:
    """
    堆辅助函数获取当前节点左子节点的位置

    >>> get_child_left_position(0)
    1
    """
    return (2 * position) + 1


def get_child_right_position(position: int) -> int:
    """
    堆辅助函数获取当前节点右子节点的位置

    >>> get_child_right_position(0)
    2
    """
    return (2 * position) + 2


class MinPriorityQueue[T]:
    """
    最低优先级队列类别

    功能：
    is_empty：检查优先级队列是否为空的函数
    Push：将具有给定优先级的元素添加到队列的函数
    extract_min：删除并返回权重最低（最高）的元素的函数
                 优先事项）
    update_key：更新给定密钥权重的函数
    _bubble_up：帮助函数将节点放置在正确的位置（向上
                移动）
    _bubble_down：帮助函数将节点放置在正确的位置（向下
                移动）
    _swap_nodes：交换给定位置节点的辅助函数

    >>> queue = MinPriorityQueue()

    >>> queue.push(1, 1000)
    >>> queue.push(2, 100)
    >>> queue.push(3, 4000)
    >>> queue.push(4, 3000)

    >>> queue.extract_min()
    2

    >>> queue.update_key(4, 50)

    >>> queue.extract_min()
    4
    >>> queue.extract_min()
    1
    >>> queue.extract_min()
    3
    """

    def __init__(self) -> None:
        self.heap: list[tuple[T, int]] = []
        self.position_map: dict[T, int] = {}
        self.elements: int = 0

    def __len__(self) -> int:
        return self.elements

    def __repr__(self) -> str:
        return str(self.heap)

    def is_empty(self) -> bool:
        # 检查优先级队列是否为空
        return self.elements == 0

    def push(self, elem: T, weight: int) -> None:
        # 将具有给定优先级的元素添加到队列中
        self.heap.append((elem, weight))
        self.position_map[elem] = self.elements
        self.elements += 1
        self._bubble_up(elem)

    def extract_min(self) -> T:
        # 删除并返回权重最低的元素（优先级最高）
        if self.elements > 1:
            self._swap_nodes(0, self.elements - 1)
        elem, _ = self.heap.pop()
        del self.position_map[elem]
        self.elements -= 1
        if self.elements > 0:
            bubble_down_elem, _ = self.heap[0]
            self._bubble_down(bubble_down_elem)
        return elem

    def update_key(self, elem: T, weight: int) -> None:
        # 更新给定密钥的权重
        position = self.position_map[elem]
        self.heap[position] = (elem, weight)
        if position > 0:
            parent_position = get_parent_position(position)
            _, parent_weight = self.heap[parent_position]
            if parent_weight > weight:
                self._bubble_up(elem)
            else:
                self._bubble_down(elem)
        else:
            self._bubble_down(elem)

    def _bubble_up(self, elem: T) -> None:
        # 将节点放置在合适的位置（向上移动）【内部使用
        # 仅有的]
        curr_pos = self.position_map[elem]
        if curr_pos == 0:
            return None
        parent_position = get_parent_position(curr_pos)
        _, weight = self.heap[curr_pos]
        _, parent_weight = self.heap[parent_position]
        if parent_weight > weight:
            self._swap_nodes(parent_position, curr_pos)
            return self._bubble_up(elem)
        return None

    def _bubble_down(self, elem: T) -> None:
        # 将节点放置在适当的位置（向下移动）【待使用
        # 仅限内部]
        curr_pos = self.position_map[elem]
        _, weight = self.heap[curr_pos]
        child_left_position = get_child_left_position(curr_pos)
        child_right_position = get_child_right_position(curr_pos)
        if child_left_position < self.elements and child_right_position < self.elements:
            _, child_left_weight = self.heap[child_left_position]
            _, child_right_weight = self.heap[child_right_position]
            if child_right_weight < child_left_weight and child_right_weight < weight:
                self._swap_nodes(child_right_position, curr_pos)
                return self._bubble_down(elem)
        if child_left_position < self.elements:
            _, child_left_weight = self.heap[child_left_position]
            if child_left_weight < weight:
                self._swap_nodes(child_left_position, curr_pos)
                return self._bubble_down(elem)
        else:
            return None
        if child_right_position < self.elements:
            _, child_right_weight = self.heap[child_right_position]
            if child_right_weight < weight:
                self._swap_nodes(child_right_position, curr_pos)
                return self._bubble_down(elem)
        return None

    def _swap_nodes(self, node1_pos: int, node2_pos: int) -> None:
        # 交换给定位置的节点
        node1_elem = self.heap[node1_pos][0]
        node2_elem = self.heap[node2_pos][0]
        self.heap[node1_pos], self.heap[node2_pos] = (
            self.heap[node2_pos],
            self.heap[node1_pos],
        )
        self.position_map[node1_elem] = node2_pos
        self.position_map[node2_elem] = node1_pos


class GraphUndirectedWeighted[T]:
    """
    图无向加权类

    功能：
    add_node：在图中添加节点的函数
    add_edge：在图中的2个节点之间添加边的函数
    """

    def __init__(self) -> None:
        self.connections: dict[T, dict[T, int]] = {}
        self.nodes: int = 0

    def __repr__(self) -> str:
        return str(self.connections)

    def __len__(self) -> int:
        return self.nodes

    def add_node(self, node: T) -> None:
        # 如果图中没有节点，则添加该节点
        if node not in self.connections:
            self.connections[node] = {}
            self.nodes += 1

    def add_edge(self, node1: T, node2: T, weight: int) -> None:
        # 在图中的 2 个节点之间添加一条边
        self.add_node(node1)
        self.add_node(node2)
        self.connections[node1][node2] = weight
        self.connections[node2][node1] = weight


def prims_algo[T](
    graph: GraphUndirectedWeighted[T],
) -> tuple[dict[T, int], dict[T, T | None]]:
    """
    >>> graph = GraphUndirectedWeighted()

    >>> graph.add_edge("a", "b", 3)
    >>> graph.add_edge("b", "c", 10)
    >>> graph.add_edge("c", "d", 5)
    >>> graph.add_edge("a", "c", 15)
    >>> graph.add_edge("b", "d", 100)

    >>> dist, parent = prims_algo(graph)

    >>> abs(dist["a"] - dist["b"])
    3
    >>> abs(dist["d"] - dist["b"])
    15
    >>> abs(dist["a"] - dist["c"])
    13
    """
    # prim 最小生成树算法
    dist: dict[T, int] = dict.fromkeys(graph.connections, maxsize)
    parent: dict[T, T | None] = dict.fromkeys(graph.connections)

    priority_queue: MinPriorityQueue[T] = MinPriorityQueue()
    for node, weight in dist.items():
        priority_queue.push(node, weight)

    if priority_queue.is_empty():
        return dist, parent

    # 初始化
    node = priority_queue.extract_min()
    dist[node] = 0
    for neighbour in graph.connections[node]:
        if dist[neighbour] > dist[node] + graph.connections[node][neighbour]:
            dist[neighbour] = dist[node] + graph.connections[node][neighbour]
            priority_queue.update_key(neighbour, dist[neighbour])
            parent[neighbour] = node

    # 运行 prim 算法
    while not priority_queue.is_empty():
        node = priority_queue.extract_min()
        for neighbour in graph.connections[node]:
            if dist[neighbour] > dist[node] + graph.connections[node][neighbour]:
                dist[neighbour] = dist[node] + graph.connections[node][neighbour]
                priority_queue.update_key(neighbour, dist[neighbour])
                parent[neighbour] = node
    return dist, parent
