#!/usr/bin/env python3

"""
二分查找（Binary Search）算法的纯 Python 实现

运行 doctest 请使用以下命令：
python3 -m doctest -v binary_search.py

手动测试请运行：
python3 binary_search.py
"""

import bisect
from itertools import pairwise


def bisect_left(
    sorted_collection: list[int], item: int, lo: int = 0, hi: int = -1
) -> int:
    """
    在有序数组中定位第一个大于或等于
    给定值的元素。

    接口与以下函数相同：
    https://docs.python.org/3/library/bisect.html#bisect.bisect_left .

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 用于二分定位的元素
    :param lo: 搜索范围的起始索引（如 sorted_collection[lo:hi]）
    :param hi: 搜索范围的结束索引，不包含该位置（如 sorted_collection[lo:hi]）
    :return: 索引 i，使 sorted_collection[lo:i] 中所有值都 < item，且
        sorted_collection[i:hi] 中所有值都 >= item。

    示例：
    >>> bisect_left([0, 5, 7, 10, 15], 0)
    0
    >>> bisect_left([0, 5, 7, 10, 15], 6)
    2
    >>> bisect_left([0, 5, 7, 10, 15], 20)
    5
    >>> bisect_left([0, 5, 7, 10, 15], 15, 1, 3)
    3
    >>> bisect_left([0, 5, 7, 10, 15], 6, 2)
    2
    """
    if hi < 0:
        hi = len(sorted_collection)

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if sorted_collection[mid] < item:
            lo = mid + 1
        else:
            hi = mid

    return lo


def bisect_right(
    sorted_collection: list[int], item: int, lo: int = 0, hi: int = -1
) -> int:
    """
    在有序数组中定位第一个大于给定值的元素。

    接口与以下函数相同：
    https://docs.python.org/3/library/bisect.html#bisect.bisect_right .

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 用于二分定位的元素
    :param lo: 搜索范围的起始索引（如 sorted_collection[lo:hi]）
    :param hi: 搜索范围的结束索引，不包含该位置（如 sorted_collection[lo:hi]）
    :return: 索引 i，使 sorted_collection[lo:i] 中所有值都 <= item，且
        sorted_collection[i:hi] 中所有值都 > item。

    示例：
    >>> bisect_right([0, 5, 7, 10, 15], 0)
    1
    >>> bisect_right([0, 5, 7, 10, 15], 15)
    5
    >>> bisect_right([0, 5, 7, 10, 15], 6)
    2
    >>> bisect_right([0, 5, 7, 10, 15], 15, 1, 3)
    3
    >>> bisect_right([0, 5, 7, 10, 15], 6, 2)
    2
    """
    if hi < 0:
        hi = len(sorted_collection)

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if sorted_collection[mid] <= item:
            lo = mid + 1
        else:
            hi = mid

    return lo


def insort_left(
    sorted_collection: list[int], item: int, lo: int = 0, hi: int = -1
) -> None:
    """
    将给定值插入有序数组，置于所有相等元素之前。

    接口与以下函数相同：
    https://docs.python.org/3/library/bisect.html#bisect.insort_left .

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 待插入的元素
    :param lo: 搜索范围的起始索引（如 sorted_collection[lo:hi]）
    :param hi: 搜索范围的结束索引，不包含该位置（如 sorted_collection[lo:hi]）

    示例：
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_left(sorted_collection, 6)
    >>> sorted_collection
    [0, 5, 6, 7, 10, 15]
    >>> sorted_collection = [(0, 0), (5, 5), (7, 7), (10, 10), (15, 15)]
    >>> item = (5, 5)
    >>> insort_left(sorted_collection, item)
    >>> sorted_collection
    [(0, 0), (5, 5), (5, 5), (7, 7), (10, 10), (15, 15)]
    >>> item is sorted_collection[1]
    True
    >>> item is sorted_collection[2]
    False
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_left(sorted_collection, 20)
    >>> sorted_collection
    [0, 5, 7, 10, 15, 20]
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_left(sorted_collection, 15, 1, 3)
    >>> sorted_collection
    [0, 5, 7, 15, 10, 15]
    """
    sorted_collection.insert(bisect_left(sorted_collection, item, lo, hi), item)


def insort_right(
    sorted_collection: list[int], item: int, lo: int = 0, hi: int = -1
) -> None:
    """
    将给定值插入有序数组，置于所有相等元素之后。

    接口与以下函数相同：
    https://docs.python.org/3/library/bisect.html#bisect.insort_right .

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 待插入的元素
    :param lo: 搜索范围的起始索引（如 sorted_collection[lo:hi]）
    :param hi: 搜索范围的结束索引，不包含该位置（如 sorted_collection[lo:hi]）

    示例：
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_right(sorted_collection, 6)
    >>> sorted_collection
    [0, 5, 6, 7, 10, 15]
    >>> sorted_collection = [(0, 0), (5, 5), (7, 7), (10, 10), (15, 15)]
    >>> item = (5, 5)
    >>> insort_right(sorted_collection, item)
    >>> sorted_collection
    [(0, 0), (5, 5), (5, 5), (7, 7), (10, 10), (15, 15)]
    >>> item is sorted_collection[1]
    False
    >>> item is sorted_collection[2]
    True
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_right(sorted_collection, 20)
    >>> sorted_collection
    [0, 5, 7, 10, 15, 20]
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_right(sorted_collection, 15, 1, 3)
    >>> sorted_collection
    [0, 5, 7, 15, 10, 15]
    """
    sorted_collection.insert(bisect_right(sorted_collection, item, lo, hi), item)


def binary_search(sorted_collection: list[int], item: int) -> int:
    """二分查找算法的纯 Python 实现

    注意，集合必须按升序排列，否则结果
    不可预测。

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 待查找的元素值
    :return: 找到的元素索引；未找到则返回 -1。
             如果元素出现多次，则返回
             最左侧出现位置的索引。

    示例：
    >>> binary_search([0, 5, 7, 10, 15], 0)
    0
    >>> binary_search([0, 5, 7, 10, 15], 15)
    4
    >>> binary_search([0, 5, 7, 10, 15], 5)
    1
    >>> binary_search([0, 5, 7, 10, 15], 6)
    -1
    >>> binary_search([1, 2, 4, 4, 4, 6, 7], 4)
    2
    >>> binary_search([0, 5, 7, 10, 10, 10], 10)
    3
    """
    if any(a > b for a, b in pairwise(sorted_collection)):
        raise ValueError("sorted_collection must be sorted in ascending order")
    left = 0
    right = len(sorted_collection) - 1
    result = -1

    while left <= right:
        midpoint = left + (right - left) // 2
        current_item = sorted_collection[midpoint]
        if current_item == item:
            result = (
                midpoint  # 已找到元素，但继续查找最左侧的出现位置
            )
            right = midpoint - 1  # 在左侧查找其他出现位置
        elif item < current_item:
            right = midpoint - 1
        else:
            left = midpoint + 1
    return result


def binary_search_std_lib(sorted_collection: list[int], item: int) -> int:
    """使用标准库的二分查找算法纯 Python 实现

    注意，集合必须按升序排列，否则结果
    不可预测。

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 待查找的元素值
    :return: 找到的元素索引；未找到则返回 -1

    示例：
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 0)
    0
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 15)
    4
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 5)
    1
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 6)
    -1
    """
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")
    index = bisect.bisect_left(sorted_collection, item)
    if index != len(sorted_collection) and sorted_collection[index] == item:
        return index
    return -1


def binary_search_with_duplicates(sorted_collection: list[int], item: int) -> list[int]:
    """支持重复元素的二分查找算法
    纯 Python 实现。

    参考资料：
    https://stackoverflow.com/questions/13197552/using-binary-search-with-sorted-array-with-duplicates

    集合必须按升序排列，否则结果
    不可预测。如果目标元素出现多次，该函数返回
    所有出现位置的索引列表。如果未找到目标元素，
    则返回空列表。

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 待查找的元素值
    :return: 元素出现位置的索引列表（未找到则返回空列表）

    示例：
    >>> binary_search_with_duplicates([0, 5, 7, 10, 15], 0)
    [0]
    >>> binary_search_with_duplicates([0, 5, 7, 10, 15], 15)
    [4]
    >>> binary_search_with_duplicates([1, 2, 2, 2, 3], 2)
    [1, 2, 3]
    >>> binary_search_with_duplicates([1, 2, 2, 2, 3], 4)
    []
    """
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")

    def lower_bound(sorted_collection: list[int], item: int) -> int:
        """
        返回第一个大于或等于目标元素的元素索引。

        :param sorted_collection: 待搜索的有序列表。
        :param item: 待查找下界的元素。
        :return: 在保持有序的前提下可插入该元素的索引。
        """
        left = 0
        right = len(sorted_collection)
        while left < right:
            midpoint = left + (right - left) // 2
            current_item = sorted_collection[midpoint]
            if current_item < item:
                left = midpoint + 1
            else:
                right = midpoint
        return left

    def upper_bound(sorted_collection: list[int], item: int) -> int:
        """
        返回第一个严格大于目标元素的元素索引。

        :param sorted_collection: 待搜索的有序列表。
        :param item: 待查找上界的元素。
        :return: 可在所有相等元素之后插入该元素的索引。
        """
        left = 0
        right = len(sorted_collection)
        while left < right:
            midpoint = left + (right - left) // 2
            current_item = sorted_collection[midpoint]
            if current_item <= item:
                left = midpoint + 1
            else:
                right = midpoint
        return left

    left = lower_bound(sorted_collection, item)
    right = upper_bound(sorted_collection, item)

    if left == len(sorted_collection) or sorted_collection[left] != item:
        return []
    return list(range(left, right))


def binary_search_by_recursion(
    sorted_collection: list[int], item: int, left: int = 0, right: int = -1
) -> int:
    """二分查找算法的纯 Python 递归实现

    注意，集合必须按升序排列，否则结果
    不可预测。
    首次递归调用应设置 left=0 和 right=(len(sorted_collection)-1)

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 待查找的元素值
    :return: 找到的元素索引；未找到则返回 -1。
             如果元素出现多次，则返回
             最左侧出现位置的索引。

    示例：
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 0, 0, 4)
    0
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 15, 0, 4)
    4
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 5, 0, 4)
    1
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 6, 0, 4)
    -1
    >>> binary_search_by_recursion([1, 2, 4, 4, 4, 6, 7], 4, 0, 6)
    2
    >>> binary_search_by_recursion([0, 5, 7, 10, 10, 10], 10, 0, 5)
    3
    """
    if right < 0:
        right = len(sorted_collection) - 1
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")

    # 二分查找的辅助函数
    def _binary_search_recursive(left_idx: int, right_idx: int) -> int:
        if right_idx < left_idx:
            return -1

        midpoint = left_idx + (right_idx - left_idx) // 2
        current_item = sorted_collection[midpoint]

        if current_item == item:
            # 已找到元素，接下来查找最左侧的出现位置
            # 先递归查找左侧是否还有该元素
            leftmost = _binary_search_recursive(left_idx, midpoint - 1)
            return leftmost if leftmost != -1 else midpoint
        elif item < current_item:
            return _binary_search_recursive(left_idx, midpoint - 1)
        else:
            return _binary_search_recursive(midpoint + 1, right_idx)

    return _binary_search_recursive(left, right)


def exponential_search(sorted_collection: list[int], item: int) -> int:
    """指数查找（Exponential Search）算法的纯 Python 实现
    参考资料：
    https://en.wikipedia.org/wiki/Exponential_search

    注意，集合必须按升序排列，否则结果
    不可预测。

    :param sorted_collection: 元素可比较且按升序排列的集合
    :param item: 待查找的元素值
    :return: 找到的元素索引；未找到则返回 -1

    该算法的时间复杂度为 O(lg I)，其中 I 为目标元素存在时的索引位置

    示例：
    >>> exponential_search([0, 5, 7, 10, 15], 0)
    0
    >>> exponential_search([0, 5, 7, 10, 15], 15)
    4
    >>> exponential_search([0, 5, 7, 10, 15], 5)
    1
    >>> exponential_search([0, 5, 7, 10, 15], 6)
    -1
    """
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")
    bound = 1
    while bound < len(sorted_collection) and sorted_collection[bound] < item:
        bound *= 2
    left = bound // 2
    right = min(bound, len(sorted_collection) - 1)
    last_result = binary_search_by_recursion(
        sorted_collection=sorted_collection, item=item, left=left, right=right
    )
    if last_result is None:
        return -1
    return last_result


searches = (  # 从最快到最慢……
    binary_search_std_lib,
    binary_search,
    exponential_search,
    binary_search_by_recursion,
)


if __name__ == "__main__":
    import doctest
    import timeit

    doctest.testmod()
    for search in searches:
        name = f"{search.__name__:>26}"
        print(f"{name}: {search([0, 5, 7, 10, 15], 10) = }")  # type: ignore[operator]

    print("\nBenchmarks...")
    setup = "collection = range(1000)"
    for search in searches:
        name = search.__name__
        print(
            f"{name:>26}:",
            timeit.timeit(
                f"{name}(collection, 500)", setup=setup, number=5_000, globals=globals()
            ),
        )

    user_input = input("\nEnter numbers separated by comma: ").strip()
    collection = sorted(int(item) for item in user_input.split(","))
    target = int(input("Enter a single number to be found in the list: "))
    result = binary_search(sorted_collection=collection, item=target)
    if result == -1:
        print(f"{target} was not found in {collection}.")
    else:
        print(f"{target} was found at position {result} of {collection}.")
