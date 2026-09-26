from __future__ import annotations


def double_linear_search(array: list[int], search_item: int) -> int:
    """
    从数组两端遍历，查找 search_item 的索引。

    :param array: 待搜索的数组
    :param search_item: 待查找的元素
    :return 若 search_item 在 array 中，返回其索引；否则返回 -1

    示例：
    >>> double_linear_search([1, 5, 5, 10], 1)
    0
    >>> double_linear_search([1, 5, 5, 10], 5)
    1
    >>> double_linear_search([1, 5, 5, 10], 100)
    -1
    >>> double_linear_search([1, 5, 5, 10], 10)
    3
    """
    # 定义给定数组的起始和结束索引
    start_ind, end_ind = 0, len(array) - 1
    while start_ind <= end_ind:
        if array[start_ind] == search_item:
            return start_ind
        elif array[end_ind] == search_item:
            return end_ind
        else:
            start_ind += 1
            end_ind -= 1
    # 若在 array 中未找到 search_item，则返回 -1
    return -1


if __name__ == "__main__":
    print(double_linear_search(list(range(100)), 40))
