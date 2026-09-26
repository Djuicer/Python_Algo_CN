"""
该算法在给定的 n 个点中，求出
最近点对之间的距离。
采用的方法 -> 分治（Divide and Conquer）
分别按 X 坐标和
Y 坐标对点排序。
然后应用分治策略，
递归求出最小距离。

>> 最近点对可能位于分割线的两侧。
为处理这种情况，构造一个点带，
其中各点的 X 坐标与中点 X 坐标之差
小于 closest_pair_dis。此步骤使用已按 Y 坐标排序的点，
以减少排序时间。
在点带内求最近点对距离。（closest_in_strip）

min(closest_pair_dis, closest_in_strip) 即为最终结果。

时间复杂度：O(n * log n)
"""


def euclidean_distance_sqr(point1, point2):
    """
    >>> euclidean_distance_sqr([1,2],[2,4])
    5
    """
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2


def column_based_sort(array, column=0):
    """
    >>> column_based_sort([(5, 1), (4, 2), (3, 0)], 1)
    [(3, 0), (5, 1), (4, 2)]
    """
    return sorted(array, key=lambda x: x[column])


def dis_between_closest_pair(points, points_counts, min_dis=float("inf")):
    """
    使用暴力法求最近点对距离

    参数：
    points, points_count, min_dis (list(tuple(int, int)), int, int)

    返回：
    min_dis (float): 最近点对之间的距离

    >>> dis_between_closest_pair([[1,2],[2,4],[5,7],[8,9],[11,0]],5)
    5

    """

    for i in range(points_counts - 1):
        for j in range(i + 1, points_counts):
            current_dis = euclidean_distance_sqr(points[i], points[j])
            min_dis = min(min_dis, current_dis)
    return min_dis


def dis_between_closest_in_strip(points, points_counts, min_dis=float("inf")):
    """
    求点带内的最近点对

    参数：
    points, points_count, min_dis (list(tuple(int, int)), int, int)

    返回：
    min_dis (float): 点带内最近点对之间的距离（< min_dis）

    >>> dis_between_closest_in_strip([[1,2],[2,4],[5,7],[8,9],[11,0]],5)
    85
    """

    for i in range(min(6, points_counts - 1), points_counts):
        for j in range(max(0, i - 6), i):
            current_dis = euclidean_distance_sqr(points[i], points[j])
            min_dis = min(min_dis, current_dis)
    return min_dis


def closest_pair_of_points_sqr(points_sorted_on_x, points_sorted_on_y, points_counts):
    """分治方法

    参数：
    points, points_count (list(tuple(int, int)), int)

    返回：
    (float): 最近点对之间的距离

    >>> closest_pair_of_points_sqr([(1, 2), (3, 4)], [(5, 6), (7, 8)], 2)
    8
    """

    # 递归终止条件
    if points_counts <= 3:
        return dis_between_closest_pair(points_sorted_on_x, points_counts)

    # 递归
    mid = points_counts // 2
    closest_in_left = closest_pair_of_points_sqr(
        points_sorted_on_x, points_sorted_on_y[:mid], mid
    )
    closest_in_right = closest_pair_of_points_sqr(
        points_sorted_on_y, points_sorted_on_y[mid:], points_counts - mid
    )
    closest_pair_dis = min(closest_in_left, closest_in_right)

    """
    cross_strip 包含 X 坐标与 mid 的 X 坐标之间
    距离小于 closest_pair_dis 的点
    """

    cross_strip = []
    for point in points_sorted_on_x:
        if abs(point[0] - points_sorted_on_x[mid][0]) < closest_pair_dis:
            cross_strip.append(point)

    closest_in_strip = dis_between_closest_in_strip(
        cross_strip, len(cross_strip), closest_pair_dis
    )
    return min(closest_pair_dis, closest_in_strip)


def closest_pair_of_points(points, points_counts):
    """
    >>> closest_pair_of_points([(2, 3), (12, 30)], len([(2, 3), (12, 30)]))
    28.792360097775937
    """
    points_sorted_on_x = column_based_sort(points, column=0)
    points_sorted_on_y = column_based_sort(points, column=1)
    return (
        closest_pair_of_points_sqr(
            points_sorted_on_x, points_sorted_on_y, points_counts
        )
    ) ** 0.5


if __name__ == "__main__":
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print("Distance:", closest_pair_of_points(points, len(points)))
