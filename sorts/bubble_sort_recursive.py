"""
递归冒泡排序（Bubble Sort）算法的纯 Python 实现。
"""

from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def bubble_sort_recursive[T: Comparable](arr: list[T]) -> list[T]:
    """
    使用递归冒泡排序算法对可比较元素的列表排序。

    >>> bubble_sort_recursive([5, 1, 4, 2, 8])
    [1, 2, 4, 5, 8]
    >>> bubble_sort_recursive([])
    []
    >>> bubble_sort_recursive([1])
    [1]
    >>> bubble_sort_recursive([3, 3, 2, 1])
    [1, 2, 3, 3]
    >>> bubble_sort_recursive([-1, 5, 0, -2])
    [-2, -1, 0, 5]
    >>> bubble_sort_recursive(["banana", "apple", "cherry"])
    ['apple', 'banana', 'cherry']
    >>> bubble_sort_recursive([3.14, 1.5, 2.7])
    [1.5, 2.7, 3.14]
    >>> bubble_sort_recursive([1, "two"])  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...
    """
    n = len(arr)
    if n <= 1:
        return arr

    swapped = False
    for i in range(n - 1):
        if arr[i + 1] < arr[i]:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
            swapped = True

    if not swapped:
        return arr

    return [*bubble_sort_recursive(arr[:-1]), arr[-1]]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
