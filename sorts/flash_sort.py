#!/usr/bin/env python3
"""
闪电排序（Flash Sort）算法实现

闪电排序是一种分布排序算法，对于均匀分布的数据集，
其计算复杂度为线性的 O(n)，且额外内存
需求较少。基本思想是利用待排序值的分布，
直接确定它们大致的最终位置，
避免像其他算法那样，反复比较并将元素
移动到多个中间位置。

该算法由 Karl-Dietrich Neubert 于 1998 年提出，基于
桶排序思想，先将元素划分为若干类，
再对各类进行排序。

时间复杂度：
- 最好情况：数据均匀分布时为 O(n)
- 平均情况：O(n + k)，其中 k 为类数
- 最坏情况：数据分布不均匀时为 O(n²)

空间复杂度：O(k)，其中 k 为类数

Source: https://en.wikipedia.org/wiki/Flashsort
"""

from __future__ import annotations


def flash_sort(arr: list[int | float]) -> list[int | float]:
    """
    使用闪电排序算法对列表排序。

    闪电排序对均匀分布的数据尤其高效。
    利用数值分布确定元素的大致位置。

    Args:
        arr: 待排序的整数或浮点数列表

    Returns:
        按升序排列的列表

    示例：
    >>> flash_sort([4, 2, 7, 1, 9, 3])
    [1, 2, 3, 4, 7, 9]
    >>> flash_sort([])
    []
    >>> flash_sort([5])
    [5]
    >>> flash_sort([3, 3, 3, 3])
    [3, 3, 3, 3]
    >>> flash_sort([-1, -5, 0, 3, 2])
    [-5, -1, 0, 2, 3]
    >>> flash_sort([1.5, 2.3, 0.1, 3.7, 1.2])
    [0.1, 1.2, 1.5, 2.3, 3.7]
    >>> flash_sort([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> import random
    >>> data = random.sample(range(100), 20)
    >>> flash_sort(data) == sorted(data)
    True
    >>> flash_sort([42])
    [42]
    >>> flash_sort([2.5, 1.1, 3.3, 2.5, 1.1])
    [1.1, 1.1, 2.5, 2.5, 3.3]
    >>> flash_sort([6, 6, 4, 4, 6])
    [4, 4, 6, 6, 6]
    >>> flash_sort([8, 3, 8, 6, 8])
    [3, 6, 8, 8, 8]
    """
    if len(arr) <= 1:
        return arr.copy()

    # 创建副本，避免修改原数组
    result = arr.copy()
    n = len(result)

    # 查找最小值和最大值
    min_val = min(result)
    max_val = max(result)

    # 所有元素相同时，直接返回数组
    if min_val == max_val:
        return result

    # 类（桶）的数量，通常取 n/10 到 n/5 效果较好
    m = max(1, int(0.45 * n))

    # 初始化各类大小的数组
    class_sizes = [0] * m

    # 计算各类大小
    c1 = (m - 1) / (max_val - min_val)

    for value in result:
        class_index = int(c1 * (value - min_val))
        if class_index >= m:
            class_index = m - 1
        class_sizes[class_index] += 1

    # 计算各类的累计大小（位置）
    for i in range(1, m):
        class_sizes[i] += class_sizes[i - 1]

    # 置换阶段：使用循环领头元素，将每个元素移入所属的类。
    # class_sizes[k] 此时为第 k 类的结束位置（不包含该位置），
    # 元素放入所属类的末尾时递减该值。
    def class_of(value: float) -> int:
        return min(int(c1 * (value - min_val)), m - 1)

    moves = 0
    j = 0
    k = m - 1
    while moves < n - 1:
        while j > class_sizes[k] - 1:
            j += 1
            k = class_of(result[j])
        flash = result[j]
        while j != class_sizes[k]:
            k = class_of(flash)
            class_sizes[k] -= 1
            result[class_sizes[k]], flash = flash, result[class_sizes[k]]
            moves += 1

    # 使用插入排序完成类内的最终排序
    for i in range(1, n):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key

    return result


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    # 额外测试用例
    test_cases: list[list[int | float]] = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [1],
        [],
        [3, 3, 3, 3],
        [-1, -3, 2, 0, -5],
        [1.1, 2.2, 0.5, 3.3, 1.5],
    ]

    for test_case in test_cases:
        sorted_result = flash_sort(test_case)
        expected = sorted(test_case)
        assert sorted_result == expected, f"Failed for {test_case}"
        print(f"✓ {test_case} -> {sorted_result}")

    print("All tests passed!")
