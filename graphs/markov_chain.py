from __future__ import annotations

from collections import Counter
from random import random


class MarkovChainGraphUndirectedUnweighted:
    """
    用于运行马尔可夫链算法的无向无权图
    """

    def __init__(self) -> None:
        self.connections = {}

    def add_node(self, node: str) -> None:
        self.connections[node] = {}

    def add_transition_probability(
        self, node1: str, node2: str, probability: float
    ) -> None:
        if node1 not in self.connections:
            self.add_node(node1)
        if node2 not in self.connections:
            self.add_node(node2)
        self.connections[node1][node2] = probability

    def get_nodes(self) -> list[str]:
        return list(self.connections)

    def transition(self, node: str) -> str:
        current_probability = 0
        random_value = random()

        for dest in self.connections[node]:
            current_probability += self.connections[node][dest]
            if current_probability > random_value:
                return dest
        return ""


def get_transitions(
    start: str, transitions: list[tuple[str, str, float]], steps: int
) -> dict[str, int]:
    """
    运行马尔可夫链算法并计算每个节点被访问的次数
    访问过

    >>> transitions = [
    ... ('a', 'a', 0.9),
    ... ('a', 'b', 0.075),
    ... ('a', 'c', 0.025),
    ... ('b', 'a', 0.15),
    ... ('b', 'b', 0.8),
    ... ('b', 'c', 0.05),
    ... ('c', 'a', 0.25),
    ... ('c', 'b', 0.25),
    ... ('c', 'c', 0.5)
    ... ]

    >>> result = get_transitions('a', transitions, 5000)

    >>> result['a'] > result['b'] > result['c']
    True
    """

    graph = MarkovChainGraphUndirectedUnweighted()

    for node1, node2, probability in transitions:
        graph.add_transition_probability(node1, node2, probability)

    visited = Counter(graph.get_nodes())
    node = start

    for _ in range(steps):
        node = graph.transition(node)
        visited[node] += 1

    return visited


if __name__ == "__main__":
    import doctest

    doctest.testmod()
