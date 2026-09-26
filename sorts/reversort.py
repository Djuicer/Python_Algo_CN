"""
Reversort 是 Google Code Jam 2021 资格赛中描述的一种排序算法。

算法：
1. i 从 1 遍历到 N-1：
   a. 找出位置 i 到 N 的子数组中最小元素的位置 j
   b. 反转位置 i 到 j 的子数组

时间复杂度：O(n²)，每个位置都需查找最小值并反转
空间复杂度：O(n)，由 Python 列表切片产生
                  （使用原地反转可降至 O(1)）

运行 doctest 请使用以下命令：
python3 -m doctest -v reversort.py

手动测试请运行：
python reversort.py
"""

from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def reversort[T: Comparable](collection: list[T]) -> list[T]:
    """
    使用 Reversort 算法对列表排序。

    反复寻找未排序部分中的最小元素，
    并反转从当前位置到最小元素
    所在位置的子数组。

    :param collection: 元素可比较的可变有序集合
    :return: 按升序排列的集合

    示例：
    >>> reversort([4, 2, 1, 3])
    [1, 2, 3, 4]
    >>> reversort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> reversort([])
    []
    >>> reversort([-2, -5, -45])
    [-45, -5, -2]
    >>> reversort([1])
    [1]
    >>> reversort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> reversort([2, 1, 4, 3])
    [1, 2, 3, 4]
    >>> reversort([-23, 0, 6, -4, 34])
    [-23, -4, 0, 6, 34]
    >>> reversort([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> reversort([3, 3, 3, 3])
    [3, 3, 3, 3]
    >>> reversort([56])
    [56]
    >>> reversort([0, 5, 2, 3, 2]) == sorted([0, 5, 2, 3, 2])
    True
    >>> reversort([]) == sorted([])
    True
    >>> reversort([-2, -45, -5]) == sorted([-2, -45, -5])
    True
    >>> reversort([-23, 0, 6, -4, 34]) == sorted([-23, 0, 6, -4, 34])
    True
    >>> reversort(['d', 'a', 'b', 'e']) == sorted(['d', 'a', 'b', 'e'])
    True
    >>> reversort(['z', 'a', 'y', 'b', 'x', 'c'])
    ['a', 'b', 'c', 'x', 'y', 'z']
    >>> reversort([1.1, 3.3, 5.5, 7.7, 2.2, 4.4, 6.6])
    [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
    >>> reversort([1, 3.3, 5, 7.7, 2, 4.4, 6])
    [1, 2, 3.3, 4.4, 5, 6, 7.7]
    >>> import random
    >>> collection_arg = random.sample(range(-50, 50), 100)
    >>> reversort(collection_arg) == sorted(collection_arg)
    True
    >>> import string
    >>> collection_arg = random.choices(string.ascii_letters + string.digits, k=100)
    >>> reversort(collection_arg) == sorted(collection_arg)
    True
    >>> reversort([1, "a"])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    arr = collection[:]  # 创建副本，避免修改原始输入
    n = len(arr)

    for i in range(n - 1):
        # 查找 arr[i:] 中最小元素的位置
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        # 反转位置 i 到 min_index 的子数组
        if min_index != i:
            arr[i : min_index + 1] = arr[i : min_index + 1][::-1]

    return arr


def reversort_cost[T: Comparable](collection: list[T]) -> int:
    """
    计算使用 Reversort 排序的代价。

    代价定义为所有反转片段的长度之和。
    此定义来自 Google Code Jam 2021 的题目。

    :param collection: 元素可比较的可变有序集合
    :return: 排序的总代价

    示例：
    >>> reversort_cost([4, 2, 1, 3])
    6
    >>> reversort_cost([1, 2])
    1
    >>> reversort_cost([7, 6, 5, 4, 3, 2, 1])
    12
    >>> reversort_cost([1, 2, 3, 4])
    3
    >>> reversort_cost([1])
    0
    >>> reversort_cost([])
    0
    >>> reversort_cost([1, "a"])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    arr = collection[:]  # 创建副本，避免修改原始输入
    n = len(arr)
    total_cost = 0

    for i in range(n - 1):
        # 查找 arr[i:] 中最小元素的位置
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        # 反转位置 i 到 min_index 的子数组
        arr[i : min_index + 1] = arr[i : min_index + 1][::-1]

        # 代价为反转片段的长度
        total_cost += min_index - i + 1

    return total_cost


if __name__ == "__main__":
    import doctest
    from random import sample
    from timeit import timeit

    doctest.testmod()

    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(f"Sorted list: {reversort(unsorted)}")
    print(f"Sort cost: {reversort_cost(unsorted)}")

    # 基准测试
    num_runs = 1000
    test_arr = sample(range(-50, 50), 100)
    timer = timeit("reversort(test_arr[:])", globals=globals(), number=num_runs)
    print(f"\nProcessing time: {timer:.5f}s for {num_runs:,} runs on 100 elements")
