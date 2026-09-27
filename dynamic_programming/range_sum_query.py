"""
Author: Sanjay Muthu <https://github.com/XenoBytesX>

这是区间和查询的动态规划（Dynamic Programming）解法实现。

问题描述如下：
    给定一个数组和 q 个查询，每个查询要求计算从 l 到 r（含）的元素之和。

示例：
    arr = [1, 4, 6, 2, 61, 12]
    queries = 3
    l_1 = 2, r_1 = 5
    l_2 = 1, r_2 = 5
    l_3 = 3, r_3 = 4

    作为输入将返回

    [81, 85, 63]

    作为输出

0-索引：
注意：0-索引表示数组索引从 0 开始。
示例：a = [1, 2, 3, 4, 5, 6]
      这里，a 的第 0 个索引处是 1，
            第 1 个索引处是 2，依此类推。

时间复杂度：O(N + Q)
* 计算前缀和数组需要 O(N) 的预计算时间
* 每个查询需要 O(1) 时间，即 O(1 * Q) = O(Q) 时间

空间复杂度：O(N)
* 使用 O(N) 空间存储前缀和

算法：
首先计算数组的前缀和 (dp)。索引 i 处的前缀和是索引从 0 到 i（含）的所有元素之和。
索引 i 处的前缀和等于索引 (i - 1) 处的前缀和加上当前元素。
因此，dp 的状态为 dp[i] = dp[i - 1] + a[i]。

计算前缀和后，对于每个查询 [l, r]，答案为 dp[r] - dp[l - 1]
（需要注意 l 可能为 0）。例如，取以下数组：
    [4, 2, 1, 6, 3]
为此数组计算出的前缀和为：
    [4, 4 + 2, 4 + 2 + 1, 4 + 2 + 1 + 6, 4 + 2 + 1 + 6 + 3]
    ==> [4, 6, 7, 13, 16]
If the query was l = 3, r = 4,
the answer would be 6 + 3 = 9 but this would require O(r - l + 1) time ≈ O(N) time

如果使用前缀和，则可以通过公式 prefix[r] - prefix[l - 1] 在 O(1) 时间内求出答案。
该公式成立是因为 prefix[r] 是 [0, r] 中的元素之和，
而 prefix[l - 1] 是 [0, l - 1] 中的元素之和，
所以 prefix[r] - prefix[l - 1] 为
[0, r] - [0, l - 1] = [0, l - 1] + [l, r] - [0, l - 1] = [l, r]
"""


def prefix_sum(array: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """
    >>> prefix_sum([1, 4, 6, 2, 61, 12], [(2, 5), (1, 5), (3, 4)])
    [81, 85, 63]
    >>> prefix_sum([4, 2, 1, 6, 3], [(3, 4), (1, 3), (0, 2)])
    [9, 9, 7]
    """
    # 前缀和数组
    dp = [0] * len(array)
    dp[0] = array[0]
    for i in range(1, len(array)):
        dp[i] = dp[i - 1] + array[i]

    # 参见算法部分（Line 44）
    result = []
    for query in queries:
        left, right = query
        res = dp[right]
        if left > 0:
            res -= dp[left - 1]
        result.append(res)

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
