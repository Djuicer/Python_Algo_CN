"""
DBSCAN（具有噪声的基于密度的聚类）

一种基于密度的聚类算法，将紧密分布的点归为一组，并将低密度区域中的点
标记为离群点。

与 K-Means 不同，DBSCAN：
- 无需预先指定簇的数量
- 可以发现任意形状的簇
- 对离群点具有鲁棒性（将其标记为噪声，cluster id = -1）

关键参数：
    epsilon (eps)：两个点被视为邻居的最大距离
    min_points：形成稠密区域（核心点）所需的最少点数

点的类型：
    - 核心点：在 `epsilon` 距离内至少有 `min_points` 个邻居
    - 边界点：位于核心点的 `epsilon` 范围内，但邻居少于 `min_points` 个
    - 噪声点：既不是核心点也不是边界点，标记为 -1

时间复杂度：使用暴力邻居搜索时为 O(n²)
空间复杂度：O(n)

References:
    - https://en.wikipedia.org/wiki/DBSCAN
    - Ester, M., et al. "A density-based algorithm for discovering clusters."
      KDD 1996. https://dl.acm.org/doi/10.5555/3001460.3001507
"""


def euclidean_distance(point_a: list[float], point_b: list[float]) -> float:
    """
    计算 n 维空间中两点之间的欧几里得距离。

    >>> euclidean_distance([0.0, 0.0], [3.0, 4.0])
    5.0
    >>> euclidean_distance([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    0.0
    >>> euclidean_distance([0.0], [5.0])
    5.0
    >>> euclidean_distance([0.0, 0.0], [1.0])
    Traceback (most recent call last):
        ...
    ValueError: Both points must have the same number of dimensions.
    """
    if len(point_a) != len(point_b):
        raise ValueError("Both points must have the same number of dimensions.")
    return sum((a - b) ** 2 for a, b in zip(point_a, point_b)) ** 0.5


def get_neighbors(
    data: list[list[float]], point_index: int, epsilon: float
) -> list[int]:
    """
    返回与 data[point_index] 的距离不超过 epsilon 的所有点的索引。

    >>> data = [[0.0, 0.0], [0.1, 0.1], [5.0, 5.0]]
    >>> get_neighbors(data, 0, 0.5)
    [0, 1]
    >>> get_neighbors(data, 2, 0.5)
    [2]
    >>> get_neighbors(data, 0, 10.0)
    [0, 1, 2]
    """
    return [
        index
        for index, point in enumerate(data)
        if euclidean_distance(data[point_index], point) <= epsilon
    ]


def dbscan(
    data: list[list[float]],
    epsilon: float,
    min_points: int,
) -> list[int]:
    """
    对数据集执行 DBSCAN 聚类。

    参数：
        data：n 维数据点列表，例如 [[x1,y1], [x2,y2], ...]
        epsilon：两个点被视为邻居的最大距离，必须大于 0。
        min_points：成为核心点所需的最少邻居数（包括自身），必须至少为 1。

    返回：
        整数簇标签列表，每个输入点对应一个标签。
        噪声点标记为 -1，簇 ID 从 0 开始。

    异常：
        ValueError：如果 data 为空。
        ValueError：如果 epsilon 不是正数。
        ValueError：如果 min_points 小于 1。

    示例——两个明显分离的簇：
    >>> data = [
    ...     [1.0, 1.0], [1.1, 1.0], [1.0, 1.1],
    ...     [9.0, 9.0], [9.1, 9.0], [9.0, 9.1],
    ... ]
    >>> labels = dbscan(data, epsilon=0.5, min_points=2)
    >>> len(set(labels))  # two clusters
    2
    >>> labels[0] == labels[1] == labels[2]  # first three in same cluster
    True
    >>> labels[3] == labels[4] == labels[5]  # last three in same cluster
    True
    >>> labels[0] != labels[3]               # different clusters
    True

    Example — isolated noise point:
    >>> data = [[0.0, 0.0], [0.1, 0.0], [0.0, 0.1], [99.0, 99.0]]
    >>> labels = dbscan(data, epsilon=0.5, min_points=2)
    >>> labels[3]  # noise
    -1
    >>> labels[0] == labels[1] == labels[2]  # one cluster
    True

    Example — all points are noise (min_points too high):
    >>> data = [[0.0, 0.0], [5.0, 5.0]]
    >>> dbscan(data, epsilon=0.3, min_points=5)
    [-1, -1]

    Example — single cluster (all points close together):
    >>> data = [[0.0, 0.0], [0.1, 0.0], [0.0, 0.1], [0.1, 0.1]]
    >>> labels = dbscan(data, epsilon=0.5, min_points=2)
    >>> len(set(labels))
    1
    >>> -1 not in labels
    True

    Example — invalid inputs:
    >>> dbscan([], epsilon=0.5, min_points=2)
    Traceback (most recent call last):
        ...
    ValueError: Data must not be empty.
    >>> dbscan([[1.0, 2.0]], epsilon=0.0, min_points=2)
    Traceback (most recent call last):
        ...
    ValueError: Epsilon must be greater than 0.
    >>> dbscan([[1.0, 2.0]], epsilon=0.5, min_points=0)
    Traceback (most recent call last):
        ...
    ValueError: min_points must be at least 1.
    """
    if not data:
        raise ValueError("Data must not be empty.")
    if epsilon <= 0:
        raise ValueError("Epsilon must be greater than 0.")
    if min_points < 1:
        raise ValueError("min_points must be at least 1.")

    labels = [-1] * len(data)  # all points start as noise
    current_cluster_id = 0

    for point_index in range(len(data)):
        if labels[point_index] != -1:
            continue  # already assigned

        neighbors = get_neighbors(data, point_index, epsilon)

        if len(neighbors) < min_points:
            continue  # not a core point — remains noise for now

        # point_index is a core point — start a new cluster
        labels[point_index] = current_cluster_id
        seeds = [n for n in neighbors if n != point_index]

        while seeds:
            current_point = seeds.pop()

            # skip points already claimed by a different cluster
            if (
                labels[current_point] != -1
                and labels[current_point] != current_cluster_id
            ):
                continue

            # assign noise points and unvisited points to this cluster
            labels[current_point] = current_cluster_id
            current_neighbors = get_neighbors(data, current_point, epsilon)

            if len(current_neighbors) >= min_points:
                # current_point is also a core point — expand cluster
                for neighbor in current_neighbors:
                    if labels[neighbor] == -1:
                        seeds.append(neighbor)

        current_cluster_id += 1

    return labels


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
