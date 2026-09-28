"""
给定一个数组 的 整数 并且 整数 k，查找 kth 最大 元素 在 该数组。

https://stackoverflow.com/questions/251781
"""


def partition(arr: list[int], low: int, high: int) -> int:
    """
    Partitions 列表 基于 在 枢轴 元素。

    此函数 rearranges 元素 在 输入 列表 '元素' such 该
    所有元素 更大 比 或 等于 到 chosen 枢轴 是 在 右 一侧
    的 枢轴，并且 所有元素 更小 比 枢轴 是 在 左 一侧。

    参数：
        arr: 该列表 到 为 partitioned
        low: lower 索引 的列表
        high: higher 索引 的列表

    返回值：
        int: 该索引 的 枢轴 元素 之后 partitioning

        示例：
        >>> partition([3, 1, 4, 5, 9, 2, 6, 5, 3, 5], 0, 9)
        4
        >>> partition([7, 1, 4, 5, 9, 2, 6, 5, 8], 0, 8)
        1
        >>> partition(['apple', 'cherry', 'date', 'banana'], 0, 3)
        2
        >>> partition([3.1, 1.2, 5.6, 4.7], 0, 3)
        1
    """
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] >= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def kth_largest_element(arr: list[int], position: int) -> int:
    """
    查找 kth 最大 元素 在 一个列表。
    应 deliver similar results 到：
    ```python
    def kth_largest_element(arr，位置)：
        返回 已排序(arr)[-位置]
    ```

    参数：
        nums: 该列表 的 数。
        k: 位置 的 所需 kth 最大 元素。

    返回值：
        int: kth 最大 元素。

    示例：
        >>> kth_largest_element([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], 3)
        5
        >>> kth_largest_element([2, 5, 6, 1, 9, 3, 8, 4, 7, 3, 5], 1)
        9
        >>> kth_largest_element([2, 5, 6, 1, 9, 3, 8, 4, 7, 3, 5], -2)
        Traceback (most recent call last):
        ...
        ValueError: Invalid value of 'position'
        >>> kth_largest_element([9, 1, 3, 6, 7, 9, 8, 4, 2, 4, 9], 110)
        Traceback (most recent call last):
        ...
        ValueError: Invalid value of 'position'
        >>> kth_largest_element([1, 2, 4, 3, 5, 9, 7, 6, 5, 9, 3], 0)
        Traceback (most recent call last):
        ...
        ValueError: Invalid value of 'position'
        >>> kth_largest_element(['apple', 'cherry', 'date', 'banana'], 2)
        'cherry'
        >>> kth_largest_element([3.1, 1.2, 5.6, 4.7,7.9,5,0], 2)
        5.6
        >>> kth_largest_element([-2, -5, -4, -1], 1)
        -1
        >>> kth_largest_element([], 1)
        -1
        >>> kth_largest_element([3.1, 1.2, 5.6, 4.7, 7.9, 5, 0], 1.5)
        Traceback (most recent call last):
        ...
        ValueError: The position should be an integer
        >>> kth_largest_element((4, 6, 1, 2), 4)
        Traceback (most recent call last):
        ...
        TypeError: 'tuple' object does not support item assignment
    """
    if not arr:
        return -1
    if not isinstance(position, int):
        raise ValueError("The position should be an integer")
    if not 1 <= position <= len(arr):
        raise ValueError("Invalid value of 'position'")
    low, high = 0, len(arr) - 1
    while low <= high:
        if low > len(arr) - 1 or high < 0:
            return -1
        pivot_index = partition(arr, low, high)
        if pivot_index == position - 1:
            return arr[pivot_index]
        elif pivot_index > position - 1:
            high = pivot_index - 1
        else:
            low = pivot_index + 1
    return -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
