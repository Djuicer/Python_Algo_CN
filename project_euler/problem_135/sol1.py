"""
Project Euler Problem 135: https://projecteuler.net/problem=135

给定正整数 x、y 和 z，它们是等差数列的连续项。使方程
x2 - y2 - z2 = n 恰有两个解的最小正整数 n 为 n = 27：

342 - 272 - 202 = 122 - 92 - 62 = 27

事实证明，n = 1155 是恰有十个解的最小值。

小于一百万且恰有十个不同解的 n 有多少个？


令 x、y、z 分别采用 a + d、a、a - d 的形式，给定方程可化简为
a * (4d - a) = n。
固定 a，计算不超过 1 million（一百万）的每个 n 的解数，且 n 必须是 a 的倍数。
总步数 = n * (1/1 + 1/2 + 1/3 + 1/4 + ... + 1/n)，因此时间复杂度约为 O(nlogn)。
"""


def solution(limit: int = 1000000) -> int:
    """
    返回小于或等于 limit 且恰有十个不同解的 n 的数量。
    >>> solution(100)
    0
    >>> solution(10000)
    45
    >>> solution(50050)
    292
    """
    limit = limit + 1
    frequency = [0] * limit
    for first_term in range(1, limit):
        for n in range(first_term, limit, first_term):
            common_difference = first_term + n / first_term
            if common_difference % 4:  # d 必须能被 4 整除
                continue
            common_difference /= 4
            if (
                first_term > common_difference and first_term < 4 * common_difference
            ):  # 因为 x、y、z 是正整数
                frequency[n] += 1  # 因此 z > 0、a > d 且 4d < a

    count = sum(1 for x in frequency[1:limit] if x == 10)

    return count


if __name__ == "__main__":
    print(f"{solution() = }")
