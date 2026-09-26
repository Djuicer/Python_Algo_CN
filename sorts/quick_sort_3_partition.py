from random import randrange
from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def quick_sort_3partition[T: Comparable](
    sorting: list[T], left: int, right: int
) -> None:
    """ "
    采用三路划分的快速排序算法的 Python 实现。
    三路快速排序的思想基于荷兰国旗算法。

    :param sorting: 待排序列表
    :param left: sorting 的左端点
    :param right: sorting 的右端点
    :return: None

    示例：
    >>> array1 = [5, -1, -1, 5, 5, 24, 0]
    >>> quick_sort_3partition(array1, 0, 6)
    >>> array1
    [-1, -1, 0, 5, 5, 5, 24]
    >>> array2 = [9, 0, 2, 6]
    >>> quick_sort_3partition(array2, 0, 3)
    >>> array2
    [0, 2, 6, 9]
    >>> array3 = []
    >>> quick_sort_3partition(array3, 0, 0)
    >>> array3
    []
    """
    if right <= left:
        return
    a = i = left
    b = right
    pivot = sorting[left]
    while i <= b:
        if sorting[i] < pivot:
            sorting[a], sorting[i] = sorting[i], sorting[a]
            a += 1
            i += 1
        elif sorting[i] > pivot:
            sorting[b], sorting[i] = sorting[i], sorting[b]
            b -= 1
        else:
            i += 1
    quick_sort_3partition(sorting, left, a - 1)
    quick_sort_3partition(sorting, b + 1, right)


def quick_sort_lomuto_partition[T: Comparable](
    sorting: list[T], left: int, right: int
) -> None:
    """
    快速排序算法的纯 Python 原地实现，
    采用 Lomuto 划分方案：
    https://en.wikipedia.org/wiki/Quicksort#Lomuto_partition_scheme

    :param sorting: 待排序列表
    :param left: sorting 的左端点
    :param right: sorting 的右端点
    :return: None

    示例：
    >>> nums1 = [0, 5, 3, 1, 2]
    >>> quick_sort_lomuto_partition(nums1, 0, 4)
    >>> nums1
    [0, 1, 2, 3, 5]
    >>> nums2 = []
    >>> quick_sort_lomuto_partition(nums2, 0, 0)
    >>> nums2
    []
    >>> nums3 = [-2, 5, 0, -4]
    >>> quick_sort_lomuto_partition(nums3, 0, 3)
    >>> nums3
    [-4, -2, 0, 5]
    """
    if left < right:
        pivot_index = lomuto_partition(sorting, left, right)
        quick_sort_lomuto_partition(sorting, left, pivot_index - 1)
        quick_sort_lomuto_partition(sorting, pivot_index + 1, right)


def lomuto_partition[T: Comparable](sorting: list[T], left: int, right: int) -> int:
    """
    示例：
    >>> lomuto_partition([1,5,7,6], 0, 3)
    2
    """
    pivot = sorting[right]
    store_index = left
    for i in range(left, right):
        if sorting[i] < pivot:
            sorting[store_index], sorting[i] = sorting[i], sorting[store_index]
            store_index += 1
    sorting[right], sorting[store_index] = sorting[store_index], sorting[right]
    return store_index


def hoare_partition_by_value[T: Comparable](
    array: list[T], pivot_value: T, start: int = 0, end: int | None = None
) -> int:
    """
    返回右侧子数组的起始索引，该子数组包含
    大于或等于 `pivot_value` 的元素

    >>> list_unsorted = [7, 3, 5, 4, 1, 8, 6]
    >>> array = list_unsorted.copy()
    >>> hoare_partition_by_value(array, 5)
    3
    >>> array
    [1, 3, 4, 5, 7, 8, 6]

    边界情况：
    >>> hoare_partition_by_value(list_unsorted.copy(), 0)
    0
    >>> hoare_partition_by_value(list_unsorted.copy(), 1)
    0
    >>> hoare_partition_by_value(list_unsorted.copy(), 2)
    1
    >>> hoare_partition_by_value(list_unsorted.copy(), 8)
    6
    >>> hoare_partition_by_value(list_unsorted.copy(), 9)
    7

    """
    if end is None:
        end = len(array) - 1

    left = start
    right = end

    while True:
        """
        某次中间迭代的状态可能如下：

            lllluuuuuuuuuurrrrr
                ^        ^
                |        |
              left      right

        中间部分尚未遍历，因此其值未知（u）。
        `left-1` 指向左子数组末尾。
        `right+1` 指向右子数组开头。
        """

        while array[left] < pivot_value:
            left += 1
            if left > end:
                # 右侧子数组为空。
                # 返回越界索引以表示这一情况。
                return end + 1
        while array[right] >= pivot_value:
            right -= 1
            if right < start:
                # 左侧子数组为空
                return start

        if left > right:
            break

        # 不变式：
        assert all(i < pivot_value for i in array[start:left])
        assert all(i >= pivot_value for i in array[right + 1 : end])
        """
            llllllruuuuulrrrrrr
                  ^     ^
                  |     |
                left   right
        """

        # 交换
        array[left], array[right] = array[right], array[left]

        left += 1
        right -= 1

    return right + 1


def hoare_partition_by_pivot[T: Comparable](
    array: list[T], pivot_index: int, start=0, end: int | None = None
) -> int:
    """
    返回划分后枢轴的新索引

    >>> array = [7, 3, 5, 4, 1, 8, 6]
    >>> array[3]
    4
    >>> hoare_partition_by_pivot(array, 3)
    2
    >>> array
    [1, 3, 4, 6, 7, 8, 5]
    """
    if end is None:
        end = len(array) - 1

    def swap(i1, i2):
        array[i1], array[i2] = array[i2], array[i1]

    pivot_value = array[pivot_index]
    swap(pivot_index, end)
    greater_or_equal = hoare_partition_by_value(
        array, pivot_value, start=start, end=end - 1
    )
    swap(end, greater_or_equal)
    return greater_or_equal


def quicksort_hoare[T: Comparable](
    array: list[T], start: int = 0, end: int | None = None
) -> None:
    """
    使用 Hoare 划分方案的快速排序：
    - https://en.wikipedia.org/wiki/Quicksort#Hoare_partition_scheme
    - The Art of Computer Programming, Volume 3: Sorting and Searching

    >>> array = [2, 2, 8, 0, 3, 7, 2, 1, 8, 8]
    >>> quicksort_hoare(array)
    >>> array
    [0, 1, 2, 2, 2, 3, 7, 8, 8, 8]
    """
    if end is None:
        end = len(array) - 1

    if end + 1 - start <= 1:
        return

    pivot_index_final = hoare_partition_by_pivot(
        array, randrange(start, end), start, end
    )
    quicksort_hoare(array, start, pivot_index_final - 1)
    quicksort_hoare(array, pivot_index_final + 1, end)


def three_way_radix_quicksort[T: Comparable](sorting: list[T]) -> list[T]:
    """
    三路基数快速排序：
    https://en.wikipedia.org/wiki/Quicksort#Three-way_radix_quicksort
    先将列表分成三部分。
    然后递归排序“小于”和“大于”枢轴的部分。

    >>> three_way_radix_quicksort([])
    []
    >>> three_way_radix_quicksort([1])
    [1]
    >>> three_way_radix_quicksort([-5, -2, 1, -2, 0, 1])
    [-5, -2, -2, 0, 1, 1]
    >>> three_way_radix_quicksort([1, 2, 5, 1, 2, 0, 0, 5, 2, -1])
    [-1, 0, 0, 1, 1, 2, 2, 2, 5, 5]
    """
    if len(sorting) <= 1:
        return sorting
    return (
        three_way_radix_quicksort([i for i in sorting if i < sorting[0]])
        + [i for i in sorting if i == sorting[0]]
        + three_way_radix_quicksort([i for i in sorting if i > sorting[0]])
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    quick_sort_3partition(unsorted, 0, len(unsorted) - 1)
    print(unsorted)
