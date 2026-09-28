"""
双向搜索算法。

该算法同时从源节点和目标节点进行搜索，
在中间的某个地方相遇。这种方法可以显着减少
搜索空间与传统的单向搜索相比。

时间复杂度：O(b^(d/2))，其中b 是方向因子，d 是深度
空间复杂度：O(b^(d/2))

https://en.wikipedia.org/wiki/Bidirectional_search
"""

from collections import deque


def expand_search(
    graph: dict[int, list[int]],
    queue: deque[int],
    parents: dict[int, int | None],
    opposite_direction_parents: dict[int, int | None],
) -> int | None:
    if not queue:
        return None

    current = queue.popleft()
    for neighbor in graph[current]:
        if neighbor in parents:
            continue

        parents[neighbor] = current
        queue.append(neighbor)

        # 检查这是否会创建交叉点
        if neighbor in opposite_direction_parents:
            return neighbor

    return None


def construct_path(current: int | None, parents: dict[int, int | None]) -> list[int]:
    path: list[int] = []
    while current is not None:
        path.append(current)
        current = parents[current]
    return path


def bidirectional_search(
    graph: dict[int, list[int]], start: int, goal: int
) -> list[int] | None:
    """
    在图上执行双向搜索以找到最短路径。

    参数：
        图：字典，其中键是节点，值是相邻节点的列表
        start：起始节点
        目标：目标节点

    返回：
        表示从起点到目标的路径的列表，如果不存在路径则为 None

    示例：
        >>> graph = {
        ...     0: [1, 2],
        ...     1: [0, 3, 4],
        ...     2: [0, 5, 6],
        ...     3: [1, 7],
        ...     4: [1, 8],
        ...     5: [2, 9],
        ...     6: [2, 10],
        ...     7: [3, 11],
        ...     8: [4, 11],
        ...     9: [5, 11],
        ...     10: [6, 11],
        ...     11: [7, 8, 9, 10],
        ... }
        >>> bidirectional_search(graph=graph, start=0, goal=11)
        [0, 1, 3, 7, 11]
        >>> bidirectional_search(graph=graph, start=5, goal=5)
        [5]
        >>> disconnected_graph = {
        ...     0: [1, 2],
        ...     1: [0],
        ...     2: [0],
        ...     3: [4],
        ...     4: [3],
        ... }
        >>> bidirectional_search(graph=disconnected_graph, start=0, goal=3) is None
        True
    """
    if start == goal:
        return [start]

    # 检查开始和目标是否在图表中
    if start not in graph or goal not in graph:
        return None

    # 初始化向前和向后搜索字典
    # 每个节点在搜索中将一个节点映射到其父节点
    forward_parents: dict[int, int | None] = {start: None}
    backward_parents: dict[int, int | None] = {goal: None}

    # 初始化向前和向后搜索队列
    forward_queue = deque([start])
    backward_queue = deque([goal])

    # 交叉点（两个搜索相遇的地方）
    intersection = None

    # 继续，直到两个队列都为空或找到交叉点
    while forward_queue and backward_queue and intersection is None:
        # 扩大向前搜索
        intersection = expand_search(
            graph=graph,
            queue=forward_queue,
            parents=forward_parents,
            opposite_direction_parents=backward_parents,
        )

        # 如果没有找到交集，则向后扩展搜索
        if intersection is not None:
            break

        intersection = expand_search(
            graph=graph,
            queue=backward_queue,
            parents=backward_parents,
            opposite_direction_parents=forward_parents,
        )

    # 如果没有找到交叉点，则没有路径
    if intersection is None:
        return None

    # 构造从起点到交叉点的路径
    forward_path: list[int] = construct_path(
        current=intersection, parents=forward_parents
    )
    forward_path.reverse()

    # 构建从交叉点到目标的路径
    backward_path: list[int] = construct_path(
        current=backward_parents[intersection], parents=backward_parents
    )

    # 返回完整路径
    return forward_path + backward_path


def main() -> None:
    """
    运行双向搜索算法的示例。

    示例：
        >>> main()  # doctest: +NORMALIZE_WHITESPACE
        Path from 0 to 11: [0, 1, 3, 7, 11]
        Path from 5 to 5: [5]
        Path from 0 to 3: None
    """
    # 表示为邻接列表的示例图
    example_graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5, 6],
        3: [1, 7],
        4: [1, 8],
        5: [2, 9],
        6: [2, 10],
        7: [3, 11],
        8: [4, 11],
        9: [5, 11],
        10: [6, 11],
        11: [7, 8, 9, 10],
    }

    # 测试用例 1：路径存在
    start, goal = 0, 11
    path = bidirectional_search(graph=example_graph, start=start, goal=goal)
    print(f"Path from {start} to {goal}: {path}")

    # 测试用例 2：开始和目标相同
    start, goal = 5, 5
    path = bidirectional_search(graph=example_graph, start=start, goal=goal)
    print(f"Path from {start} to {goal}: {path}")

    # 测试用例 3：不存在路径（断开的图）
    disconnected_graph = {
        0: [1, 2],
        1: [0],
        2: [0],
        3: [4],
        4: [3],
    }
    start, goal = 0, 3
    path = bidirectional_search(graph=disconnected_graph, start=start, goal=goal)
    print(f"Path from {start} to {goal}: {path}")


if __name__ == "__main__":
    main()
