"""
梳排序（Comb Sort）算法的纯 Python 实现。
梳排序是一种较简单的排序算法，由 Wlodzimierz
Dobosiewicz 于 1980 年设计，Stephen Lacey 和 Richard Box 于 1991 年重新发现。
梳排序改进了冒泡排序。
冒泡排序中，被比较元素的距离（间隔）始终为 1。
梳排序允许间隔远大于 1，避免列表末尾的小值
拖慢排序过程。

More info on: https://en.wikipedia.org/wiki/Comb_sort

运行 doctest 请使用以下命令：
python -m doctest -v comb_sort.py
或
python3 -m doctest -v comb_sort.py

手动测试请运行：
python comb_sort.py
"""

from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def comb_sort[T: Comparable](data: list[T]) -> list[T]:
    """梳排序算法的纯 Python 实现
    :param data: 元素可比较的可变集合
    :return: 按升序排列后的同一个集合
    示例：
    >>> comb_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> comb_sort([])
    []
    >>> comb_sort([99, 45, -7, 8, 2, 0, -15, 3])
    [-15, -7, 0, 2, 3, 8, 45, 99]
    >>> comb_sort([2, 0, 3, 4, 5, 6, 1])
    [0, 1, 2, 3, 4, 5, 6]
    >>> comb_sort(["c", "a", "b"])
    ['a', 'b', 'c']
    >>> comb_sort([2.5, -1, 0.0])
    [-1, 0.0, 2.5]
    >>> comb_sort([1, "a"])
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    shrink_factor = 1.3
    gap = len(data)
    completed = False

    while not completed:
        # 更新下一轮梳理的间隔。间隔不能小于
        # 1：间隔为 0 时，每个元素只与自身比较，不会发生交换，
        # 从而可能在数据尚未有序时退出循环。
        gap = max(int(gap / shrink_factor), 1)
        if gap == 1:
            completed = True

        index = 0
        while index + gap < len(data):
            if data[index + gap] < data[index]:
                # 交换值
                data[index], data[index + gap] = data[index + gap], data[index]
                completed = False
            index += 1

    return data


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(comb_sort(unsorted))
