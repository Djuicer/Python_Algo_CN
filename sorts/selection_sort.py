from collections.abc import MutableSequence
from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def selection_sort[T: Comparable](collection: MutableSequence[T]) -> MutableSequence[T]:
    """
    使用选择排序（Selection Sort）算法将列表按升序排列。

    选择排序将输入列表划分为已排序区和未排序区，
    反复查找未排序区中的最小元素，
    将其放到已排序区末尾。

    时间复杂度：所有情况均为 O(n²)
    空间复杂度：O(1)

    :param collection: 待排序的可变序列，元素可比较。
    :return: 按升序排列后的同一个序列。


    时间复杂度：O(n^2)，由嵌套循环决定，其中 n 为集合
        长度。外层循环执行 n-1 次，内层循环每轮
        执行 n-i-1 次。
    空间复杂度：O(1)，仅为变量
        （length、i、min_index、k）使用常数大小的额外空间。
    示例：
    >>> selection_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> selection_sort([])
    []

    >>> selection_sort([-2, -5, -45])
    [-45, -5, -2]

    >>> selection_sort([1])
    [1]

    >>> selection_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]

    >>> selection_sort([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]

    >>> selection_sort([3, 3, 3, 3])
    [3, 3, 3, 3]

    >>> selection_sort([0])
    [0]

    >>> selection_sort([2, -3, 0, 5, -1])
    [-3, -1, 0, 2, 5]

    >>> selection_sort([0, 5, 3, 2, 2]) == sorted([0, 5, 3, 2, 2])
    True

    >>> selection_sort([-2, -5, -45]) == sorted([-2, -5, -45])
    True

    >>> selection_sort(["d", "a", "c", "b"])
    ['a', 'b', 'c', 'd']

    >>> selection_sort([3.2, 1.1, 2.4, 0.5])
    [0.5, 1.1, 2.4, 3.2]
    """
    length = len(collection)
    for i in range(length - 1):
        min_index = i
        for k in range(i + 1, length):
            if collection[k] < collection[min_index]:
                min_index = k
        if min_index != i:
            collection[i], collection[min_index] = collection[min_index], collection[i]
    return collection


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    sorted_list = selection_sort(unsorted)
    print("Sorted List:", sorted_list)
