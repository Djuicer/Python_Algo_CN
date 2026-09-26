"""
这是一种分治（Divide and Conquer）算法，将搜索空间划分为
3 部分，并根据数组或列表的性质
（通常是单调性）查找目标值。

时间复杂度（Time Complexity）  : O(log3 N)
空间复杂度（Space Complexity） : O(1)
"""

from __future__ import annotations

# 这是该函数可调整的精度参数。
# 建议将此值保持为大于或等于 10。
precision = 10


# 搜索空间缩小后，将执行下面的线性查找。


def lin_search(left: int, right: int, array: list[int], target: int) -> int:
    """在列表中执行线性查找。未找到元素则返回 -1。

    Parameters
    ----------
    left : int
        左侧索引边界。
    right : int
        右侧索引边界。
    array : List[int]
        待搜索的元素列表
    target : int
        待查找的元素

    Returns
    -------
    int
        目标元素的索引。

    Examples
    --------
    >>> lin_search(0, 4, [4, 5, 6, 7], 7)
    3
    >>> lin_search(0, 3, [4, 5, 6, 7], 7)
    -1
    >>> lin_search(0, 2, [-18, 2], -18)
    0
    >>> lin_search(0, 1, [5], 5)
    0
    >>> lin_search(0, 3, ['a', 'c', 'd'], 'c')
    1
    >>> lin_search(0, 3, [.1, .4 , -.1], .1)
    0
    >>> lin_search(0, 3, [.1, .4 , -.1], -.1)
    2
    """
    for i in range(left, right):
        if array[i] == target:
            return i
    return -1


def ite_ternary_search(array: list[int], target: int) -> int:
    """三分查找（Ternary Search）算法的迭代实现。
    >>> test_list = [0, 1, 2, 8, 13, 17, 19, 32, 42]
    >>> ite_ternary_search(test_list, 3)
    -1
    >>> ite_ternary_search(test_list, 13)
    4
    >>> ite_ternary_search([4, 5, 6, 7], 4)
    0
    >>> ite_ternary_search([4, 5, 6, 7], -10)
    -1
    >>> ite_ternary_search([-18, 2], -18)
    0
    >>> ite_ternary_search([5], 5)
    0
    >>> ite_ternary_search(['a', 'c', 'd'], 'c')
    1
    >>> ite_ternary_search(['a', 'c', 'd'], 'f')
    -1
    >>> ite_ternary_search([], 1)
    -1
    >>> ite_ternary_search([.1, .4 , -.1], .1)
    0
    >>> test_list_large = list(range(100))
    >>> ite_ternary_search(test_list_large, 65)
    65
    >>> ite_ternary_search(test_list_large, 105)
    -1
    """

    left = 0
    right = len(array)
    while left <= right:
        if right - left < precision:
            return lin_search(left, right, array, target)

        one_third = left + (right - left) // 3
        two_third = right - (right - left) // 3

        if array[one_third] == target:
            return one_third
        elif array[two_third] == target:
            return two_third

        elif target < array[one_third]:
            right = one_third
        elif array[two_third] < target:
            left = two_third + 1

        else:
            left = one_third + 1
            right = two_third
    return -1


def rec_ternary_search(left: int, right: int, array: list[int], target: int) -> int:
    """三分查找算法的递归实现。

    >>> test_list = [0, 1, 2, 8, 13, 17, 19, 32, 42]
    >>> rec_ternary_search(0, len(test_list), test_list, 3)
    -1
    >>> rec_ternary_search(4, len(test_list), test_list, 42)
    8
    >>> rec_ternary_search(0, 2, [4, 5, 6, 7], 4)
    0
    >>> rec_ternary_search(0, 3, [4, 5, 6, 7], -10)
    -1
    >>> rec_ternary_search(0, 1, [-18, 2], -18)
    0
    >>> rec_ternary_search(0, 1, [5], 5)
    0
    >>> rec_ternary_search(0, 2, ['a', 'c', 'd'], 'c')
    1
    >>> rec_ternary_search(0, 2, ['a', 'c', 'd'], 'f')
    -1
    >>> rec_ternary_search(0, 0, [], 1)
    -1
    >>> rec_ternary_search(0, 3, [.1, .4 , -.1], .1)
    0
    >>> test_list_large = list(range(100))
    >>> rec_ternary_search(0, len(test_list_large), test_list_large, 65)
    65
    >>> rec_ternary_search(20, 80, test_list_large, 65)
    65
    >>> rec_ternary_search(20, 80, test_list_large, 15)
    -1
    """
    if left < right:
        if right - left < precision:
            return lin_search(left, right, array, target)
        one_third = left + (right - left) // 3
        two_third = right - (right - left) // 3

        if array[one_third] == target:
            return one_third
        elif array[two_third] == target:
            return two_third

        elif target < array[one_third]:
            return rec_ternary_search(left, one_third, array, target)
        elif array[two_third] < target:
            return rec_ternary_search(two_third + 1, right, array, target)
        else:
            return rec_ternary_search(one_third + 1, two_third, array, target)
    else:
        return -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    user_input = input("Enter numbers separated by comma:\n").strip()
    collection = [int(item.strip()) for item in user_input.split(",")]
    assert collection == sorted(collection), f"List must be ordered.\n{collection}."
    target = int(input("Enter the number to be found in the list:\n").strip())
    result1 = ite_ternary_search(collection, target)
    result2 = rec_ternary_search(0, len(collection), collection, target)
    if result2 != -1:
        print(f"Iterative search: {target} found at positions: {result1}")
        print(f"Recursive search: {target} found at positions: {result2}")
    else:
        print("Not found")
