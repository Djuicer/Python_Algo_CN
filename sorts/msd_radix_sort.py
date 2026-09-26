"""
最高位优先基数排序（MSD Radix Sort）算法的 Python 实现。
根据整数的二进制表示
进行排序。
https://en.wikipedia.org/wiki/Radix_sort
"""

from __future__ import annotations


def msd_radix_sort(list_of_ints: list[int]) -> list[int]:
    """
    最高位优先基数排序算法的实现，仅适用于
    正整数
    :param list_of_ints: 整数列表
    :return: 返回排序后的列表
    >>> msd_radix_sort([40, 12, 1, 100, 4])
    [1, 4, 12, 40, 100]
    >>> msd_radix_sort([])
    []
    >>> msd_radix_sort([123, 345, 123, 80])
    [80, 123, 123, 345]
    >>> msd_radix_sort([1209, 834598, 1, 540402, 45])
    [1, 45, 1209, 540402, 834598]
    >>> msd_radix_sort([-1, 34, 45])
    Traceback (most recent call last):
        ...
    ValueError: All numbers must be positive
    """
    if not list_of_ints:
        return []

    if min(list_of_ints) < 0:
        raise ValueError("All numbers must be positive")

    most_bits = max(len(bin(x)[2:]) for x in list_of_ints)
    return _msd_radix_sort(list_of_ints, most_bits)


def _msd_radix_sort(list_of_ints: list[int], bit_position: int) -> list[int]:
    """
    根据 bit_position 处的位对列表排序。该位为
    0 的数放在列表前部，该位为
    1 的数放在后部。
    :param list_of_ints: 整数列表
    :param bit_position: 待比较的位的位置
    :return: 返回部分排序后的列表
    >>> _msd_radix_sort([45, 2, 32], 1)
    [2, 32, 45]
    >>> _msd_radix_sort([10, 4, 12], 2)
    [4, 12, 10]
    """
    if bit_position == 0 or len(list_of_ints) in [0, 1]:
        return list_of_ints

    zeros = []
    ones = []
    # 根据从右侧起 bit_position 处的位划分整数
    for number in list_of_ints:
        if (number >> (bit_position - 1)) & 1:
            # 该整数在 bit_position 处为 1
            ones.append(number)
        else:
            # 该整数在 bit_position 处为 0
            zeros.append(number)

    # 递归进一步划分两个列表
    zeros = _msd_radix_sort(zeros, bit_position - 1)
    ones = _msd_radix_sort(ones, bit_position - 1)

    # 重新合并列表
    res = zeros
    res.extend(ones)

    return res


def msd_radix_sort_inplace(list_of_ints: list[int]) -> None:
    """
    最高位优先基数排序算法的原地实现。
    根据整数的二进制表示排序。
    >>> lst = [1, 345, 23, 89, 0, 3]
    >>> msd_radix_sort_inplace(lst)
    >>> lst == sorted(lst)
    True
    >>> lst = [1, 43, 0, 0, 0, 24, 3, 3]
    >>> msd_radix_sort_inplace(lst)
    >>> lst == sorted(lst)
    True
    >>> lst = []
    >>> msd_radix_sort_inplace(lst)
    >>> lst == []
    True
    >>> lst = [-1, 34, 23, 4, -42]
    >>> msd_radix_sort_inplace(lst)
    Traceback (most recent call last):
        ...
    ValueError: All numbers must be positive
    """

    length = len(list_of_ints)
    if not list_of_ints or length == 1:
        return

    if min(list_of_ints) < 0:
        raise ValueError("All numbers must be positive")

    most_bits = max(len(bin(x)[2:]) for x in list_of_ints)
    _msd_radix_sort_inplace(list_of_ints, most_bits, 0, length)


def _msd_radix_sort_inplace(
    list_of_ints: list[int], bit_position: int, begin_index: int, end_index: int
) -> None:
    """
    根据 bit_position 处的位对列表排序。该位为
    0 的数放在列表前部，该位为
    1 的数放在后部。
    >>> lst = [45, 2, 32, 24, 534, 2932]
    >>> _msd_radix_sort_inplace(lst, 1, 0, 3)
    >>> lst == [32, 2, 45, 24, 534, 2932]
    True
    >>> lst = [0, 2, 1, 3, 12, 10, 4, 90, 54, 2323, 756]
    >>> _msd_radix_sort_inplace(lst, 2, 4, 7)
    >>> lst == [0, 2, 1, 3, 12, 4, 10, 90, 54, 2323, 756]
    True
    """
    if bit_position == 0 or end_index - begin_index <= 1:
        return

    bit_position -= 1

    i = begin_index
    j = end_index - 1
    while i <= j:
        changed = False
        if not (list_of_ints[i] >> bit_position) & 1:
            # 在前部找到零
            i += 1
            changed = True
        if (list_of_ints[j] >> bit_position) & 1:
            # 在后部找到一
            j -= 1
            changed = True

        if changed:
            continue

        list_of_ints[i], list_of_ints[j] = list_of_ints[j], list_of_ints[i]
        j -= 1
        if j != i:
            i += 1

    _msd_radix_sort_inplace(list_of_ints, bit_position, begin_index, i)
    _msd_radix_sort_inplace(list_of_ints, bit_position, i, end_index)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
