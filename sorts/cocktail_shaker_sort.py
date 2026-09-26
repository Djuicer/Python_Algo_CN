"""
鸡尾酒排序（Cocktail Shaker Sort）算法的纯 Python 实现。

https://en.wikipedia.org/wiki/Cocktail_shaker_sort
"""

from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def cocktail_shaker_sort[T: Comparable](arr: list[T]) -> list[T]:
    """
    使用鸡尾酒排序算法对列表排序。

    :param arr: 待排序的元素列表。
    :return: 排序后的列表。

    >>> cocktail_shaker_sort([4, 5, 2, 1, 2])
    [1, 2, 2, 4, 5]
    >>> cocktail_shaker_sort([-4, 5, 0, 1, 2, 11])
    [-4, 0, 1, 2, 5, 11]
    >>> cocktail_shaker_sort([0.1, -2.4, 4.4, 2.2])
    [-2.4, 0.1, 2.2, 4.4]
    >>> cocktail_shaker_sort([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> cocktail_shaker_sort([-4, -5, -24, -7, -11])
    [-24, -11, -7, -5, -4]
    >>> cocktail_shaker_sort(["elderberry", "banana", "date", "apple", "cherry"])
    ['apple', 'banana', 'cherry', 'date', 'elderberry']
    >>> cocktail_shaker_sort((-4, -5, -24, -7, -11))
    Traceback (most recent call last):
        ...
    TypeError: 'tuple' object does not support item assignment
    >>> cocktail_shaker_sort([1, "a"])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: ...
    """
    start, end = 0, len(arr) - 1

    while start < end:
        swapped = False

        # 从左向右遍历
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        end -= 1  # 每轮遍历后减小结束指针

        # 从右向左遍历
        for i in range(end, start, -1):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                swapped = True

        if not swapped:
            break

        start += 1  # 每轮遍历后增大起始指针

    return arr


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(f"{cocktail_shaker_sort(unsorted) = }")
