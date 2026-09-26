from __future__ import annotations


def merge(left_half: list, right_half: list) -> list:
    """归并排序（Merge Sort）的辅助函数。

    >>> left_half = [-2]
    >>> right_half = [-1]
    >>> merge(left_half, right_half)
    [-2, -1]

    >>> left_half = [1,2,3]
    >>> right_half = [4,5,6]
    >>> merge(left_half, right_half)
    [1, 2, 3, 4, 5, 6]

    >>> left_half = [-2]
    >>> right_half = [-1]
    >>> merge(left_half, right_half)
    [-2, -1]

    >>> left_half = [12, 15]
    >>> right_half = [13, 14]
    >>> merge(left_half, right_half)
    [12, 13, 14, 15]

    >>> left_half = []
    >>> right_half = []
    >>> merge(left_half, right_half)
    []
    """
    sorted_array = [None] * (len(right_half) + len(left_half))

    pointer1 = 0  # 指向左半部分当前索引的指针
    pointer2 = 0  # 指向右半部分当前索引的指针
    index = 0  # 指向已排序数组当前索引的指针

    while pointer1 < len(left_half) and pointer2 < len(right_half):
        if left_half[pointer1] < right_half[pointer2]:
            sorted_array[index] = left_half[pointer1]
            pointer1 += 1
            index += 1
        else:
            sorted_array[index] = right_half[pointer2]
            pointer2 += 1
            index += 1
    while pointer1 < len(left_half):
        sorted_array[index] = left_half[pointer1]
        pointer1 += 1
        index += 1

    while pointer2 < len(right_half):
        sorted_array[index] = right_half[pointer2]
        pointer2 += 1
        index += 1

    return sorted_array


def merge_sort(array: list) -> list:
    """使用归并排序，返回排序后的数组元素列表。

    >>> from random import shuffle
    >>> array = [-2, 3, -10, 11, 99, 100000, 100, -200]
    >>> shuffle(array)
    >>> merge_sort(array)
    [-200, -10, -2, 3, 11, 99, 100, 100000]

    >>> shuffle(array)
    >>> merge_sort(array)
    [-200, -10, -2, 3, 11, 99, 100, 100000]

    >>> array = [-200]
    >>> merge_sort(array)
    [-200]

    >>> array = [-2, 3, -10, 11, 99, 100000, 100, -200]
    >>> shuffle(array)
    >>> sorted(array) == merge_sort(array)
    True

    >>> array = [-2]
    >>> merge_sort(array)
    [-2]

    >>> array = []
    >>> merge_sort(array)
    []

    >>> array = [10000000, 1, -1111111111, 101111111112, 9000002]
    >>> sorted(array) == merge_sort(array)
    True
    """
    if len(array) <= 1:
        return array
    # 计算中间元素的公式为 left + (right - left) // 2
    # 当 N 较大时，这可避免整数溢出
    middle = 0 + (len(array) - 0) // 2

    # 将数组分成两半，直到数组长度为 1
    # 合并 mergeSort 函数返回的长度为 1 的数组，
    # 将其传入数组合并函数完成合并
    left_half = array[:middle]
    right_half = array[middle:]

    return merge(merge_sort(left_half), merge_sort(right_half))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
