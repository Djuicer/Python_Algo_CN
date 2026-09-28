# 标题：Dijkstra算法从头开始寻找单源最短路径
# Author: Shubham Malik
# References: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

import math
import sys

# 用于存储顶点集以检索具有最小距离的节点


class PriorityQueue:
    # 基于最小堆
    def __init__(self) -> None:
        """
        优先级队列类的构造方法。

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.cur_size
        0
        >>> priority_queue_test.array
        []
        >>> priority_queue_test.pos
        {}
        """
        self.cur_size = 0
        self.array = []
        self.pos = {}  # 将节点的pos在存储中

    def is_empty(self):
        """
        用于确定优先级队列是否为空的条件布尔方法。

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.is_empty()
        True
        >>> priority_queue_test.insert((2, 'A'))
        >>> priority_queue_test.is_empty()
        False
        """
        return self.cur_size == 0

    def min_heapify(self, idx) -> None:
        """
        对队列数组进行排序，使最小元素成为根。

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.cur_size = 3
        >>> priority_queue_test.pos = {'A': 0, 'B': 1, 'C': 2}

        >>> priority_queue_test.array = [(5, 'A'), (10, 'B'), (15, 'C')]
        >>> priority_queue_test.min_heapify(0)
        >>> priority_queue_test.array
        [(5, 'A'), (10, 'B'), (15, 'C')]

        >>> priority_queue_test.array = [(10, 'A'), (5, 'B'), (15, 'C')]
        >>> priority_queue_test.min_heapify(0)
        >>> priority_queue_test.array
        [(5, 'B'), (10, 'A'), (15, 'C')]

        >>> priority_queue_test.array = [(10, 'A'), (15, 'B'), (5, 'C')]
        >>> priority_queue_test.min_heapify(0)
        >>> priority_queue_test.array
        [(5, 'C'), (15, 'B'), (10, 'A')]

        >>> priority_queue_test.array = [(10, 'A'), (5, 'B')]
        >>> priority_queue_test.cur_size = len(priority_queue_test.array)
        >>> priority_queue_test.pos = {'A': 0, 'B': 1}
        >>> priority_queue_test.min_heapify(0)
        >>> priority_queue_test.array
        [(5, 'B'), (10, 'A')]
        """
        lc = self.left(idx)
        rc = self.right(idx)
        if lc < self.cur_size and self.array[lc][0] < self.array[idx][0]:
            smallest = lc
        else:
            smallest = idx
        if rc < self.cur_size and self.array[rc][0] < self.array[smallest][0]:
            smallest = rc
        if smallest != idx:
            self.swap(idx, smallest)
            self.min_heapify(smallest)

    def insert(self, tup) -> None:
        """
        将节点插入优先级队列。

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.insert((10, 'A'))
        >>> priority_queue_test.array
        [(10, 'A')]
        >>> priority_queue_test.insert((15, 'B'))
        >>> priority_queue_test.array
        [(10, 'A'), (15, 'B')]
        >>> priority_queue_test.insert((5, 'C'))
        >>> priority_queue_test.array
        [(5, 'C'), (10, 'A'), (15, 'B')]
        """
        self.pos[tup[1]] = self.cur_size
        self.cur_size += 1
        self.array.append((sys.maxsize, tup[1]))
        self.decrease_key((sys.maxsize, tup[1]), tup[0])

    def extract_min(self):
        """
        删除并返回优先级队列顶部的最小元素。

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.array = [(10, 'A'), (15, 'B')]
        >>> priority_queue_test.cur_size = len(priority_queue_test.array)
        >>> priority_queue_test.pos = {'A': 0, 'B': 1}
        >>> priority_queue_test.insert((5, 'C'))
        >>> priority_queue_test.extract_min()
        'C'
        >>> priority_queue_test.array[0]
        (10, 'A')
        """
        min_node = self.array[0][1]
        self.array[0] = self.array[self.cur_size - 1]
        self.cur_size -= 1
        self.min_heapify(0)
        del self.pos[min_node]
        return min_node

    def left(self, i):
        """
        返回左孩子的索引

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.left(0)
        1
        >>> priority_queue_test.left(1)
        3
        """
        return 2 * i + 1

    def right(self, i):
        """
        返回右孩子的索引

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.right(0)
        2
        >>> priority_queue_test.right(1)
        4
        """
        return 2 * i + 2

    def par(self, i):
        """
        返回父级的索引

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.par(1)
        0
        >>> priority_queue_test.par(2)
        1
        >>> priority_queue_test.par(4)
        2
        """
        return math.floor(i / 2)

    def swap(self, i, j) -> None:
        """
        交换索引 i 和 j 处的分布式元素，更新 pos{}

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.array = [(10, 'A'), (15, 'B')]
        >>> priority_queue_test.cur_size = len(priority_queue_test.array)
        >>> priority_queue_test.pos = {'A': 0, 'B': 1}
        >>> priority_queue_test.swap(0, 1)
        >>> priority_queue_test.array
        [(15, 'B'), (10, 'A')]
        >>> priority_queue_test.pos
        {'A': 1, 'B': 0}
        """
        self.pos[self.array[i][1]] = j
        self.pos[self.array[j][1]] = i
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp

    def decrease_key(self, tup, new_d) -> None:
        """
        减少给定元组的键值，假设new_d最多为old_d。

        示例：
        >>> priority_queue_test = PriorityQueue()
        >>> priority_queue_test.array = [(10, 'A'), (15, 'B')]
        >>> priority_queue_test.cur_size = len(priority_queue_test.array)
        >>> priority_queue_test.pos = {'A': 0, 'B': 1}
        >>> priority_queue_test.decrease_key((10, 'A'), 5)
        >>> priority_queue_test.array
        [(5, 'A'), (15, 'B')]
        """
        idx = self.pos[tup[1]]
        # 假设 new_d 至多为 old_d
        self.array[idx] = (new_d, tup[1])
        while idx > 0 and self.array[self.par(idx)][0] > self.array[idx][0]:
            self.swap(idx, self.par(idx))
            idx = self.par(idx)


class Graph:
    def __init__(self, num) -> None:
        """
        图类构造函数

        示例：
        >>> graph_test = Graph(1)
        >>> graph_test.num_nodes
        1
        >>> graph_test.dist
        [0]
        >>> graph_test.par
        [-1]
        >>> graph_test.adjList
        {}
        """
        self.adjList = {}  # 存储图： u -> (v,w)
        self.num_nodes = num  # 图中的节点数
        # 存储距源顶点的距离
        self.dist = [0] * self.num_nodes
        self.par = [-1] * self.num_nodes  # 存储路径

    def add_edge(self, u, v, w) -> None:
        """
        添加从节点 u 到 v 和 v 到 u 的边，权重为 w：u (w)-> v, v (w) -> u

        示例：
        >>> graph_test = Graph(1)
        >>> graph_test.add_edge(1, 2, 1)
        >>> graph_test.add_edge(2, 3, 2)
        >>> graph_test.adjList
        {1: [(2, 1)], 2: [(1, 1), (3, 2)], 3: [(2, 2)]}
        """
        # 检查你是否已经在图表中
        if u in self.adjList:
            self.adjList[u].append((v, w))
        else:
            self.adjList[u] = [(v, w)]

        # 假设无向图
        if v in self.adjList:
            self.adjList[v].append((u, w))
        else:
            self.adjList[v] = [(u, w)]

    def show_graph(self) -> None:
        """
        显示图：u -> v(w)

        示例：
        >>> graph_test = Graph(1)
        >>> graph_test.add_edge(1, 2, 1)
        >>> graph_test.show_graph()
        1 -> 2(1)
        2 -> 1(1)
        >>> graph_test.add_edge(2, 3, 2)
        >>> graph_test.show_graph()
        1 -> 2(1)
        2 -> 1(1) -> 3(2)
        3 -> 2(2)
        """
        for u in self.adjList:
            print(u, "->", " -> ".join(str(f"{v}({w})") for v, w in self.adjList[u]))

    def dijkstra(self, src) -> None:
        """
        迪杰斯特拉算法

        示例：
        >>> graph_test = Graph(3)
        >>> graph_test.add_edge(0, 1, 2)
        >>> graph_test.add_edge(1, 2, 2)
        >>> graph_test.dijkstra(0)
        Distance from node: 0
        Node 0 has distance: 0
        Node 1 has distance: 2
        Node 2 has distance: 4
        >>> graph_test.dist
        [0, 2, 4]

        >>> graph_test = Graph(2)
        >>> graph_test.add_edge(0, 1, 2)
        >>> graph_test.dijkstra(0)
        Distance from node: 0
        Node 0 has distance: 0
        Node 1 has distance: 2
        >>> graph_test.dist
        [0, 2]

        >>> graph_test = Graph(3)
        >>> graph_test.add_edge(0, 1, 2)
        >>> graph_test.dijkstra(0)
        Distance from node: 0
        Node 0 has distance: 0
        Node 1 has distance: 2
        Node 2 has distance: 0
        >>> graph_test.dist
        [0, 2, 0]

        >>> graph_test = Graph(3)
        >>> graph_test.add_edge(0, 1, 2)
        >>> graph_test.add_edge(1, 2, 2)
        >>> graph_test.add_edge(0, 2, 1)
        >>> graph_test.dijkstra(0)
        Distance from node: 0
        Node 0 has distance: 0
        Node 1 has distance: 2
        Node 2 has distance: 1
        >>> graph_test.dist
        [0, 2, 1]

        >>> graph_test = Graph(4)
        >>> graph_test.add_edge(0, 1, 4)
        >>> graph_test.add_edge(1, 2, 2)
        >>> graph_test.add_edge(2, 3, 1)
        >>> graph_test.add_edge(0, 2, 3)
        >>> graph_test.dijkstra(0)
        Distance from node: 0
        Node 0 has distance: 0
        Node 1 has distance: 4
        Node 2 has distance: 3
        Node 3 has distance: 4
        >>> graph_test.dist
        [0, 4, 3, 4]

        >>> graph_test = Graph(4)
        >>> graph_test.add_edge(0, 1, 4)
        >>> graph_test.add_edge(1, 2, 2)
        >>> graph_test.add_edge(2, 3, 1)
        >>> graph_test.add_edge(0, 2, 7)
        >>> graph_test.dijkstra(0)
        Distance from node: 0
        Node 0 has distance: 0
        Node 1 has distance: 4
        Node 2 has distance: 6
        Node 3 has distance: 7
        >>> graph_test.dist
        [0, 4, 6, 7]
        """
        # 刷新 par[] 中的旧垃圾值
        self.par = [-1] * self.num_nodes
        # src 是源节点
        self.dist[src] = 0
        q = PriorityQueue()
        q.insert((0, src))  # (dist from src, node)
        for u in self.adjList:
            if u != src:
                self.dist[u] = sys.maxsize  # 无限
                self.par[u] = -1

        while not q.is_empty():
            u = q.extract_min()  # 返回与源的最小距离的节点
            # 更新您的所有邻居的距离
            # 如果他们前面的距离是无限，那么他们将推入 Q
            for v, w in self.adjList[u]:
                new_dist = self.dist[u] + w
                if self.dist[v] > new_dist:
                    if self.dist[v] == sys.maxsize:
                        q.insert((new_dist, v))
                    else:
                        q.decrease_key((self.dist[v], v), new_dist)
                    self.dist[v] = new_dist
                    self.par[v] = u

        # 显示距src的最短距离
        self.show_distances(src)

    def show_distances(self, src) -> None:
        """
        显示从 src 到所有其他节点的距离

        示例：
        >>> graph_test = Graph(1)
        >>> graph_test.show_distances(0)
        Distance from node: 0
        Node 0 has distance: 0
        """
        print(f"Distance from node: {src}")
        for u in range(self.num_nodes):
            print(f"Node {u} has distance: {self.dist[u]}")

    def show_path(self, src, dest) -> None:
        """
        显示从 src 到 dest 的最短路径。
        警告：*在*调用 dijkstra 之后使用它。

        示例：
        >>> graph_test = Graph(4)
        >>> graph_test.add_edge(0, 1, 1)
        >>> graph_test.add_edge(1, 2, 2)
        >>> graph_test.add_edge(2, 3, 3)
        >>> graph_test.dijkstra(0)
        Distance from node: 0
        Node 0 has distance: 0
        Node 1 has distance: 1
        Node 2 has distance: 3
        Node 3 has distance: 6
        >>> graph_test.show_path(0, 3)  # doctest: +NORMALIZE_WHITESPACE
        ----Path to reach 3 from 0----
        0 -> 1 -> 2 -> 3
        Total cost of path:  6
        """
        path = []
        cost = 0
        temp = dest
        # 从dest回溯到src
        while self.par[temp] != -1:
            path.append(temp)
            if temp != src:
                for v, w in self.adjList[temp]:
                    if v == self.par[temp]:
                        cost += w
                        break
            temp = self.par[temp]
        path.append(src)
        path.reverse()

        print(f"----Path to reach {dest} from {src}----")
        for u in path:
            print(f"{u}", end=" ")
            if u != dest:
                print("-> ", end="")

        print("\nTotal cost of path: ", cost)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    graph = Graph(9)
    graph.add_edge(0, 1, 4)
    graph.add_edge(0, 7, 8)
    graph.add_edge(1, 2, 8)
    graph.add_edge(1, 7, 11)
    graph.add_edge(2, 3, 7)
    graph.add_edge(2, 8, 2)
    graph.add_edge(2, 5, 4)
    graph.add_edge(3, 4, 9)
    graph.add_edge(3, 5, 14)
    graph.add_edge(4, 5, 10)
    graph.add_edge(5, 6, 2)
    graph.add_edge(6, 7, 1)
    graph.add_edge(6, 8, 6)
    graph.add_edge(7, 8, 7)
    graph.show_graph()
    graph.dijkstra(0)
    graph.show_path(0, 4)

# 输出
# 0 -> 1(4) -> 7(8)
# 1 -> 0(4) -> 2(8) -> 7(11)
# 7 -> 0(8) -> 1(11) -> 6(1) -> 8(7)
# 2 -> 1(8) -> 3(7) -> 8(2) -> 5(4)
# 3 -> 2(7) -> 4(9) -> 5(14)
# 8 -> 2(2) -> 6(6) -> 7(7)
# 5 -> 2(4) -> 3(14) -> 4(10) -> 6(2)
# 4 -> 3(9) -> 5(10)
# 6 -> 5(2) -> 7(1) -> 8(6)
# 距节点的距离：0
# 节点 0 的距离：0
# 节点 1 的距离：4
# 节点 2 的距离：12
# 节点 3 的距离：19
# 节点 4 的距离：21
# 节点 5 的距离：11
# 节点 6 的距离：9
# 节点 7 的距离：8
# 节点 8 的距离：14
# ----Path to reach 4 from 0----
# 0 -> 7 -> 6 -> 5 -> 4
# 路径总代价：21
