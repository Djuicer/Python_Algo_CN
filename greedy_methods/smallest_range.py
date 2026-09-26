"""
smallest_range 接收由有序整数列表组成的列表，找出
至少包含每个列表中一个数的最小区间，并使用最小堆提高效率。
"""

from heapq import heappop, heappush
from sys import maxsize


def smallest_range(nums: list[list[int]]) -> list[int]:
    """
    求覆盖 nums 中每个列表的最小区间。

    使用最小堆（Min Heap）提高效率。区间至少包含每个列表中的一个数。

    参数：
        `nums`：由 k 个有序整数列表组成的列表。

    返回：
        list：以两个元素组成的列表表示最小区间。

    示例：

    >>> smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]])
    [20, 24]
    >>> smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    [1, 1]
    >>> smallest_range(((1, 2, 3), (1, 2, 3), (1, 2, 3)))
    [1, 1]
    >>> smallest_range(((-3, -2, -1), (0, 0, 0), (1, 2, 3)))
    [-1, 1]
    >>> smallest_range([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    [3, 7]
    >>> smallest_range([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    [0, 0]
    >>> smallest_range([[], [], []])
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    """

    min_heap: list[tuple[int, int, int]] = []
    current_max = -maxsize - 1

    for i, items in enumerate(nums):
        heappush(min_heap, (items[0], i, 0))
        current_max = max(current_max, items[0])

    # 使用较大的整数初始化 smallest_range
    smallest_range = [-maxsize - 1, maxsize]

    while min_heap:
        current_min, list_index, element_index = heappop(min_heap)

        if current_max - current_min < smallest_range[1] - smallest_range[0]:
            smallest_range = [current_min, current_max]

        if element_index == len(nums[list_index]) - 1:
            break

        next_element = nums[list_index][element_index + 1]
        heappush(min_heap, (next_element, list_index, element_index + 1))
        current_max = max(current_max, next_element)

    return smallest_range


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    print(f"{smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]])}")  # 输出：[1, 1]
