"""
中位数的中位数（Median of Medians）算法的 Python 实现，
用于为 quick_select 选择枢轴，能够高效地
求出列表排序后某个索引处应有的值，
即使输入列表尚未
排序。对于任意秩，都能以 O(n) 的时间复杂度
进行确定性查找。
https://en.wikipedia.org/wiki/Median_of_medians
"""


def median_of_five(arr: list) -> int:
    """
    返回输入列表的中位数
    :param arr: 待求中位数的数组
    :return: arr 的中位数

    >>> median_of_five([2, 4, 5, 7, 899])
    5
    >>> median_of_five([5, 7, 899, 54, 32])
    32
    >>> median_of_five([5, 4, 3, 2])
    4
    >>> median_of_five([3, 5, 7, 10, 2])
    5
    """
    arr = sorted(arr)
    return arr[len(arr) // 2]


def median_of_medians(arr: list) -> int:
    """
    通过计算输入数据的中位数的中位数，
    返回用于划分数据的枢轴
    :param arr: 待处理的数据（列表）
    :return: 输入数组的中位数的中位数

    >>> median_of_medians([2, 4, 5, 7, 899, 54, 32])
    54
    >>> median_of_medians([5, 7, 899, 54, 32])
    32
    >>> median_of_medians([5, 4, 3, 2])
    4
    >>> median_of_medians([3, 5, 7, 10, 2, 12])
    12
    """

    if len(arr) <= 5:
        return median_of_five(arr)
    medians = []
    i = 0
    while i < len(arr):
        if (i + 4) <= len(arr):
            medians.append(median_of_five(arr[i:].copy()))
        else:
            medians.append(median_of_five(arr[i : i + 5].copy()))
        i += 5
    return median_of_medians(medians)


def quick_select(arr: list, target: int) -> int:
    """
    根据数据与枢轴的大小关系，
    将其划分为较小和较大的两个列表
    :param arr: 待搜索的数据（列表）
    :param target: 待查找的秩
    :return: 秩为 target 的元素

    >>> quick_select([2, 4, 5, 7, 899, 54, 32], 5)
    32
    >>> quick_select([2, 4, 5, 7, 899, 54, 32], 1)
    2
    >>> quick_select([5, 4, 3, 2], 2)
    3
    >>> quick_select([3, 5, 7, 10, 2, 12], 3)
    5
    """

    # 无效输入
    if target > len(arr):
        return -1

    # x 是通过中位数的中位数算法估算的枢轴
    x = median_of_medians(arr)
    left = []
    right = []
    check = False
    for i in range(len(arr)):
        if arr[i] < x:
            left.append(arr[i])
        elif arr[i] > x:
            right.append(arr[i])
        elif arr[i] == x and not check:
            check = True
        else:
            right.append(arr[i])
    rank_x = len(left) + 1
    if rank_x == target:
        answer = x
    elif rank_x > target:
        answer = quick_select(left, target)
    elif rank_x < target:
        answer = quick_select(right, target - rank_x)
    return answer


print(median_of_five([5, 4, 3, 2]))
