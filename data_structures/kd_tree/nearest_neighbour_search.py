#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11532
#  https://github.com/TheAlgorithms/Python/pull/11532
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

from data_structures.kd_tree.kd_node import KDNode


def nearest_neighbour_search(
    root: KDNode | None, query_point: list[float]
) -> tuple[list[float] | None, float, int]:
    """
    执行 最近 邻居 搜索 在 KD-树 用于 给定 查询 点。

    参数：
        根节点 (KDNode | None): 根节点 的 KD-树。
        query_point (列表[浮点数]): 点 用于 其 最近 邻居
                                    是 being 已搜索。

    返回值：
        元组[列表[浮点数] | None，浮点数，int]：
            - 最近 点 找到 在 KD-树 到 查询 点,
              或 None 如果 没有 点 是 找到。
            - squared 距离 到 最近 点。
            - 节点数量 visited during 搜索。
    """
    nearest_point: list[float] | None = None
    nearest_dist: float = float("inf")
    nodes_visited: int = 0

    def search(node: KDNode | None, depth: int = 0) -> None:
        """
        递归地 搜索 最近 邻居 在 KD-树。

        参数：
            节点: 当前节点 在 KD-树。
            深度: 当前 深度 在 KD-树。
        """
        nonlocal nearest_point, nearest_dist, nodes_visited
        if node is None:
            return

        nodes_visited += 1

        # 计算 当前 距离 (squared 距离)
        current_point = node.point
        current_dist = sum(
            (query_coord - point_coord) ** 2
            for query_coord, point_coord in zip(query_point, current_point)
        )

        # 更新 最近 点 如果 当前节点 是 closer
        if nearest_point is None or current_dist < nearest_dist:
            nearest_point = current_point
            nearest_dist = current_dist

        # Determine 其 子树 到 搜索 第一个 (基于 在 axis 并且 查询 点)
        k = len(query_point)  # Dimensionality 的 点
        axis = depth % k

        if query_point[axis] <= current_point[axis]:
            nearer_subtree = node.left
            further_subtree = node.right
        else:
            nearer_subtree = node.right
            further_subtree = node.left

        # 搜索 nearer 子树 第一个
        search(nearer_subtree, depth + 1)

        # 如果 further 子树 具有 closer 点
        if (query_point[axis] - current_point[axis]) ** 2 < nearest_dist:
            search(further_subtree, depth + 1)

    search(root, 0)
    return nearest_point, nearest_dist, nodes_visited
