"""
https://en.wikipedia.org/wiki/Breadth-first_search
伪代码（原始代码保持不变）：
breadth_first_search(graph G, start vertex s):
// all nodes initially unexplored
mark s as explored
let Q = queue data structure, initialized with s
while Q is non-empty:
    remove the first node of Q, call it v
    for each edge(v, w):  // for w in graph[v]
        if w unexplored:
            mark w as explored
            add w to Q (at the end)
"""

from __future__ import annotations

from collections import deque
from queue import Queue
from timeit import timeit

G = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}


def breadth_first_search(graph: dict, start: str) -> list[str]:
    """
    使用queue.Queue实现广度优先搜索。

    >>> ''.join(breadth_first_search(G, 'A'))
    'ABCDEF'
    """
    explored = {start}
    result = [start]
    queue: Queue = Queue()
    queue.put(start)
    while not queue.empty():
        v = queue.get()
        for w in graph[v]:
            if w not in explored:
                explored.add(w)
                result.append(w)
                queue.put(w)
    return result


def breadth_first_search_with_deque(graph: dict, start: str) -> list[str]:
    """
    使用collection.queue实现广度优先搜索。

    >>> ''.join(breadth_first_search_with_deque(G, 'A'))
    'ABCDEF'
    """
    visited = {start}
    result = [start]
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for child in graph[v]:
            if child not in visited:
                visited.add(child)
                result.append(child)
                queue.append(child)
    return result


def benchmark_function(name: str) -> None:
    setup = f"from __main__ import G, {name}"
    number = 10000
    res = timeit(f"{name}(G, 'A')", setup=setup, number=number)
    print(f"{name:<35} finished {number} runs in {res:.5f} seconds")


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    benchmark_function("breadth_first_search")
    benchmark_function("breadth_first_search_with_deque")
    # breadth_first_search 在 0.20999 秒内完成 10000 次运行
    # breadth_first_search_with_deque 在 0.01421 秒内完成 10000 次运行
