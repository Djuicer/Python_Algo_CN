"""
插值查找（Interpolation Search）算法的纯 Python 实现
"""


def interpolation_search(sorted_collection: list[int], item: int) -> int | None:
    """
    使用插值查找算法在有序集合中查找元素。

    Args:
        sorted_collection: 已排序的整数列表
        item: 待查找的元素值

    Returns:
        int: 找到的元素索引；未找到则返回 None。
    示例：
    >>> interpolation_search([1, 2, 3, 4, 5], 2)
    1
    >>> interpolation_search([1, 2, 3, 4, 5], 4)
    3
    >>> interpolation_search([1, 2, 3, 4, 5], 6) is None
    True
    >>> interpolation_search([], 1) is None
    True
    >>> interpolation_search([100], 100)
    0
    >>> interpolation_search([1, 2, 3, 4, 5], 0) is None
    True
    >>> interpolation_search([1, 2, 3, 4, 5], 7) is None
    True
    >>> interpolation_search([1, 2, 3, 4, 5], 2)
    1
    >>> interpolation_search([1, 2, 3, 4, 5], 0) is None
    True
    >>> interpolation_search([1, 2, 3, 4, 5], 7) is None
    True
    >>> interpolation_search([1, 2, 3, 4, 5], 2)
    1
    >>> interpolation_search([5, 5, 5, 5, 5], 3) is None
    True
    """
    left = 0
    right = len(sorted_collection) - 1

    while left <= right:
        # 避免插值计算时除以 0
        if sorted_collection[left] == sorted_collection[right]:
            if sorted_collection[left] == item:
                return left
            return None

        point = left + ((item - sorted_collection[left]) * (right - left)) // (
            sorted_collection[right] - sorted_collection[left]
        )

        # 检查索引是否越界
        if point < 0 or point >= len(sorted_collection):
            return None

        current_item = sorted_collection[point]
        if current_item == item:
            return point
        if point < left:
            right = left
            left = point
        elif point > right:
            left = right
            right = point
        elif item < current_item:
            right = point - 1
        else:
            left = point + 1
    return None


def interpolation_search_by_recursion(
    sorted_collection: list[int], item: int, left: int = 0, right: int | None = None
) -> int | None:
    """插值查找算法的纯 Python 递归实现
    注意，集合必须按升序排列，否则结果
    不可预测。
    首次递归调用应设置 left=0 和 right=(len(sorted_collection)-1)

    Args:
        sorted_collection: 元素可比较的有序集合
        item: 待查找的元素值
        left: 集合中的左侧索引
        right: 集合中的右侧索引

    Returns:
        元素在集合中的索引；元素不存在则返回 None

    示例：
    >>> interpolation_search_by_recursion([0, 5, 7, 10, 15], 0)
    0
    >>> interpolation_search_by_recursion([0, 5, 7, 10, 15], 15)
    4
    >>> interpolation_search_by_recursion([0, 5, 7, 10, 15], 5)
    1
    >>> interpolation_search_by_recursion([0, 5, 7, 10, 15], 100) is None
    True
    >>> interpolation_search_by_recursion([0, 5, 7, 10, 15], 16) is None
    True
    >>> interpolation_search_by_recursion([0, 5, 7, 10, 15], -1) is None
    True
    >>> interpolation_search_by_recursion([0, 3, 6, 12, 14, 15, 20], 10) is None
    True
    >>> interpolation_search_by_recursion([], 1) is None
    True
    >>> interpolation_search_by_recursion([5, 5, 5, 5, 5], 3) is None
    True
    """
    if right is None:
        right = len(sorted_collection) - 1
    if left > right:
        return None
    # 避免插值计算时除以 0
    if sorted_collection[left] == sorted_collection[right]:
        return left if sorted_collection[left] == item else None

    point = left + ((item - sorted_collection[left]) * (right - left)) // (
        sorted_collection[right] - sorted_collection[left]
    )

    # 检查索引是否越界
    if point < 0 or point >= len(sorted_collection):
        return None

    if sorted_collection[point] == item:
        return point
    if point < left:
        return interpolation_search_by_recursion(sorted_collection, item, point, left)
    if point > right:
        return interpolation_search_by_recursion(sorted_collection, item, right, left)
    if sorted_collection[point] > item:
        return interpolation_search_by_recursion(
            sorted_collection, item, left, point - 1
        )
    return interpolation_search_by_recursion(sorted_collection, item, point + 1, right)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
