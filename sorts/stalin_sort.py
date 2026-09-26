"""
斯大林排序（Stalin Sort）：移除顺序不正确的元素。
不大于或等于前一个元素的元素会被丢弃。
Reference: https://medium.com/@kaweendra/the-ultimate-sorting-algorithm-6513d6968420
"""


def stalin_sort(sequence: list[int]) -> list[int]:
    """
    使用斯大林排序算法对列表排序。

    >>> stalin_sort([4, 3, 5, 2, 1, 7])
    [4, 5, 7]

    >>> stalin_sort([1, 2, 3, 4])
    [1, 2, 3, 4]

    >>> stalin_sort([4, 5, 5, 2, 3])
    [4, 5, 5]

    >>> stalin_sort([6, 11, 12, 4, 1, 5])
    [6, 11, 12]

    >>> stalin_sort([5, 0, 4, 3])
    [5]

    >>> stalin_sort([5, 4, 3, 2, 1])
    [5]

    >>> stalin_sort([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]

    >>> stalin_sort([1, 2, 8, 7, 6])
    [1, 2, 8]

    >>> stalin_sort([])
    []

    >>> stalin_sort([7])
    [7]
    """
    if not sequence:
        return []

    result = [sequence[0]]
    for element in sequence[1:]:
        if element >= result[-1]:
            result.append(element)

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
