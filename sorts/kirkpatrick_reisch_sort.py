import heapq
import random

"""
Kirkpatrick-Reisch 排序算法。
将输入分成 sqrt(n) 个块，分别排序，再使用最小堆合并。

时间复杂度：
- 平均情况：O(n * sqrt(n))
- 最坏情况：O(n * sqrt(n))
- 最好情况：O(n * sqrt(n))

空间复杂度：O(n)

说明链接：
https://en.wikipedia.org/wiki/Kirkpatrick%E2%80%93Reisch_sort
https://sortingsearching.com/2020/06/06/kirkpatrick-reisch.html
"""


def kirkpatrick_reisch_sort(arr: list[int]) -> list[int]:
    """
    实现 Kirkpatrick-Reisch 排序算法。

    Args:
    arr (list): 待排序的输入列表。

    Returns:
    list: 包含排序后元素的新列表。

    示例：
    >>> kirkpatrick_reisch_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

    >>> kirkpatrick_reisch_sort([])
    []

    >>> kirkpatrick_reisch_sort([1])
    [1]

    >>> kirkpatrick_reisch_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]

    >>> kirkpatrick_reisch_sort([-1, -3, 5, 0, 2])
    [-3, -1, 0, 2, 5]
    """
    n = len(arr)
    if n <= 1:
        return arr

    # 第 1 步：将输入分成 sqrt(n) 个块
    block_size = int(n**0.5)
    blocks = [arr[i : i + block_size] for i in range(0, n, block_size)]

    # 第 2 步：对每个块排序
    for block in blocks:
        block.sort()

    # 第 3 步：用各块的首元素创建最小堆
    heap = [(block[0], i, 0) for i, block in enumerate(blocks) if block]
    heapq.heapify(heap)

    # 第 4 步：从堆中取出元素，并从各块补入元素
    sorted_arr = []
    while heap:
        val, block_index, element_index = heapq.heappop(heap)
        sorted_arr.append(val)

        if element_index + 1 < len(blocks[block_index]):
            next_element = blocks[block_index][element_index + 1]
            heapq.heappush(heap, (next_element, block_index, element_index + 1))

    return sorted_arr


if __name__ == "__main__":
    # 生成随机整数列表
    arr = [random.randint(1, 1000) for _ in range(100)]

    print("Original Array:", arr)
    sorted_arr = kirkpatrick_reisch_sort(arr)
    print("Sorted Array:", sorted_arr)

    # 验证结果
    assert sorted_arr == sorted(arr)
