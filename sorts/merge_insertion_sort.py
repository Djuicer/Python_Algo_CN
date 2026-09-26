"""
归并插入排序（Merge-Insertion Sort）算法的纯 Python 实现
Source: https://en.wikipedia.org/wiki/Merge-insertion_sort

运行 doctest 请使用以下命令：
python3 -m doctest -v merge_insertion_sort.py
或
python -m doctest -v merge_insertion_sort.py

手动测试请运行：
python3 merge_insertion_sort.py
"""

from __future__ import annotations

from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def binary_search_insertion[T: Comparable](sorted_list: list[T], item: T) -> list[T]:
    """
    >>> binary_search_insertion([1, 2, 7, 9, 10], 4)
    [1, 2, 4, 7, 9, 10]
    """
    left = 0
    right = len(sorted_list) - 1
    while left <= right:
        middle = (left + right) // 2
        if left == right:
            if sorted_list[middle] < item:
                left = middle + 1
            break
        if sorted_list[middle] < item:
            left = middle + 1
        else:
            right = middle - 1
    sorted_list.insert(left, item)
    return sorted_list


def merge[T: Comparable](left: list[list[T]], right: list[list[T]]) -> list[list[T]]:
    """
    >>> merge([[1, 6], [9, 10]], [[2, 3], [4, 5], [7, 8]])
    [[1, 6], [2, 3], [4, 5], [7, 8], [9, 10]]
    """
    result = []
    while left and right:
        if left[0][0] < right[0][0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    return result + left + right


def sortlist_2d[T: Comparable](list_2d: list[list[T]]) -> list[list[T]]:
    """
    >>> sortlist_2d([[9, 10], [1, 6], [7, 8], [2, 3], [4, 5]])
    [[1, 6], [2, 3], [4, 5], [7, 8], [9, 10]]
    """
    length = len(list_2d)
    if length <= 1:
        return list_2d
    middle = length // 2
    return merge(sortlist_2d(list_2d[:middle]), sortlist_2d(list_2d[middle:]))


def merge_insertion_sort[T: Comparable](collection: list[T]) -> list[T]:
    """归并插入排序算法的纯 Python 实现

    :param collection: 可变有序集合，其中包含类型可不同但
    可相互比较的元素
    :return: 按升序排列后的同一个集合

    示例：
    >>> merge_insertion_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> merge_insertion_sort([99])
    [99]

    >>> merge_insertion_sort([-2, -5, -45])
    [-45, -5, -2]

    使用 range(0,5) 的所有排列进行测试：
    >>> import itertools
    >>> permutations = list(itertools.permutations([0, 1, 2, 3, 4]))
    >>> all(merge_insertion_sort(p) == [0, 1, 2, 3, 4] for p in permutations)
    True
    """

    if len(collection) <= 1:
        return collection

    """
    将元素两两分组；若元素数量为奇数，则留下最后一个元素。

    示例：[999, 100, 75, 40, 10000]
                -> [999, 100], [75, 40]。留下 10000。
    """
    two_paired_list = []
    has_last_odd_item = False
    for i in range(0, len(collection), 2):
        if i == len(collection) - 1:
            has_last_odd_item = True
        else:
            """
            对每组中的两个元素排序。

            示例：[999, 100], [75, 40]
                        -> [100, 999], [40, 75]
            """
            if collection[i] < collection[i + 1]:
                two_paired_list.append([collection[i], collection[i + 1]])
            else:
                two_paired_list.append([collection[i + 1], collection[i]])

    """
    对 two_paired_list 排序。

    示例：[100, 999], [40, 75]
                -> [40, 75], [100, 999]
    """
    sorted_list_2d = sortlist_2d(two_paired_list)

    """
    由于已经排序，可以确定 40 < 100。
    据此生成 sorted_list，以避免不必要的比较。

    示例：
           group0 group1
           40     100
           75     999
        ->
           group0 group1
           [40,   100]
           75     999
    """
    result = [i[0] for i in sorted_list_2d]

    """
    由于已经排序，可以确定 100 < 999。
    将 999 放到 sorted_list 末尾，以避免不必要的比较。

    示例：
           group0 group1
           [40,   100]
           75     999
        ->
           group0 group1
           [40,   100,   999]
           75
    """
    result.append(sorted_list_2d[-1][1])

    """
    若有因总数为奇数而留下的最后一个元素，则将其插入。

    示例：
           group0 group1
           [40,   100,   999]
           75
        ->
           group0 group1
           [40,   100,   999,   10000]
           75
    """
    if has_last_odd_item:
        pivot = collection[-1]
        result = binary_search_insertion(result, pivot)

    """
    插入剩余元素。
    此时由于已经排序，可以确定 40 < 75。
    因此，只需将 75 插入 [100, 999, 10000]，
    从而避免不必要的比较。

    示例：
           group0 group1
           [40,   100,   999,   10000]
            ^ 已确定 40 < 75，无需与此处比较。
           75
        ->
           [40,   75,    100,   999,   10000]
    """
    is_last_odd_item_inserted_before_this_index = False
    for i in range(len(sorted_list_2d) - 1):
        if result[i] == collection[-1] and has_last_odd_item:
            is_last_odd_item_inserted_before_this_index = True
        pivot = sorted_list_2d[i][1]
        # 若 last_odd_item 插入到该元素索引之前，
        # 则应将索引再向后移动一位。
        if is_last_odd_item_inserted_before_this_index:
            result = result[: i + 2] + binary_search_insertion(result[i + 2 :], pivot)
        else:
            result = result[: i + 1] + binary_search_insertion(result[i + 1 :], pivot)

    return result


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(merge_insertion_sort(unsorted))
