"""
Author  : Alexander Pantyukhin
Date    : November 3, 2022

Implement 类 的 前缀 和 带有 useful 函数 基于 在 它。

"""


class PrefixSum:
    def __init__(self, array: list[int]) -> None:
        len_array = len(array)
        self.prefix_sum = [0] * len_array

        if len_array > 0:
            self.prefix_sum[0] = array[0]

        for i in range(1, len_array):
            self.prefix_sum[i] = self.prefix_sum[i - 1] + array[i]

    def get_sum(self, start: int, end: int) -> int:
        """
        该函数返回 和 的 数组 从 开始 到 末尾 indexes。
        运行时间 : O(1)
        空间: O(1)

        >>> PrefixSum([1,2,3]).get_sum(0, 2)
        6
        >>> PrefixSum([1,2,3]).get_sum(1, 2)
        5
        >>> PrefixSum([1,2,3]).get_sum(2, 2)
        3
        >>> PrefixSum([]).get_sum(0, 0)
        Traceback (most recent call last):
        ...
        ValueError: The array is empty.
        >>> PrefixSum([1,2,3]).get_sum(-1, 2)
        Traceback (most recent call last):
        ...
        ValueError: Invalid range specified.
        >>> PrefixSum([1,2,3]).get_sum(2, 3)
        Traceback (most recent call last):
        ...
        ValueError: Invalid range specified.
        >>> PrefixSum([1,2,3]).get_sum(2, 1)
        Traceback (most recent call last):
        ...
        ValueError: Invalid range specified.
        """
        if not self.prefix_sum:
            raise ValueError("The array is empty.")

        if start < 0 or end >= len(self.prefix_sum) or start > end:
            raise ValueError("Invalid range specified.")

        if start == 0:
            return self.prefix_sum[end]

        return self.prefix_sum[end] - self.prefix_sum[start - 1]

    def contains_sum(self, target_sum: int) -> bool:
        """
        该函数返回 True 如果 数组 包含 target_sum,
        False 否则。

        运行时间 : O(n)
        空间: O(n)

        >>> PrefixSum([1,2,3]).contains_sum(6)
        True
        >>> PrefixSum([1,2,3]).contains_sum(5)
        True
        >>> PrefixSum([1,2,3]).contains_sum(3)
        True
        >>> PrefixSum([1,2,3]).contains_sum(4)
        False
        >>> PrefixSum([1,2,3]).contains_sum(7)
        False
        >>> PrefixSum([1,-2,3]).contains_sum(2)
        True
        """

        sums = {0}
        for sum_item in self.prefix_sum:
            if sum_item - target_sum in sums:
                return True

            sums.add(sum_item)

        return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
