"""
活动选择问题（Activity Selection Problem）是一个经典问题：给定一组活动，
每项活动都有开始和结束时间，需要合理安排，
使选出的互不重叠的活动数量最多。
这里采用贪心算法（Greedy Algorithm），每一步都
选择结束时间最早、
且不与已选活动冲突的活动。

Wikipedia: https://en.wikipedia.org/wiki/Activity_selection_problem
"""


def activity_selection(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    使用贪心算法求解活动选择问题，从活动列表中
    选出数量最多的互不重叠的活动。

    Parameters:
    activities: 元组列表，每个元组包含
                                        一项活动的开始和结束时间。

    Returns:
    互不重叠的已选活动列表。

    示例：
    >>> activity_selection([(1, 3), (2, 5), (3, 9), (6, 8)])
    [(1, 3), (6, 8)]

    >>> activity_selection([(0, 6), (1, 4), (3, 5), (5, 7), (5, 9), (8, 9)])
    [(1, 4), (5, 7), (8, 9)]

    >>> activity_selection([(1, 2), (2, 4), (3, 5), (0, 6)])
    [(1, 2), (2, 4)]

    >>> activity_selection([(5, 9), (1, 2), (3, 4), (0, 6)])
    [(1, 2), (3, 4), (5, 9)]

    >>> all(activity_selection(x) == [] for x in ([], {}, None, False, 0, 0.0))
    True
    """
    if not activities:
        return []

    # 第 1 步：按结束时间对活动排序
    sorted_activities = sorted(activities, key=lambda activity: activity[1])

    # 第 2 步：选择第一项活动（结束最早的活动）
    # 作为初始活动
    selected_activities = [sorted_activities[0]]

    # 第 3 步：遍历排序后的活动，选出
    # 与上一次选择的活动不重叠的活动
    for i in range(1, len(sorted_activities)):
        if sorted_activities[i][0] >= selected_activities[-1][1]:
            selected_activities.append(sorted_activities[i])

    return selected_activities
