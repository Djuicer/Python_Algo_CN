"""
双调排序（Bitonic Sort）的 Python 程序。

注意，此程序仅适用于输入大小为 2 的幂的情况。
"""

from __future__ import annotations

from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def comp_and_swap[T: Comparable](
    array: list[T], index1: int, index2: int, direction: int
) -> None:
    """比较数组中给定 index1 和 index2 位置的值，并根据
    指定方向交换它们。

    direction 参数指定排序方向：升序 ASCENDING(1) 或
    降序 DESCENDING(0)。若 (a[i] > a[j]) 与指定方向一致，
    则交换 a[i] 与 a[j]。

    >>> arr = [12, 42, -21, 1]
    >>> comp_and_swap(arr, 1, 2, 1)
    >>> arr
    [12, -21, 42, 1]

    >>> comp_and_swap(arr, 1, 2, 0)
    >>> arr
    [12, 42, -21, 1]

    >>> comp_and_swap(arr, 0, 3, 1)
    >>> arr
    [1, 42, -21, 12]

    >>> comp_and_swap(arr, 0, 3, 0)
    >>> arr
    [12, 42, -21, 1]
    """
    if (direction == 1 and array[index2] < array[index1]) or (
        direction == 0 and array[index1] < array[index2]
    ):
        array[index1], array[index2] = array[index2], array[index1]


def bitonic_merge[T: Comparable](
    array: list[T], low: int, length: int, direction: int
) -> None:
    """
    递归排序双调序列：direction = 1 时为升序，
    direction = 0 时为降序。
    待排序序列从索引 low 开始，length 参数表示
    待排序的元素数量。

    >>> arr = [12, 42, -21, 1]
    >>> bitonic_merge(arr, 0, 4, 1)
    >>> arr
    [-21, 1, 12, 42]

    >>> bitonic_merge(arr, 0, 4, 0)
    >>> arr
    [42, 12, 1, -21]
    """
    if length > 1:
        middle = int(length / 2)
        for i in range(low, low + middle):
            comp_and_swap(array, i, i + middle, direction)
        bitonic_merge(array, low, middle, direction)
        bitonic_merge(array, low + middle, middle, direction)


def bitonic_sort[T: Comparable](
    array: list[T], low: int, length: int, direction: int
) -> None:
    """
    先将两个半区递归排成相反的顺序，生成
    双调序列，再调用 bitonic_merge 将它们合并为
    相同顺序。

    >>> arr = [12, 34, 92, -23, 0, -121, -167, 145]
    >>> bitonic_sort(arr, 0, 8, 1)
    >>> arr
    [-167, -121, -23, 0, 12, 34, 92, 145]

    >>> bitonic_sort(arr, 0, 8, 0)
    >>> arr
    [145, 92, 34, 12, 0, -23, -121, -167]

    >>> arr = ["banana", "apple", "cherry", "date"]
    >>> bitonic_sort(arr, 0, 4, 1)
    >>> arr
    ['apple', 'banana', 'cherry', 'date']

    >>> arr = [3, 1.5, 2, 4.5]
    >>> bitonic_sort(arr, 0, 4, 1)
    >>> arr
    [1.5, 2, 3, 4.5]

    >>> arr = [1, "two", 3, "four"]
    >>> bitonic_sort(arr, 0, 4, 1)
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    if length > 1:
        middle = int(length / 2)
        bitonic_sort(array, low, middle, 1)
        bitonic_sort(array, low + middle, middle, 0)
        bitonic_merge(array, low, length, direction)


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item.strip()) for item in user_input.split(",")]

    bitonic_sort(unsorted, 0, len(unsorted), 1)
    print("\nSorted array in ascending order is: ", end="")
    print(*unsorted, sep=", ")

    bitonic_merge(unsorted, 0, len(unsorted), 0)
    print("Sorted array in descending order is: ", end="")
    print(*unsorted, sep=", ")
