"""
实现希尔排序（Shell Sort）算法，
比其基础实现略快。

此实现使用间隔进行希尔排序，
每轮按固定因子缩小间隔。
间隔最初设为
集合长度，然后每轮
按因子 1.3 缩小。

每次迭代时，算法会比较相隔若干位置（由 gap 决定）的元素。
如果较高位置的元素大于较低位置的元素，则交换两者。
重复此过程，直到 gap 等于 1。

这种方法通过减少所需的比较次数来提高效率；随着 gap 缩小，
列表能够更快地完成排序。
"""

from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def shell_sort[T: Comparable](collection: list[T]) -> list[T]:
    """希尔排序算法的 Python 实现
    :param collection:  可变有序集合，其中包含类型可不同但
    可相互比较的元素
    :return:  按升序排列后的同一个集合

    >>> shell_sort([3, 2, 1])
    [1, 2, 3]
    >>> shell_sort([])
    []
    >>> shell_sort([1])
    [1]
    >>> shell_sort(["pear", "apple", "orange"])
    ['apple', 'orange', 'pear']
    >>> shell_sort([2.5, -1, 0.0])
    [-1, 0.0, 2.5]
    >>> shell_sort([1, "a"])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: ...
    """

    # 选择初始间隔值
    gap = len(collection)

    # 设置间隔在每轮之后
    # 按因子 1.3 缩小
    shrink = 1.3

    # 持续排序，直到间隔为 1
    while gap > 1:
        # 缩小间隔
        gap = int(gap / shrink)

        # 使用插入排序处理元素
        for i in range(gap, len(collection)):
            temp = collection[i]
            j = i
            while j >= gap and collection[j - gap] > temp:
                collection[j] = collection[j - gap]
                j -= gap
            collection[j] = temp

    return collection


if __name__ == "__main__":
    import doctest

    doctest.testmod()
