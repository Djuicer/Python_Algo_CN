"""
归并排序（Merge Sort）算法。

运行 doctest 请使用以下命令：
python -m doctest -v merge_sort.py
或
python3 -m doctest -v merge_sort.py
手动测试请运行：
python merge_sort.py
"""

from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def merge_sort[T: Comparable](collection: list[T]) -> list[T]:
    """
    使用归并排序算法对列表排序。

    :param collection: 元素可比较的集合。
    :return: 按升序排列的集合。

    时间复杂度：O(n log n)
    空间复杂度：O(n)

    示例：
    >>> merge_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> merge_sort([])
    []

    >>> merge_sort([-2, -45, -5])
    [-45, -5, -2]
    """

    def merge(left: list[T], right: list[T]) -> list[T]:
        """
        将两个有序列表合并为一个有序列表。

        :param left: 左侧集合
        :param right: 右侧集合
        :return: 合并结果
        """
        result: list[T] = []
        while left and right:
            if right[0] < left[0]:
                result.append(right.pop(0))
            else:
                result.append(left.pop(0))
        result.extend(left)
        result.extend(right)
        return result

    if len(collection) <= 1:
        return collection
    mid_index = len(collection) // 2
    return merge(merge_sort(collection[:mid_index]), merge_sort(collection[mid_index:]))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    try:
        user_input = input("Enter numbers separated by a comma:\n").strip()
        unsorted = [int(item) for item in user_input.split(",")]
        sorted_list = merge_sort(unsorted)
        print(*sorted_list, sep=",")
    except ValueError:
        print("Invalid input. Please enter valid integers separated by commas.")
