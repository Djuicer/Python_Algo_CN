#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11532
#  https://github.com/TheAlgorithms/Python/pull/11532
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

import numpy as np
import pytest

from data_structures.kd_tree.build_kdtree import build_kdtree
from data_structures.kd_tree.example.hypercube_points import hypercube_points
from data_structures.kd_tree.kd_node import KDNode
from data_structures.kd_tree.nearest_neighbour_search import nearest_neighbour_search


@pytest.mark.parametrize(
    ("num_points", "cube_size", "num_dimensions", "depth", "expected_result"),
    [
        (0, 10.0, 2, 0, None),  # 空 点 列表
        (10, 10.0, 2, 2, KDNode),  # 深度 = 2，2D 点
        (10, 10.0, 3, -2, KDNode),  # 深度 = -2，3D 点
    ],
)
def test_build_kdtree(
    num_points, cube_size, num_dimensions, depth, expected_result
) -> None:
    """
    测试 该 KD-树 是 built correctly。

    情况：
        - 空 点 列表。
        - 正 深度 值。
        - 负 深度 值。
    """
    points = (
        hypercube_points(num_points, cube_size, num_dimensions).tolist()
        if num_points > 0
        else []
    )

    kdtree = build_kdtree(points, depth=depth)

    if expected_result is None:
        # 空 点 列表 情况
        assert kdtree is None, f"Expected None for empty points list, got {kdtree}"
    else:
        # 检查是否 根节点 是 不 None
        assert kdtree is not None, "Expected a KDNode, got None"

        # 检查是否 根节点 具有 correct dimensions
        assert len(kdtree.point) == num_dimensions, (
            f"Expected point dimension {num_dimensions}, got {len(kdtree.point)}"
        )

        # 检查 该 该树 是 balanced 到 some extent (simplistic 检查)
        assert isinstance(kdtree, KDNode), (
            f"Expected KDNode instance, got {type(kdtree)}"
        )


def test_nearest_neighbour_search() -> None:
    """
    测试 最近 邻居 搜索 函数。
    """
    num_points = 10
    cube_size = 10.0
    num_dimensions = 2
    points = hypercube_points(num_points, cube_size, num_dimensions)
    kdtree = build_kdtree(points.tolist())

    rng = np.random.default_rng()
    query_point = rng.random(num_dimensions).tolist()

    nearest_point, nearest_dist, nodes_visited = nearest_neighbour_search(
        kdtree, query_point
    )

    # 检查 该 最近 点 是 不 None
    assert nearest_point is not None

    # 检查 该 距离 是 非-负 数
    assert nearest_dist >= 0

    # 检查 该 节点 visited 是 非-负 整数
    assert nodes_visited >= 0


def test_edge_cases() -> None:
    """
    测试 edge 情况 such 作为 空 KD-树。
    """
    empty_kdtree = build_kdtree([])
    query_point = [0.0] * 2  # 使用 default 2D 查询 点

    nearest_point, nearest_dist, nodes_visited = nearest_neighbour_search(
        empty_kdtree, query_point
    )

    # 带有 空 KD-树，nearest_point 应 为 None
    assert nearest_point is None
    assert nearest_dist == float("inf")
    assert nodes_visited == 0


if __name__ == "__main__":
    import pytest

    pytest.main()
