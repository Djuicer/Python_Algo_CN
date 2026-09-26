def search(list_data: list, key: int, left: int = 0, right: int = 0) -> int:
    """
    使用递归遍历数组，查找 key 的索引。
    :param list_data: 待搜索的列表
    :param key: 待查找的键值
    :param left: 第一个元素的索引
    :param right: 最后一个元素的索引
    :return: 找到 key 则返回其索引，否则返回 -1。

    >>> search(list(range(0, 11)), 5)
    5
    >>> search([1, 2, 4, 5, 3], 4)
    2
    >>> search([1, 2, 4, 5, 3], 6)
    -1
    >>> search([5], 5)
    0
    >>> search([], 1)
    -1
    """
    right = right or len(list_data) - 1
    if left > right:
        return -1
    elif list_data[left] == key:
        return left
    elif list_data[right] == key:
        return right
    else:
        return search(list_data, key, left + 1, right - 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
