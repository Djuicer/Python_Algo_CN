"""
给定包含 n 个正整数的数组 nums。

可以对数组中的任意元素执行以下两种操作，
次数不限：

若元素为偶数，则将其除以 2。
例如，数组为 [1,2,3,4] 时，可以对
最后一个元素执行此操作，得到 [1,2,3,2]。
若元素为奇数，则将其乘以 2。
例如，数组为 [1,2,3,4] 时，可以对
第一个元素执行此操作，得到 [2,2,3,4]。
数组的偏差是任意两个元素之间
差值的最大值。

返回执行若干次操作后
数组可以达到的最小偏差。
"""

from heapq import heapify, heappop, heappush


class Solution:
    def minimum_deviation(self, nums: list[int]) -> int:
        """
        求执行操作后数组的最小偏差。

        参数：
            nums (List[int])：正整数列表。

        返回：
            temp_mindeviation (int)：操作后数组的最小偏差。

        示例：
            >>> solution = Solution()
            >>> solution.minimum_deviation([1, 2, 3, 4])
            1
            >>> solution.minimum_deviation([5, 10, 20, 30, 30])
            5
            >>> solution.minimum_deviation([8, 8, 8, 8, 8])
            0
        """
        heapque = [-n * 2 if n % 2 else -n for n in nums]
        heapify(heapque)
        temp_min = -min(heapque, key=lambda num: -num)
        temp_mindeviation = -heapque[0] - temp_min

        while heapque and heapque[0] % 2 == 0:
            n = heappop(heapque) // 2
            heappush(heapque, n)
            temp_min = min(temp_min, -n)
            temp_mindeviation = min(temp_mindeviation, -heapque[0] - temp_min)

        return temp_mindeviation


if __name__ == "__main__":
    import doctest

    doctest.testmod()
