"""
圆圈排序（Circle Sort）算法的 Python 实现

运行 doctest 请使用以下命令：
python3 -m doctest -v circle_sort.py

手动测试请运行：
python3 circle_sort.py
"""

from collections.abc import MutableSequence
from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def circle_sort[T: Comparable](
    collection: MutableSequence[T],
) -> MutableSequence[T]:
    """圆圈排序算法的纯 Python 实现

    :param collection: 顺序任意、元素可比较的可变集合
    :return: 按升序排列后的同一个集合

    示例：
    >>> circle_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> circle_sort([])
    []
    >>> circle_sort([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    >>> circle_sort(["d", "a", "c", "b"])
    ['a', 'b', 'c', 'd']
    >>> circle_sort([2.5, -1.0, 0.0])
    [-1.0, 0.0, 2.5]
    >>> circle_sort([1, "a"])
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    >>> collections = ([], [0, 5, 3, 2, 2], [-2, 5, 0, -45])
    >>> all(sorted(collection) == circle_sort(collection) for collection in collections)
    True
    """

    if len(collection) < 2:
        return collection

    def circle_sort_util(collection: MutableSequence[T], low: int, high: int) -> bool:
        """
        >>> arr = [5,4,3,2,1]
        >>> circle_sort_util(arr, 0, 2)
        True
        >>> arr
        [3, 4, 5, 2, 1]
        """

        swapped = False

        if low == high:
            return swapped

        left = low
        right = high

        while left < right:
            if collection[right] < collection[left]:
                collection[left], collection[right] = (
                    collection[right],
                    collection[left],
                )
                swapped = True

            left += 1
            right -= 1

        if left == right and collection[right + 1] < collection[left]:
            collection[left], collection[right + 1] = (
                collection[right + 1],
                collection[left],
            )

            swapped = True

        mid = low + int((high - low) / 2)
        left_swap = circle_sort_util(collection, low, mid)
        right_swap = circle_sort_util(collection, mid + 1, high)

        return swapped or left_swap or right_swap

    is_not_sorted = True

    while is_not_sorted is True:
        is_not_sorted = circle_sort_util(collection, 0, len(collection) - 1)

    return collection


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(circle_sort(unsorted))
