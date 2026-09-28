# https://leetcode.com/problems/monotonic-array/
def is_monotonic(nums: list[int]) -> bool:
    """
    检查是否 一个列表 是 monotonic。

    >>> is_monotonic([1, 2, 2, 3])
    True
    >>> is_monotonic([6, 5, 4, 4])
    True
    >>> is_monotonic([1, 3, 2])
    False
    >>> is_monotonic([1,2,3,4,5,6,5])
    False
    >>> is_monotonic([-3,-2,-1])
    True
    >>> is_monotonic([-5,-6,-7])
    True
    >>> is_monotonic([0,0,0])
    True
    >>> is_monotonic([-100,0,100])
    True
    """
    return all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)) or all(
        nums[i] >= nums[i + 1] for i in range(len(nums) - 1)
    )


# 测试 函数 带有 your 示例
if __name__ == "__main__":
    # 测试 函数 带有 your 示例
    print(is_monotonic([1, 2, 2, 3]))  # 输出: True
    print(is_monotonic([6, 5, 4, 4]))  # 输出: True
    print(is_monotonic([1, 3, 2]))  # 输出: False

    import doctest

    doctest.testmod()
