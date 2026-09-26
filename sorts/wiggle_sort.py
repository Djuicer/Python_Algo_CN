"""
摆动排序（Wiggle Sort）。

给定无序数组 nums，重新排列，使其满足
nums[0] < nums[1] > nums[2] < nums[3]....
例如：
输入 numbers = [3, 5, 2, 1, 6, 4] 时，
一种可能的摆动排序结果为 [3, 5, 1, 6, 2, 4]。
"""


def wiggle_sort(nums: list) -> list:
    """
    摆动排序的 Python 实现。
    重新排列数组，使 nums[0] <= nums[1] >= nums[2] <= nums[3]...

    示例：
    >>> wiggle_sort([0, 5, 3, 2, 2])
    [0, 5, 2, 3, 2]
    >>> wiggle_sort([])
    []
    >>> wiggle_sort([-2, -5, -45])
    [-5, -2, -45]
    >>> wiggle_sort([-2.1, -5.68, -45.11])
    [-5.68, -2.1, -45.11]
    """
    for i in range(1, len(nums)):
        if (i % 2 == 1 and nums[i - 1] > nums[i]) or (
            i % 2 == 0 and nums[i - 1] < nums[i]
        ):
            nums[i - 1], nums[i] = nums[i], nums[i - 1]

    return nums


if __name__ == "__main__":
    print("Enter the array elements:")
    array = list(map(int, input().split()))
    print("The unsorted array is:")
    print(array)
    print("Array after Wiggle sort:")
    print(wiggle_sort(array))
