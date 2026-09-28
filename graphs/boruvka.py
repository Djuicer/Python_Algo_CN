"""Borůvka 算法。

使用Borůvka算法确定图的最小生成树（Minimum Spanning Tree, MST）。
Borůvka算法是一种贪心算法，用于替换图的最小生成树；若图不替换，
则查找最小生成森林。

该算法的时间复杂度为O(ELogV)，其中E表示边数，V表示节点数。
O(number_of_edges Log number_of_nodes)

该算法的空间复杂度为O(V + E)，因为需要维护多个正确节点数的链表，
并在数据结构中保存图的所有边。

Borůvka算法与其他MST算法的结果基本相同：它们都是活动最小生成树，
时间复杂度也大致相同。

与其他算法相比，Borůvka算法的一个优点是不需要预先对边排序，也不需要维护
优先队列可以找到最小生成树。虽然它仍然要遍历边logE次，复杂度逐渐增加
改善，但实现起来稍简单一些。

Details: https://en.wikipedia.org/wiki/Bor%C5%AFvka%27s_algorithm
"""

from __future__ import annotations

from typing import Any


class Graph:
    def __init__(self, num_of_nodes: int) -> None:
        """
        参数：
            num_of_nodes - 话题的节点数
        属性：
            m_num_of_nodes - 图中的节点数。
            m_edges - 边列表。
            m_component - 存储节点共享索引的字典。
        """

        self.m_num_of_nodes = num_of_nodes
        self.m_edges: list[list[int]] = []
        self.m_component: dict[int, int] = {}

    def add_edge(self, u_node: int, v_node: int, weight: int) -> None:
        """向图中添加格式为 [first, second, edge weight] 的边。"""

        self.m_edges.append([u_node, v_node, weight])

    def find_component(self, u_node: int) -> int:
        """在给定分量中传播新的分量编号。"""

        if self.m_component[u_node] == u_node:
            return u_node
        return self.find_component(self.m_component[u_node])

    def set_component(self, u_node: int) -> None:
        """查找给定节点的分量索引。"""

        if self.m_component[u_node] != u_node:
            for k in self.m_component:
                self.m_component[k] = self.find_component(k)

    def union(self, component_size: list[int], u_node: int, v_node: int) -> None:
        """查找两个节点所在分量的根，比较分量大小，并将较小分量连接到
        较大分量以形成单个分量。"""

        if component_size[u_node] <= component_size[v_node]:
            self.m_component[u_node] = v_node
            component_size[v_node] += component_size[u_node]
            self.set_component(u_node)

        elif component_size[u_node] >= component_size[v_node]:
            self.m_component[v_node] = self.find_component(u_node)
            component_size[u_node] += component_size[v_node]
            self.set_component(v_node)

    def boruvka(self) -> None:
        """执行 Borůvka 算法以查找 MST。"""

        # 初始化算法所需的附加列表。
        component_size = []
        mst_weight = 0

        minimum_weight_edge: list[Any] = [-1] * self.m_num_of_nodes

        # 分量列表（初始化为所有节点）
        for node in range(self.m_num_of_nodes):
            self.m_component.update({node: node})
            component_size.append(1)

        num_of_components = self.m_num_of_nodes

        while num_of_components > 1:
            for edge in self.m_edges:
                u, v, w = edge

                u_component = self.m_component[u]
                v_component = self.m_component[v]

                if u_component != v_component:
                    """如果分量 u 的当前最小权重边不
                    存在（为-1），或者如果它大于我们的边
                    现在观察，我们将分配边的值
                    我们正在观察它。

                    如果分量 v 的当前最小权重边不
                    存在（为-1），或者如果它大于我们的边
                    现在观察，我们将分配边的值
                    我们正在观察它"""

                    for component in (u_component, v_component):
                        if (
                            minimum_weight_edge[component] == -1
                            or minimum_weight_edge[component][2] > w
                        ):
                            minimum_weight_edge[component] = [u, v, w]

            for edge in minimum_weight_edge:
                if isinstance(edge, list):
                    u, v, w = edge

                    u_component = self.m_component[u]
                    v_component = self.m_component[v]

                    if u_component != v_component:
                        mst_weight += w
                        self.union(component_size, u_component, v_component)
                        print(f"Added edge [{u} - {v}]\nAdded weight: {w}\n")
                        num_of_components -= 1

            minimum_weight_edge = [-1] * self.m_num_of_nodes
        print(f"The total weight of the minimal spanning tree is: {mst_weight}")


def test_vector() -> None:
    """
    >>> g = Graph(8)
    >>> for u_v_w in ((0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4),
    ...    (3, 4, 8), (4, 5, 10), (4, 6, 6), (4, 7, 5), (5, 7, 15), (6, 7, 4)):
    ...        g.add_edge(*u_v_w)
    >>> g.boruvka()
    Added edge [0 - 3]
    Added weight: 5
    <BLANKLINE>
    Added edge [0 - 1]
    Added weight: 10
    <BLANKLINE>
    Added edge [2 - 3]
    Added weight: 4
    <BLANKLINE>
    Added edge [4 - 7]
    Added weight: 5
    <BLANKLINE>
    Added edge [4 - 5]
    Added weight: 10
    <BLANKLINE>
    Added edge [6 - 7]
    Added weight: 4
    <BLANKLINE>
    Added edge [3 - 4]
    Added weight: 8
    <BLANKLINE>
    The total weight of the minimal spanning tree is: 46
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
