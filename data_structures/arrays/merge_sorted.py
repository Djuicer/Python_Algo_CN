def merge_sorted_arrays(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    合并两个 已排序 数组 到 一个 有序数组。

    参数：
        nums1: 第一个 有序数组。
        nums2: 第二个 有序数组。

    返回值：
        single 合并后 并且 有序数组。

    示例：
        >>> merge_sorted_arrays([1, 3, 5], [2, 4, 6])
        [1, 2, 3, 4, 5, 6]

        >>> merge_sorted_arrays([1, 2], [])
        [1, 2]

        >>> merge_sorted_arrays([], [3, 4])
        [3, 4]

        >>> merge_sorted_arrays([], [])
        []

        >>> merge_sorted_arrays([0, 0], [0, 0])
        [0, 0, 0, 0]

        >>> merge_sorted_arrays([-5, -3, -1], [-2, -2])
        [-5, -3, -2, -2, -1]

        >>> merge_sorted_arrays(range(5), range(5))
        [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]

        >>> merge_sorted_arrays([1, -1], [])
        Traceback (most recent call last):
            ...
        ValueError: nums = [1, -1] is not sorted

        >>> merge_sorted_arrays([], [1, -1])
        Traceback (most recent call last):
            ...
        ValueError: nums = [1, -1] is not sorted
    """
    for nums in (nums1, nums2):
        if list(nums) != sorted(nums):
            msg = f"{nums = } is not sorted"
            raise ValueError(msg)
    # 如果 一个 数组 为空，simply 返回 另一个。
    if not nums1:
        return nums2
    if not nums2:
        return nums1

    # 双指针方法 到 合并 两者 已排序 数组。
    i, j = 0, 0
    merged = []

    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1

    # 追加 剩余 元素 如果 任意。
    merged.extend(nums1[i:])
    merged.extend(nums2[j:])

    return merged


if __name__ == "__main__":
    import doctest

    doctest.testmod()
