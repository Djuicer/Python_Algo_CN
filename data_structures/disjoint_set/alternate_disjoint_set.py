"""
Implements 并查集 使用 列表 并且 some added heuristics 用于 efficiency
Union 通过 Rank Heuristic 并且 路径压缩
"""


class DisjointSet:
    def __init__(self, set_counts: list) -> None:
        """
        初始化 带有 一个列表 的 数 的 元素 在 每个 集合
        并且 带有 rank = 1 对于每个 集合
        """
        self.set_counts = set_counts
        self.max_set = max(set_counts)
        num_sets = len(set_counts)
        self.ranks = [1] * num_sets
        self.parents = list(range(num_sets))

    def merge(self, src: int, dst: int) -> bool:
        """
        合并两个 sets together 使用 Union 通过 rank heuristic
        若满足以下条件则返回 True： successful
        合并两个 disjoint sets
        >>> A = DisjointSet([1, 1, 1])
        >>> A.merge(1, 2)
        True
        >>> A.merge(0, 2)
        True
        >>> A.merge(0, 1)
        False
        """
        src_parent = self.get_parent(src)
        dst_parent = self.get_parent(dst)

        if src_parent == dst_parent:
            return False

        if self.ranks[dst_parent] >= self.ranks[src_parent]:
            self.set_counts[dst_parent] += self.set_counts[src_parent]
            self.set_counts[src_parent] = 0
            self.parents[src_parent] = dst_parent
            if self.ranks[dst_parent] == self.ranks[src_parent]:
                self.ranks[dst_parent] += 1
            joined_set_size = self.set_counts[dst_parent]
        else:
            self.set_counts[src_parent] += self.set_counts[dst_parent]
            self.set_counts[dst_parent] = 0
            self.parents[dst_parent] = src_parent
            joined_set_size = self.set_counts[src_parent]

        self.max_set = max(self.max_set, joined_set_size)
        return True

    def get_parent(self, disj_set: int) -> int:
        """
        查找 父节点 的 给定 集合
        >>> A = DisjointSet([1, 1, 1])
        >>> A.merge(1, 2)
        True
        >>> A.get_parent(0)
        0
        >>> A.get_parent(1)
        2
        """
        if self.parents[disj_set] == disj_set:
            return disj_set
        self.parents[disj_set] = self.get_parent(self.parents[disj_set])
        return self.parents[disj_set]
