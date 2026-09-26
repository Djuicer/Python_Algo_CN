"""一种归并排序，接收可比较元素并递归地
将其分成两半，再排序并合并。

https://en.wikipedia.org/wiki/Merge_sort
"""

from collections.abc import Iterable
from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def merge[T: Comparable](collection: Iterable[T]) -> list[T]:
    """返回 ``collection`` 按升序排列的新列表。

    复制输入，因此不会改变原始可迭代对象。
    元素之间必须能够使用 ``<`` 相互比较。

    >>> merge([10,9,8,7,6,5,4,3,2,1])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> merge([1,2,3,4,5,6,7,8,9,10])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> merge([10,22,1,2,3,9,15,23])
    [1, 2, 3, 9, 10, 15, 22, 23]
    >>> merge([100])
    [100]
    >>> merge([])
    []
    >>> merge(["c", "a", "b"])
    ['a', 'b', 'c']
    >>> merge([2.5, -1, 0.0])
    [-1, 0.0, 2.5]
    >>> values = [3, 1, 2]
    >>> merge(values)
    [1, 2, 3]
    >>> values
    [3, 1, 2]
    >>> merge(("b", "c", "a"))
    ['a', 'b', 'c']
    >>> merge([1, "a"])
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'int' and 'str'
    """
    arr = list(collection)
    if len(arr) > 1:
        middle_length = len(arr) // 2  # 查找数组中点
        # 将每一半排成新列表，再将它们合并到 ``arr`` 中。
        left_array = merge(arr[:middle_length])
        right_array = merge(arr[middle_length:])
        left_size = len(left_array)
        right_size = len(right_array)
        left_index = 0  # 左侧计数器
        right_index = 0  # 右侧计数器
        index = 0  # 位置计数器
        while (
            left_index < left_size and right_index < right_size
        ):  # 持续合并，直到左右两半中较短的一半处理完毕。
            if left_array[left_index] < right_array[right_index]:
                arr[index] = left_array[left_index]
                left_index += 1
            else:
                arr[index] = right_array[right_index]
                right_index += 1
            index += 1
        while (
            left_index < left_size
        ):  # 添加数组左半部分的剩余元素
            arr[index] = left_array[left_index]
            left_index += 1
            index += 1
        while (
            right_index < right_size
        ):  # 添加数组右半部分的剩余元素
            arr[index] = right_array[right_index]
            right_index += 1
            index += 1
    return arr


if __name__ == "__main__":
    import doctest

    doctest.testmod()
