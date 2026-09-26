"""
侏儒排序（Gnome Sort，也称 Stupid Sort）算法

遍历列表，将元素与其前一个元素比较。
若顺序不正确，则向前交换，直到与前一个元素的顺序正确。
然后从元素的新位置继续原有遍历。

运行 doctest 请使用以下命令：
python3 -m doctest -v gnome_sort.py

手动测试请运行：
python3 gnome_sort.py
"""

from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def gnome_sort[T: Comparable](lst: list[T]) -> list[T]:
    """
    侏儒排序算法的纯 Python 实现

    接收一个可变有序集合，其中包含类型可不同但可相互比较的元素，
    返回按升序排列后的同一个集合。

    示例：
    >>> gnome_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> gnome_sort([])
    []

    >>> gnome_sort([-2, -5, -45])
    [-45, -5, -2]

    >>> "".join(gnome_sort(list(set("Gnomes are stupid!"))))
    ' !Gadeimnoprstu'
    """
    if len(lst) <= 1:
        return lst

    i = 1

    while i < len(lst):
        if not lst[i] < lst[i - 1]:
            i += 1
        else:
            lst[i - 1], lst[i] = lst[i], lst[i - 1]
            i -= 1
            if i == 0:
                i = 1

    return lst


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(gnome_sort(unsorted))
