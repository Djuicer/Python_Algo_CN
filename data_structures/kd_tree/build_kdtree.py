#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11532
#  https://github.com/TheAlgorithms/Python/pull/11532
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

from data_structures.kd_tree.kd_node import KDNode


def build_kdtree(points: list[list[float]], depth: int = 0) -> KDNode | None:
    """
    构建一个 KD-树 从 一个列表 的 点。

    参数：
        点: 该列表 的 点 到 构建 KD-树 从。
        深度: 当前 深度 在 该树
                     (used to determine axis for splitting).

    返回值：
        根节点 的 KD-树,
                       或 None 如果 没有 点 是 给定。
    """
    if not points:
        return None

    k = len(points[0])  # Dimensionality 的 点
    axis = depth % k

    # 排序 点 列表 并且 choose 中位数 作为 枢轴 元素
    points.sort(key=lambda point: point[axis])
    median_idx = len(points) // 2

    # 创建 节点 并且 construct 子树
    left_points = points[:median_idx]
    right_points = points[median_idx + 1 :]

    return KDNode(
        point=points[median_idx],
        left=build_kdtree(left_points, depth + 1),
        right=build_kdtree(right_points, depth + 1),
    )
