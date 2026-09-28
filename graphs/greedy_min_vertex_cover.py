"""
* Author: Manuel Di Lullo (https://github.com/manueldilullo)
* Description: Approximization algorithm for minimum vertex cover problem.
               贪婪方法。使用以邻接列表表示的图
URL: https://mathworld.wolfram.com/MinimumVertexCover.html
URL: https://cs.stackexchange.com/questions/129017/greedy-algorithm-for-vertex-cover
"""

import heapq


def greedy_min_vertex_cover(graph: dict) -> set[int]:
    """
    最小顶点覆盖的贪心 APX 算法
    @input：图（存储在邻接列表中的图，其中每个顶点
            用整数表示）
    @例子：
    >>> graph = {0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]}
    >>> greedy_min_vertex_cover(graph)
    {0, 1, 2, 4}
    """
    # 队列用于存储节点及其排名
    queue: list[list] = []

    # 对于每个节点及其邻接列表，添加它们以及要排队的节点的排名
    # 使用 heapq 模块，队列将像优先级队列一样被填充
    # heapq 使用最小优先级队列，因此我使用 -1*len(v) 来构建它
    for key, value in graph.items():
        # O(log(n)）
        heapq.heappush(queue, [-1 * len(value), (key, value)])

    # chosen_vertices = 首选顶点的集合
    chosen_vertices = set()

    # 当队列不为空并且仍然有边时
    #   (queue[0][0] is the rank of the node with max rank)
    while queue and queue[0][0] != 0:
        # 从队列中取出排名最高的顶点并将其添加到chosen_vertices
        argmax = heapq.heappop(queue)[1][0]
        chosen_vertices.add(argmax)

        # 删除与 argmax 后续的所有弧
        for elem in queue:
            # 如果 v 没有相邻节点，则跳过
            if elem[0] == 0:
                continue
            # 如果argmax可以从elem到达
            # 从 elem 的顺序列表中删除 argmax 并更新他的排名
            if argmax in elem[1][1]:
                index = elem[1][1].index(argmax)
                del elem[1][1][index]
                elem[0] += 1
        # 重新排序队列
        heapq.heapify(queue)
    return chosen_vertices


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    graph = {0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]}
    print(f"Minimum vertex cover:\n{greedy_min_vertex_cover(graph)}")
