"""
https://en.wikipedia.org/wiki/Shellsort#Pseudocode
"""

from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def shell_sort[T: Comparable](collection: list[T]) -> list[T]:
    """希尔排序（Shell Sort）算法的纯 Python 实现。

    :param collection:  可变有序集合，其中包含类型可不同但
    可相互比较的元素
    :return:  按升序排列后的同一个集合

    示例：
    >>> shell_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> shell_sort([])
    []
    >>> shell_sort([-2, -5, -45])
    [-45, -5, -2]
    >>> shell_sort(["c", "a", "b"])
    ['a', 'b', 'c']
    >>> shell_sort([2.5, -1.0, 0.0])
    [-1.0, 0.0, 2.5]
    >>> shell_sort([0, 5, 3, 2, 2]) == sorted([0, 5, 3, 2, 2])
    True
    >>> shell_sort(["c", "a", "b"]) == sorted(["c", "a", "b"])
    True
    """
    # Marcin Ciura 的间隔序列
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]
    for gap in gaps:
        for i in range(gap, len(collection)):
            insert_value = collection[i]
            j = i
            while j >= gap and insert_value < collection[j - gap]:
                collection[j] = collection[j - gap]
                j -= gap
            if j != i:
                collection[j] = insert_value
    return collection


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(shell_sort(unsorted))
