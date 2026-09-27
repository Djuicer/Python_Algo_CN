"""
Problem 72 Counting fractions: https://projecteuler.net/problem=72

说明：

考虑分数 n/d，其中 n 和 d 为正整数。如果 n<d 且 HCF(n,d)=1，则称其为最简真分数。
如果按大小升序列出 d ≤ 8 的最简真分数集合，可得：
1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7,
3/4, 4/5, 5/6, 6/7, 7/8
可以看出，该集合包含 21 个元素。d ≤ 1,000,000 的最简真分数集合包含多少个元素？

解法：

1 到 n 之间与 n 互素的数的数量由 Euler 欧拉函数 phi(n) 给出。因此答案就是
2 <= n <= 1,000,000 时 phi(n) 的总和。对所有 d|n，phi(d) 之和 = n。
可利用该结果通过筛法求 phi(n)。

用时：1 秒
"""

import numpy as np


def solution(limit: int = 1_000_000) -> int:
    """
    返回整数形式的问题解。
    >>> solution(10)
    31
    >>> solution(100)
    3043
    >>> solution(1_000)
    304191
    """

    # generating an array from -1 to limit
    phi = np.arange(-1, limit)

    for i in range(2, limit + 1):
        if phi[i] == i - 1:
            ind = np.arange(2 * i, limit + 1, i)  # indexes for selection
            phi[ind] -= phi[ind] // i

    return int(np.sum(phi[2 : limit + 1]))


if __name__ == "__main__":
    print(solution())
