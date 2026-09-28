"""
用于划分图的Karger算法的实现。
"""

from __future__ import annotations

import random

# 该图的邻接列表表示：
# https://en.wikipedia.org/wiki/File:Single_run_of_Karger%E2%80%99s_Mincut_algorithm.svg
TEST_GRAPH = {
    "1": ["2", "3", "4", "5"],
    "2": ["1", "3", "4", "5"],
    "3": ["1", "2", "4", "5", "10"],
    "4": ["1", "2", "3", "5", "6"],
    "5": ["1", "2", "3", "4", "7"],
    "6": ["7", "8", "9", "10", "4"],
    "7": ["6", "8", "9", "10", "5"],
    "8": ["6", "7", "9", "10"],
    "9": ["6", "7", "8", "10"],
    "10": ["6", "7", "8", "9", "3"],
}


def partition_graph(graph: dict[str, list[str]]) -> set[tuple[str, str]]:
    """
    使用 Karger 算法对图进行分区。实施自
    伪代码在这里找到：
    https://en.wikipedia.org/wiki/Karger%27s_algorithm.
    该函数涉及随机选择，这意味着它不会给出
    一致的输出。

    参数：
        graph：包含图表邻接列表的字典。
            节点必须是字符串。

    返回：
        Karger 算法找到了切割的切割集。

    >>> graph = {'0':['1'], '1':['0']}
    >>> partition_graph(graph)
    {('0', '1')}
    """
    # 将契约节点映射到它“包含”的所有节点的列表的字典。
    contracted_nodes = {node: {node} for node in graph}

    graph_copy = {node: graph[node][:] for node in graph}

    while len(graph_copy) > 2:
        # 选择随机边。
        u = random.choice(list(graph_copy.keys()))
        v = random.choice(graph_copy[u])

        # 将边 (u, v) 收缩到新节点 uv
        uv = u + v
        uv_neighbors = list(set(graph_copy[u] + graph_copy[v]))
        uv_neighbors.remove(u)
        uv_neighbors.remove(v)
        graph_copy[uv] = uv_neighbors
        for neighbor in uv_neighbors:
            graph_copy[neighbor].append(uv)

        contracted_nodes[uv] = set(contracted_nodes[u].union(contracted_nodes[v]))

        # 删除节点u和v。
        del graph_copy[u]
        del graph_copy[v]
        for neighbor in uv_neighbors:
            if u in graph_copy[neighbor]:
                graph_copy[neighbor].remove(u)
            if v in graph_copy[neighbor]:
                graph_copy[neighbor].remove(v)

    # 求割集。
    groups = [contracted_nodes[node] for node in graph_copy]
    return {
        (node, neighbor)
        for node in groups[0]
        for neighbor in graph[node]
        if neighbor in groups[1]
    }


if __name__ == "__main__":
    print(partition_graph(TEST_GRAPH))
