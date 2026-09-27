#!/usr/bin/env python3

# 此 Python 程序实现一种构建最优二叉搜索树（简称 BST）的动态规划算法，
# 性能为 O(n^2)。
#
# 最优 BST 问题的目标是为给定节点集合构建低代价 BST，
# 每个节点都有自己的键和频率。节点频率定义为该节点被搜索的次数。
# 二叉搜索树的搜索代价由以下公式给出：
#
# cost(1, n) = sum{i = 1 to n}((depth(node_i) + 1) * node_i_freq)
#
# 其中 n 是 BST 中的节点数。低代价 BST 的特点是总体搜索时间更短。
# 这是因为高频节点会被放在靠近树根的位置，而低频节点会被放在靠近叶节点的位置，
# 从而缩短最常见情况下的搜索时间。
import sys
from random import randint


class Node:
    """二叉搜索树节点。"""

    def __init__(self, key, freq) -> None:
        self.key = key
        self.freq = freq

    def __str__(self) -> str:
        """
        >>> str(Node(1, 2))
        'Node(key=1, freq=2)'
        """
        return f"Node(key={self.key}, freq={self.freq})"


def print_binary_search_tree(root, key, i, j, parent, is_left) -> None:
    """
    根据根表递归输出 BST。

    >>> key = [3, 8, 9, 10, 17, 21]
    >>> root = [[0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 3], [0, 0, 2, 3, 3, 3], \
                [0, 0, 0, 3, 3, 3], [0, 0, 0, 0, 4, 5], [0, 0, 0, 0, 0, 5]]
    >>> print_binary_search_tree(root, key, 0, 5, -1, False)
    8 is the root of the binary search tree.
    3 is the left child of key 8.
    10 is the right child of key 8.
    9 is the left child of key 10.
    21 is the right child of key 10.
    17 is the left child of key 21.
    """
    if i > j or i < 0 or j > len(root) - 1:
        return

    node = root[i][j]
    if parent == -1:  # 根节点没有父节点
        print(f"{key[node]} is the root of the binary search tree.")
    elif is_left:
        print(f"{key[node]} is the left child of key {parent}.")
    else:
        print(f"{key[node]} is the right child of key {parent}.")

    print_binary_search_tree(root, key, i, node - 1, key[node], True)
    print_binary_search_tree(root, key, node + 1, j, key[node], False)


def find_optimal_binary_search_tree(nodes) -> None:
    """
    此函数计算并输出最优二叉搜索树。
    以下动态规划算法的运行时间为 O(n^2)。
    根据 CLRS（算法导论）一书实现。
    https://en.wikipedia.org/wiki/Introduction_to_Algorithms

    >>> find_optimal_binary_search_tree([Node(12, 8), Node(10, 34), Node(20, 50), \
                                         Node(42, 3), Node(25, 40), Node(37, 30)])
    Binary search tree nodes:
    Node(key=10, freq=34)
    Node(key=12, freq=8)
    Node(key=20, freq=50)
    Node(key=25, freq=40)
    Node(key=37, freq=30)
    Node(key=42, freq=3)
    <BLANKLINE>
    The cost of optimal BST for given tree nodes is 324.
    20 is the root of the binary search tree.
    10 is the left child of key 20.
    12 is the right child of key 10.
    25 is the right child of key 20.
    37 is the right child of key 25.
    42 is the right child of key 37.
    """
    # 必须先对树节点排序；以下代码按升序排列键，并相应地重新排列其频率
    nodes.sort(key=lambda node: node.key)

    n = len(nodes)

    keys = [nodes[i].key for i in range(n)]
    freqs = [nodes[i].freq for i in range(n)]

    # 此 2D 数组存储整棵树的代价（尽可能最小）；对于单个键，代价等于该键的频率
    dp = [[freqs[i] if i == j else 0 for j in range(n)] for i in range(n)]
    # total[i][j] 存储 nodes 数组中 i 到 j（含）之间的键频率之和
    total = [[freqs[i] if i == j else 0 for j in range(n)] for i in range(n)]
    # 存储稍后用于构造二叉搜索树的树根
    root = [[i if i == j else 0 for j in range(n)] for i in range(n)]

    for interval_length in range(2, n + 1):
        for i in range(n - interval_length + 1):
            j = i + interval_length - 1

            dp[i][j] = sys.maxsize  # 将值设为“无穷大”
            total[i][j] = total[i][j - 1] + freqs[j]

            # 应用带安全边界处理的 Knuth 优化
            r_start = root[i][j - 1] if j > i else i
            r_end = root[i + 1][j] if i < j else j

            # 确保 r_start 和 r_end 位于有效边界内
            r_start = max(i, min(r_start, j))
            r_end = min(j, max(r_end, i))

            for r in range(r_start, r_end + 1):
                left = dp[i][r - 1] if r > i else 0  # 左子树的最优代价
                right = dp[r + 1][j] if r < j else 0  # 右子树的最优代价
                cost = left + total[i][j] + right

                if dp[i][j] > cost:
                    dp[i][j] = cost
                    root[i][j] = r

    print("Binary search tree nodes:")
    for node in nodes:
        print(node)

    print(f"\nThe cost of optimal BST for given tree nodes is {dp[0][n - 1]}.")
    print_binary_search_tree(root, keys, 0, n - 1, -1, False)


def main() -> None:
    # 二叉搜索树示例
    nodes = [Node(i, randint(1, 50)) for i in range(10, 0, -1)]
    find_optimal_binary_search_tree(nodes)


if __name__ == "__main__":
    main()
