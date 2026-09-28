from collections import deque
from math import floor
from random import random
from time import time

# 如果未分配，则默认权重为 1，但所有实现均已加权


class DirectedGraph:
    def __init__(self) -> None:
        self.graph = {}

    def add_pair(self, u, v, w=1) -> None:
        """
        添加权重为 w 的有向边 u->v。
        添加顶点和边
        添加重量是可选的
        处理重复

        >>> dg = DirectedGraph()
        >>> dg.add_pair(-1,2)
        >>> dg.add_pair(1,3,5)
        >>> dg.add_pair(1,3,5)
        >>> dg.add_pair(1,3,6)
        >>> dg.all_nodes()
        [-1, 2, 1, 3]
        >>> dg.graph[1]
        [[5, 3], [6, 3]]
        """
        if self.graph.get(u):
            if self.graph[u].count([w, v]) == 0:
                self.graph[u].append([w, v])
        else:
            self.graph[u] = [[w, v]]
        if not self.graph.get(v):
            self.graph[v] = []

    def all_nodes(self):
        """
        返回图中所有节点的列表。
        >>> dg = DirectedGraph()
        >>> dg.all_nodes()
        []
        >>> dg.add_pair(1,1)
        >>> dg.all_nodes()
        [1]
        >>> dg.add_pair(2,3,3)
        >>> dg.all_nodes()
        [1, 2, 3]
        """
        return list(self.graph)

    # 如果输入不存在则处理
    def remove_pair(self, u, v) -> None:
        """
        删除所有边 u->v（如果存在）。
        >>> dg = DirectedGraph()
        >>> dg.remove_pair(1,2) # silently exits
        >>> dg.add_pair(0,5,2)
        >>> dg.graph[0]
        [[2, 5]]
        >>> dg.remove_pair(5,0)
        >>> dg.graph[0]
        [[2, 5]]
        >>> dg.remove_pair(0,5)
        >>> dg.graph[0]
        []
        """
        if self.graph.get(u):
            for _ in self.graph[u]:
                if _[1] == v:
                    self.graph[u].remove(_)

    # 如果没有指定目的地，则默认值为 -1
    def dfs(self, s=-2, d=-1):
        """
        从 s 执行深度优先搜索以找到 d。
        以列表形式返回路径s->d。
        如果未找到 d，则从 s 返回 dfs
        >>> dg = DirectedGraph()
        >>> dg.dfs()
        []
        >>> dg.add_pair(1,1)
        >>> dg.dfs(1,1)
        [1]
        >>> dg = DirectedGraph()
        >>> dg.add_pair(0,1)
        >>> dg.add_pair(0,2)
        >>> dg.add_pair(1,3)
        >>> dg.add_pair(1,4)
        >>> dg.add_pair(1,5)
        >>> dg.add_pair(2,5)
        >>> dg.add_pair(5,6)
        >>> dg.dfs(0,6)
        [0, 2, 5, 6]
        >>> dg.dfs(1,6)
        [1, 5, 6]
        >>> dg.dfs()
        [0, 2, 5, 6, 1, 4, 3]
        >>> dg.dfs(1,0)
        [1, 5, 6, 4, 3]
        """
        stack = []
        visited = []
        if s == -2:
            if self.graph.get(s, None):
                pass  # -2 is a node
            elif len(self.graph) > 0:
                s = next(iter(self.graph))
            else:
                return []  # 图为空
        stack.append(s)

        # 运行dfs
        while len(stack) > 0:
            s = stack.pop()
            visited.append(s)
            # 如果到达，则返回
            if s == d:
                break

            # 将未访问过的子节点添加到堆栈中
            for _, ss in self.graph[s]:
                if visited.count(ss) < 1:
                    stack.append(ss)
        return visited

    # c 是你想要的节点数，如果你保留它或者将 -1 传递给函数
    # 计数将从 10 到 10000 随机
    def fill_graph_randomly(self, c=-1) -> None:
        if c == -1:
            c = floor(random() * 10000) + 10
        for i in range(c):
            # 每个顶点最多有 100 条边
            for _ in range(floor(random() * 102) + 1):
                n = floor(random() * c) + 1
                if n != i:
                    self.add_pair(i, n, 1)

    def bfs(self, s=-2):
        """
        从 s 执行广度优先搜索
        返回列表。
        >>> dg = DirectedGraph()
        >>> dg.bfs()
        []
        >>> dg.add_pair(1,1)
        >>> dg.bfs(1)
        [1]
        >>> dg = DirectedGraph()
        >>> dg.add_pair(0,1)
        >>> dg.add_pair(0,2)
        >>> dg.add_pair(1,3)
        >>> dg.add_pair(1,4)
        >>> dg.add_pair(1,5)
        >>> dg.add_pair(2,5)
        >>> dg.add_pair(5,6)
        >>> dg.bfs(0)
        [0, 1, 2, 3, 4, 5, 6]
        >>> dg.bfs(1)
        [1, 3, 4, 5, 6]
        >>> dg.bfs()
        [0, 1, 2, 3, 4, 5, 6]
        """
        d = deque()
        visited = []
        if s == -2:
            if self.graph.get(s, None):
                pass  # -2 is a node
            elif len(self.graph) > 0:
                s = next(iter(self.graph))
            else:
                return []  # 图为空
        d.append(s)
        visited.append(s)
        # 运行bfs
        while d:
            s = d.popleft()
            if len(self.graph[s]) != 0:
                for node in self.graph[s]:
                    if visited.count(node[1]) < 1:
                        d.append(node[1])
                        visited.append(node[1])
        return visited

    def in_degree(self, u):
        count = 0
        for x in self.graph:
            for y in self.graph[x]:
                if y[1] == u:
                    count += 1
        return count

    def out_degree(self, u):
        return len(self.graph[u])

    def topological_sort(self, s=-2):
        stack = []
        visited = []
        if s == -2:
            s = next(iter(self.graph))
        stack.append(s)
        visited.append(s)
        ss = s
        sorted_nodes = []

        while True:
            # 检查是否存在非孤立节点
            if len(self.graph[s]) != 0:
                ss = s
                for node in self.graph[s]:
                    if visited.count(node[1]) < 1:
                        stack.append(node[1])
                        visited.append(node[1])
                        ss = node[1]
                        break

            # 检查是否所有的孩子都被访问过
            if s == ss:
                sorted_nodes.append(stack.pop())
                if len(stack) != 0:
                    s = stack[len(stack) - 1]
            else:
                s = ss

            # 检查是否已经到达起点
            if len(stack) == 0:
                return sorted_nodes

    def cycle_nodes(self):
        stack = []
        visited = []
        s = next(iter(self.graph))
        stack.append(s)
        visited.append(s)
        parent = -2
        indirect_parents = []
        ss = s
        on_the_way_back = False
        anticipating_nodes = set()

        while True:
            # 检查是否存在非孤立节点
            if len(self.graph[s]) != 0:
                ss = s
                for node in self.graph[s]:
                    if (
                        visited.count(node[1]) > 0
                        and node[1] != parent
                        and indirect_parents.count(node[1]) > 0
                        and not on_the_way_back
                    ):
                        len_stack = len(stack) - 1
                        while len_stack >= 0:
                            if stack[len_stack] == node[1]:
                                anticipating_nodes.add(node[1])
                                break
                            anticipating_nodes.add(stack[len_stack])
                            len_stack -= 1
                    if visited.count(node[1]) < 1:
                        stack.append(node[1])
                        visited.append(node[1])
                        ss = node[1]
                        break

            # 检查是否所有的孩子都被访问过
            if s == ss:
                stack.pop()
                on_the_way_back = True
                if len(stack) != 0:
                    s = stack[len(stack) - 1]
            else:
                on_the_way_back = False
                indirect_parents.append(parent)
                parent = s
                s = ss

            # 检查是否已经到达起点
            if len(stack) == 0:
                return list(anticipating_nodes)

    def has_cycle(self) -> bool | None:
        stack = []
        visited = []
        s = next(iter(self.graph))
        stack.append(s)
        visited.append(s)
        parent = -2
        indirect_parents = []
        ss = s
        on_the_way_back = False
        anticipating_nodes = set()

        while True:
            # 检查是否存在非孤立节点
            if len(self.graph[s]) != 0:
                ss = s
                for node in self.graph[s]:
                    if (
                        visited.count(node[1]) > 0
                        and node[1] != parent
                        and indirect_parents.count(node[1]) > 0
                        and not on_the_way_back
                    ):
                        len_stack_minus_one = len(stack) - 1
                        while len_stack_minus_one >= 0:
                            if stack[len_stack_minus_one] == node[1]:
                                anticipating_nodes.add(node[1])
                                break
                            return True
                    if visited.count(node[1]) < 1:
                        stack.append(node[1])
                        visited.append(node[1])
                        ss = node[1]
                        break

            # 检查是否所有的孩子都被访问过
            if s == ss:
                stack.pop()
                on_the_way_back = True
                if len(stack) != 0:
                    s = stack[len(stack) - 1]
            else:
                on_the_way_back = False
                indirect_parents.append(parent)
                parent = s
                s = ss

            # 检查是否已经到达起点
            if len(stack) == 0:
                return False

    def dfs_time(self, s=-2, e=-1):
        begin = time()
        self.dfs(s, e)
        end = time()
        return end - begin

    def bfs_time(self, s=-2):
        begin = time()
        self.bfs(s)
        end = time()
        return end - begin


class Graph:
    def __init__(self) -> None:
        self.graph = {}

    # 添加顶点和边
    # 添加重量是可选的
    # 处理重复
    def add_pair(self, u, v, w=1) -> None:
        # 检查 u 是否存在
        if self.graph.get(u):
            # 如果已经有边
            if self.graph[u].count([w, v]) == 0:
                self.graph[u].append([w, v])
        else:
            # 如果你不存在
            self.graph[u] = [[w, v]]
        # 添加另一种方式
        if self.graph.get(v):
            # 如果已经有边
            if self.graph[v].count([w, u]) == 0:
                self.graph[v].append([w, u])
        else:
            # 如果你不存在
            self.graph[v] = [[w, u]]

    # 如果输入不存在则处理
    def remove_pair(self, u, v) -> None:
        if self.graph.get(u):
            for _ in self.graph[u]:
                if _[1] == v:
                    self.graph[u].remove(_)
        # 反过来
        if self.graph.get(v):
            for _ in self.graph[v]:
                if _[1] == u:
                    self.graph[v].remove(_)

    # 如果没有指定目的地，则默认值为 -1
    def dfs(self, s=-2, d=-1):
        """
        从 s 执行深度优先搜索以找到 d。
        以列表形式返回路径s->d。
        如果未找到 d，则从 s 返回 dfs
        >>> ug = Graph()
        >>> ug.dfs()
        []
        >>> ug.add_pair(1,1)
        >>> ug.dfs(1,1)
        [1]
        >>> ug = Graph()
        >>> ug.add_pair(0,1)
        >>> ug.add_pair(0,2)
        >>> ug.add_pair(1,3)
        >>> ug.add_pair(1,4)
        >>> ug.add_pair(1,5)
        >>> ug.add_pair(2,5)
        >>> ug.add_pair(5,6)
        >>> ug.dfs(0,6)
        [0, 2, 5, 6]
        >>> ug.dfs(1,6)
        [1, 5, 6]
        >>> ug.dfs()
        [0, 2, 5, 6, 1, 4, 3]
        >>> ug.dfs(1,0)
        [1, 5, 6, 2, 0]
        """
        stack = []
        visited = []
        if s == -2:
            if self.graph.get(s, None):
                pass  # -2 is a node
            elif len(self.graph) > 0:
                s = next(iter(self.graph))
            else:
                return []  # 图为空
        stack.append(s)

        # 运行dfs
        while len(stack) > 0:
            s = stack.pop()
            if visited.count(s) == 1:
                continue
            visited.append(s)
            # 如果到达，则返回
            if s == d:
                break

            # 将未访问过的子节点添加到堆栈中
            for _, ss in self.graph[s]:
                if visited.count(ss) < 1:
                    stack.append(ss)
        return visited

    # c 是你想要的节点数，如果你保留它或者将 -1 传递给函数
    # 计数将从 10 到 10000 随机
    def fill_graph_randomly(self, c=-1) -> None:
        if c == -1:
            c = floor(random() * 10000) + 10
        for i in range(c):
            # 每个顶点最多有 100 条边
            for _ in range(floor(random() * 102) + 1):
                n = floor(random() * c) + 1
                if n != i:
                    self.add_pair(i, n, 1)

    def bfs(self, s=-2):
        """
        从 s 执行广度优先搜索
        返回列表。
        >>> ug = Graph()
        >>> ug.bfs()
        []
        >>> ug.add_pair(1,1)
        >>> ug.bfs(1)
        [1]
        >>> ug = Graph()
        >>> ug.add_pair(0,1)
        >>> ug.add_pair(0,2)
        >>> ug.add_pair(1,3)
        >>> ug.add_pair(1,4)
        >>> ug.add_pair(1,5)
        >>> ug.add_pair(2,5)
        >>> ug.add_pair(5,6)
        >>> ug.bfs(0)
        [0, 1, 2, 3, 4, 5, 6]
        >>> ug.bfs(1)
        [1, 0, 3, 4, 5, 2, 6]
        >>> ug.bfs()
        [0, 1, 2, 3, 4, 5, 6]
        """
        d = deque()
        visited = []
        if s == -2:
            if self.graph.get(s, None):
                pass  # -2 is a node
            elif len(self.graph) > 0:
                s = next(iter(self.graph))
            else:
                return []  # 图为空
        d.append(s)
        visited.append(s)
        while d:
            s = d.popleft()
            if len(self.graph[s]) != 0:
                for node in self.graph[s]:
                    if visited.count(node[1]) < 1:
                        d.append(node[1])
                        visited.append(node[1])
        return visited

    def degree(self, u):
        return len(self.graph[u])

    def cycle_nodes(self):
        stack = []
        visited = []
        s = next(iter(self.graph))
        stack.append(s)
        visited.append(s)
        parent = -2
        indirect_parents = []
        ss = s
        on_the_way_back = False
        anticipating_nodes = set()

        while True:
            # 检查是否存在非孤立节点
            if len(self.graph[s]) != 0:
                ss = s
                for node in self.graph[s]:
                    if (
                        visited.count(node[1]) > 0
                        and node[1] != parent
                        and indirect_parents.count(node[1]) > 0
                        and not on_the_way_back
                    ):
                        len_stack = len(stack) - 1
                        while len_stack >= 0:
                            if stack[len_stack] == node[1]:
                                anticipating_nodes.add(node[1])
                                break
                            anticipating_nodes.add(stack[len_stack])
                            len_stack -= 1
                    if visited.count(node[1]) < 1:
                        stack.append(node[1])
                        visited.append(node[1])
                        ss = node[1]
                        break

            # 检查是否所有的孩子都被访问过
            if s == ss:
                stack.pop()
                on_the_way_back = True
                if len(stack) != 0:
                    s = stack[len(stack) - 1]
            else:
                on_the_way_back = False
                indirect_parents.append(parent)
                parent = s
                s = ss

            # 检查是否已经到达起点
            if len(stack) == 0:
                return list(anticipating_nodes)

    def has_cycle(self) -> bool | None:
        stack = []
        visited = []
        s = next(iter(self.graph))
        stack.append(s)
        visited.append(s)
        parent = -2
        indirect_parents = []
        ss = s
        on_the_way_back = False
        anticipating_nodes = set()

        while True:
            # 检查是否存在非孤立节点
            if len(self.graph[s]) != 0:
                ss = s
                for node in self.graph[s]:
                    if (
                        visited.count(node[1]) > 0
                        and node[1] != parent
                        and indirect_parents.count(node[1]) > 0
                        and not on_the_way_back
                    ):
                        len_stack_minus_one = len(stack) - 1
                        while len_stack_minus_one >= 0:
                            if stack[len_stack_minus_one] == node[1]:
                                anticipating_nodes.add(node[1])
                                break
                            return True
                    if visited.count(node[1]) < 1:
                        stack.append(node[1])
                        visited.append(node[1])
                        ss = node[1]
                        break

            # 检查是否所有的孩子都被访问过
            if s == ss:
                stack.pop()
                on_the_way_back = True
                if len(stack) != 0:
                    s = stack[len(stack) - 1]
            else:
                on_the_way_back = False
                indirect_parents.append(parent)
                parent = s
                s = ss

            # 检查是否已经到达起点
            if len(stack) == 0:
                return False

    def all_nodes(self):
        return list(self.graph)

    def dfs_time(self, s=-2, e=-1):
        begin = time()
        self.dfs(s, e)
        end = time()
        return end - begin

    def bfs_time(self, s=-2):
        begin = time()
        self.bfs(s)
        end = time()
        return end - begin
