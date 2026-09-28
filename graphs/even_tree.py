"""
给你一棵树（一个没有循环的简单图示）。这棵树有N个
节点编号从 1 到 N，以节点 1 为根。

找出可以从树上删除以获得森林的最大边数
这样森林的每个连通部分都包含偶数个
节点。

约束条件
2 <= 2 <= 100

注意：树的输入总是可以分解为
包含偶数个节点的组件。
"""

# pylint: disable=invalid-name
from collections import defaultdict


def dfs(start: int) -> int:
    """DFS遍历"""
    # pylint: disable=redefined-outer-name
    ret = 1
    visited[start] = True
    for v in tree[start]:
        if v not in visited:
            ret += dfs(v)
    if ret % 2 == 0:
        cuts.append(start)
    return ret


def even_tree() -> None:
    """
    2 1
    3 1
    4 3
    5 2
    6 1
    7 2
    8 6
    9 8
    10 8
    删除边 (1,3) 和 (1,6)，我们可以获得所需的结果 2。
    """
    dfs(1)


if __name__ == "__main__":
    n, m = 10, 9
    tree = defaultdict(list)
    visited: dict[int, bool] = {}
    cuts: list[int] = []
    count = 0
    edges = [(2, 1), (3, 1), (4, 3), (5, 2), (6, 1), (7, 2), (8, 6), (9, 8), (10, 8)]
    for u, v in edges:
        tree[u].append(v)
        tree[v].append(u)
    even_tree()
    print(len(cuts) - 1)
