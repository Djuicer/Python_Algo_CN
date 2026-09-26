"""
反转选择排序（Reverse Selection Sort）算法的纯 Python 实现

通过反转子数组，逐步完成数组排序

运行 doctest 请使用以下命令：
python3 -m doctest -v reverse_selection.py

手动测试请运行：
python3 reverse_selection.py
"""

from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def reverse_subarray[T](arr: list[T], start: int, end: int) -> None:
    """
    原地反转子数组。

    :param arr: 包含待反转子数组的数组
    :param start: 子数组的起始索引
    :param end: 子数组的结束索引

    示例：
    >>> lst = [1, 2, 3, 4, 5]
    >>> reverse_subarray(lst, 1, 3)
    >>> lst
    [1, 4, 3, 2, 5]

    >>> lst = [1]
    >>> reverse_subarray(lst, 0, 0)
    >>> lst
    [1]

    >>> lst = [1, 2]
    >>> reverse_subarray(lst, 0, 1)
    >>> lst
    [2, 1]
    """
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1


def reverse_selection_sort[T: Comparable](collection: list[T]) -> list[T]:
    """
    反转选择排序算法的纯 Python 实现

    :param collection: 可变有序集合，其中包含类型可不同但
    可相互比较的元素
    :return: 按升序排列后的同一个集合

    示例：
    >>> reverse_selection_sort([1, 9, 5, 21, 17, 6])
    [1, 5, 6, 9, 17, 21]

    >>> reverse_selection_sort([])
    []

    >>> reverse_selection_sort([-3, -17, -48])
    [-48, -17, -3]

    >>> reverse_selection_sort([1, 1, 1, 1])
    [1, 1, 1, 1]

    >>> reverse_selection_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]

    >>> reverse_selection_sort(["banana", "apple", "cherry"])
    ['apple', 'banana', 'cherry']

    >>> reverse_selection_sort([3.14, 1.5, 2.7])
    [1.5, 2.7, 3.14]

    >>> reverse_selection_sort([1, "a"])  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...
    """
    n = len(collection)
    for i in range(n - 1):
        # 查找未排序部分的最小元素
        min_idx = i
        for j in range(i + 1, n):
            if collection[j] < collection[min_idx]:
                min_idx = j

        # 若最小元素不在未排序部分的开头，
        # 则反转子数组，将其移到前端
        if min_idx != i:
            reverse_subarray(collection, i, min_idx)

    return collection


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(reverse_selection_sort(unsorted))
