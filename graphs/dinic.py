INF = float("inf")


class Dinic:
    def __init__(self, n) -> None:
        self.lvl = [0] * n
        self.ptr = [0] * n
        self.q = [0] * n
        self.adj = [[] for _ in range(n)]

    """
    在这里，我们将添加包含以下参数的边：
    最接近源的顶点、最接近汇的顶点和流量
    穿过那个边...
    """

    def add_edge(self, a, b, c, rcap=0) -> None:
        self.adj[a].append([b, len(self.adj[b]), c, 0])
        self.adj[b].append([a, len(self.adj[a]) - 1, rcap, 0])

    # 这是在 max_flow 中使用的深度优先搜索示例
    def depth_first_search(self, vertex, sink, flow):
        if vertex == sink or not flow:
            return flow

        for i in range(self.ptr[vertex], len(self.adj[vertex])):
            e = self.adj[vertex][i]
            if self.lvl[e[0]] == self.lvl[vertex] + 1:
                p = self.depth_first_search(e[0], sink, min(flow, e[2] - e[3]))
                if p:
                    self.adj[vertex][i][3] += p
                    self.adj[e[0]][e[1]][3] -= p
                    return p
            self.ptr[vertex] = self.ptr[vertex] + 1
        return 0

    # 这里我们计算到达水槽的流量
    def max_flow(self, source, sink):
        flow, self.q[0] = 0, source
        for l in range(31):  # l = 30 maybe faster for random data  # noqa: E741
            while True:
                self.lvl, self.ptr = [0] * len(self.q), [0] * len(self.q)
                qi, qe, self.lvl[source] = 0, 1, 1
                while qi < qe and not self.lvl[sink]:
                    v = self.q[qi]
                    qi += 1
                    for e in self.adj[v]:
                        if not self.lvl[e[0]] and (e[2] - e[3]) >> (30 - l):
                            self.q[qe] = e[0]
                            qe += 1
                            self.lvl[e[0]] = self.lvl[v] + 1

                p = self.depth_first_search(source, sink, INF)
                while p:
                    flow += p
                    p = self.depth_first_search(source, sink, INF)

                if not self.lvl[sink]:
                    break

        return flow


# 使用示例

"""
将是一个二部图，它的顶点靠近源（4）
和水槽附近的顶点(4)
"""
# 这里我们制作一个有10个顶点的图（包括源和汇）
graph = Dinic(10)
source = 0
sink = 9
"""
现在我们将字体旁边的顶点添加到该边的容量为 1 的字体中
(source -> source vertices)
"""
for vertex in range(1, 5):
    graph.add_edge(source, vertex, 1)
"""
我们将对水槽附近的顶点执行相同的操作，但从顶点到水槽
(sink vertices -> sink)
"""
for vertex in range(5, 9):
    graph.add_edge(vertex, sink, 1)
"""
最后，我们将接收器附近的顶点添加到源附近的顶点。
(source vertices -> sink vertices)
"""
for vertex in range(1, 5):
    graph.add_edge(vertex, vertex + 4, 1)

# 现在我们可以知道这是最大流量（源->汇）
print(graph.max_flow(source, sink))
