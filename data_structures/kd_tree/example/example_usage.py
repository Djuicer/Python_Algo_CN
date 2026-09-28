#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11532
#  https://github.com/TheAlgorithms/Python/pull/11532
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

import numpy as np

from data_structures.kd_tree.build_kdtree import build_kdtree
from data_structures.kd_tree.example.hypercube_points import hypercube_points
from data_structures.kd_tree.nearest_neighbour_search import nearest_neighbour_search


def main() -> None:
    """
    Demonstrates 使用 的 KD-树 通过 building 它 从 随机 点
    在 10-dimensional hypercube 并且 performing 最近 邻居 搜索。
    """
    num_points: int = 5000
    cube_size: float = 10.0  # 大小 的 hypercube (edge 长度)
    num_dimensions: int = 10

    # 生成 随机 点 之内 hypercube
    points: np.ndarray = hypercube_points(num_points, cube_size, num_dimensions)
    hypercube_kdtree = build_kdtree(points.tolist())

    # 生成 随机 查询 点 之内 相同 空间
    rng = np.random.default_rng()
    query_point: list[float] = rng.random(num_dimensions).tolist()

    # 执行 最近 邻居 搜索
    nearest_point, nearest_dist, nodes_visited = nearest_neighbour_search(
        hypercube_kdtree, query_point
    )

    # 打印 results
    print(f"Query point: {query_point}")
    print(f"Nearest point: {nearest_point}")
    print(f"Distance: {nearest_dist:.4f}")
    print(f"Nodes visited: {nodes_visited}")


if __name__ == "__main__":
    main()
