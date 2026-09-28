"""
伪代码

DIJKSTRA(graph G, start vertex s, destination vertex d):

// all nodes initially unexplored

1 -  let H = min heap data structure, initialized with (0, s)
     // 0 is the distance from start vertex s
2 -  let costs = dictionary to store minimum costs to reach each node,
     initialized with {s: 0}
3 -  while H is non-empty:
4 -    remove the first node and cost from H, call them U and cost
5 -    if U has been previously explored:
6 -      continue // skip further processing and go back to while loop, line 3
7 -    mark U as explored
8 -    if U is d:
9 -      return cost // total cost from start to destination vertex
10 -   for each neighbor V and edge cost c of U in G:
11 -     if V has been previously explored:
12 -       continue to next neighbor V in line 10
13 -     total_cost = cost + c
14 -     if total_cost is less than costs.get(V, ∞):
15 -       update costs[V] to total_cost
16 -       add (total_cost, V) to H

// At the end, if destination d is not reachable, return -1

您可以将代价视为 Dijkstra 找到最短距离的距离
图G中的边s和v之间。使用最小作为堆H保证
如果一个顶点已经被探索过，那么就没有其他路径了
最短距离，发生这种情况是因为 heapq.heappop 将始终返回
考虑到堆存储的不是距离最短的下一个顶点
仅前一个顶点和当前顶点之间的距离，但整个
构成从起始顶点到目标的路径的每个顶点之间的距离
顶点。
"""

import heapq


def dijkstra(graph: dict[str, list[tuple[str, int]]], start: str, end: str) -> int:
    """返回顶点起点和终点之间的最短路径的代价。

    >>> dijkstra(G, "E", "C")
    6
    >>> dijkstra(G2, "E", "F")
    3
    >>> dijkstra(G3, "E", "F")
    3
    """
    heap: list[tuple[int, str]] = [(0, start)]  # (cost, node)
    visited: set[str] = set()
    costs: dict[str, int] = {start: 0}  # 存储到达每个节点的最低代价

    while heap:
        cost, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u == end:
            return cost

        for v, c in graph[u]:
            if v in visited:
                continue
            next_cost = cost + c
            # 仅当找到更便宜的路径时才推送到堆
            if next_cost < costs.get(v, float("inf")):
                costs[v] = next_cost
                heapq.heappush(heap, (next_cost, v))

    return -1


G = {
    "A": [("B", 2), ("C", 5)],
    "B": [("A", 2), ("D", 3), ("E", 1), ("F", 1)],
    "C": [("A", 5), ("F", 3)],
    "D": [("B", 3)],
    "E": [("B", 4), ("F", 3)],
    "F": [("C", 3), ("E", 3)],
}

r"""
G2布局：

E -- 1 --> B -- 1 --> C -- 1 --> D -- 1 --> F
 \                                         /\
  \                                        ||
    ----------------- 3 --------------------
"""
G2 = {
    "B": [("C", 1)],
    "C": [("D", 1)],
    "D": [("F", 1)],
    "E": [("B", 1), ("F", 3)],
    "F": [],
}

r"""
G3布局：

E -- 1 --> B -- 1 --> C -- 1 --> D -- 1 --> F
 \                                         /\
  \                                        ||
    -------- 2 ---------> G ------- 1 ------
"""
G3 = {
    "B": [("C", 1)],
    "C": [("D", 1)],
    "D": [("F", 1)],
    "E": [("B", 1), ("G", 2)],
    "F": [],
    "G": [("F", 1)],
}

short_distance = dijkstra(G, "E", "C")
print(short_distance)  # E -- 3 --> F -- 3 --> C == 6

short_distance = dijkstra(G2, "E", "F")
print(short_distance)  # E -- 3 --> F == 3

short_distance = dijkstra(G3, "E", "F")
print(short_distance)  # E -- 2 --> G -- 1 --> F == 3

if __name__ == "__main__":
    import doctest

    doctest.testmod()
