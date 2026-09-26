from collections.abc import Sequence
from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def binary_search[T: Comparable](lst: list[T], item: T, start: int, end: int) -> int:
    """>>> binary_search([1, 3, 5], 4, 0, 2)
    2
    >>> binary_search([1, 3, 5], 0, 0, 2)
    0
    >>> binary_search([1, 3, 5], 6, 0, 2)
    3

    在有序子列表中查找 ``item`` 的插入索引。

    在 ``lst`` 的 ``start`` 到 ``end`` 索引范围内
    （包含两端）执行递归二分查找，返回
    能够保持列表有序的插入位置。

    Args:
        lst: 元素可比较的列表。
             ``start`` 到 ``end`` 的子列表必须已有序。
        item: 待查找插入位置的值。
        start: 待搜索有序子列表的最左索引。
        end: 待搜索有序子列表的最右索引。

    Returns:
        ``item`` 应插入的索引。

    复杂度：
        时间：相对于待搜索子列表为 ``O(log n)``。
        空间：递归深度带来 ``O(log n)`` 开销。
    """
    if start == end:
        return start if item < lst[start] else start + 1
    if start > end:
        return start

    mid = (start + end) // 2
    if lst[mid] < item:
        return binary_search(lst, item, mid + 1, end)
    elif item < lst[mid]:
        return binary_search(lst, item, start, mid - 1)
    else:
        return mid


def insertion_sort[T: Comparable](lst: list[T]) -> list[T]:
    """>>> insertion_sort([3, 2, 1])
    [1, 2, 3]

    使用插入排序返回 ``lst`` 的已排序副本。

    使用 ``binary_search`` 查找每个元素的插入位置。
    不修改输入列表，返回新的有序列表。

    Args:
        lst: 待排序的列表。返回新列表，不会
            原地修改输入。

    Returns:
        包含 ``lst`` 所有元素、按升序排列的新列表。

    复杂度：
        时间：最坏为 ``O(n^2)``，因为每次插入都可能
            移动多个元素。
        空间：重建列表副本需要 ``O(n)``。
    """
    length = len(lst)

    for index in range(1, length):
        value = lst[index]
        pos = binary_search(lst, value, 0, index - 1)
        lst = [*lst[:pos], value, *lst[pos:index], *lst[index + 1 :]]

    return lst


def merge[T: Comparable](left: list[T], right: list[T]) -> list[T]:
    """>>> merge([1, 4], [2, 3])
    [1, 2, 3, 4]

    合并两个有序列表，返回新的有序列表。

    Args:
        left: 按升序排列的列表。
        right: 按升序排列的列表。

    Returns:
        包含 ``left`` 和 ``right`` 所有元素、按
        升序排列的新列表。

    复杂度：
        时间：``O(n + m)``，其中 ``n`` 和 ``m`` 为输入长度。
        空间：``O(n + m)``，因为递归切片会创建新列表。
    """
    if not left:
        return right

    if not right:
        return left

    if left[0] < right[0]:
        return [left[0], *merge(left[1:], right)]

    return [right[0], *merge(left, right[1:])]


def tim_sort[T: Comparable](lst: Sequence[T]) -> list[T]:
    """
    使用类似 TimSort 的方式排序并返回输入：检测
    有序段，使用插入排序处理各段，再合并这些段。

    复杂度：
        时间：通常为 ``O(n log n)``。
        空间：排序中使用的额外列表需要 ``O(n)``。

    >>> tim_sort([])
    []
    >>> tim_sort("Python")
    ['P', 'h', 'n', 'o', 't', 'y']
    >>> tim_sort((1.1, 1, 0, -1, -1.1))
    [-1.1, -1, 0, 1, 1.1]
    >>> tim_sort(list(reversed(list(range(7)))))
    [0, 1, 2, 3, 4, 5, 6]
    >>> tim_sort([3, 2, 1]) == insertion_sort([3, 2, 1])
    True
    >>> tim_sort([3, 2, 1]) == sorted([3, 2, 1])
    True
    >>> tim_sort([1, "a"])
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'str' and 'int'

    """
    if not lst:
        return []
    length = len(lst)
    runs, sorted_runs = [], []
    new_run = [lst[0]]
    sorted_array: list[T] = []
    i = 1
    while i < length:
        if lst[i] < lst[i - 1]:
            runs.append(new_run)
            new_run = [lst[i]]
        else:
            new_run.append(lst[i])
        i += 1
    runs.append(new_run)

    for run in runs:
        sorted_runs.append(insertion_sort(run))
    for run in sorted_runs:
        sorted_array = merge(sorted_array, run)

    return sorted_array


def main() -> None:
    lst = [5, 9, 10, 3, -4, 5, 178, 92, 46, -18, 0, 7]
    sorted_lst = tim_sort(lst)
    print(sorted_lst)


if __name__ == "__main__":
    main()
