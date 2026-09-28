"""
https://www.enjoyalgorithms.com/blog/median-of-two-sorted-arrays
"""


def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    """
    查找 中位数 的 两个 数组。

    参数：
        nums1: 第一个 数组。
        nums2: 第二个 数组。

    返回值：
    中位数 的 两个 数组。

    示例：
        >>> find_median_sorted_arrays([1, 3], [2])
        2.0

        >>> find_median_sorted_arrays([1, 2], [3, 4])
        2.5

        >>> find_median_sorted_arrays([0, 0], [0, 0])
        0.0

        >>> find_median_sorted_arrays([], [])
        Traceback (most recent call last):
            ...
        ValueError: Both input arrays are empty.

        >>> find_median_sorted_arrays([], [1])
        1.0

        >>> find_median_sorted_arrays([-1000], [1000])
        0.0

        >>> find_median_sorted_arrays([-1.1, -2.2], [-3.3, -4.4])
        -2.75
    """
    if not nums1 and not nums2:
        raise ValueError("Both input arrays are empty.")

    # 合并 数组 到 single 有序数组。
    merged = sorted(nums1 + nums2)
    total = len(merged)

    if total % 2 == 1:  # 如果 total 元素数量 是 奇数
        return float(merged[total // 2])  # 则 返回 中间元素

    # 如果 total 元素数量 是 偶数，计算
    # 平均值 的 两个 middle 元素 作为 中位数。
    middle1 = merged[total // 2 - 1]
    middle2 = merged[total // 2]
    return (float(middle1) + float(middle2)) / 2.0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
