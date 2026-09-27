"""
Project Euler Problem 190: https://projecteuler.net/problem=190

最大化加权乘积

令 S_m = (x_1, x_2, ..., x_m) 为满足 x_1 + x_2 + ... + x_m = m，且使
P_m = x_1 * x_2^2 * ... * x_m^m 最大的正实数 m 元组。

例如，可以验证 |_ P_10 _| = 4112（|_ _| 为取整数部分函数）。

求 Sum_{m=2}^15 = |_ P_m _|。

解法：
- 固定 x_1 = m - x_2 - ... - x_m。
- 计算 P_m 关于 x_2, ..., x_m 的偏导数，可得
  x_2 = 2 * x_1, x_3 = 3 * x_1, ..., x_m = m * x_1.
- 计算 P_m 关于 x_2, ..., x_m 的二阶偏导数。代入上一步的值，可以验证该解为最大值。
"""


def solution(n: int = 15) -> int:
    """
    计算 m 从 2 到 n 时 |_ P_m _| 的总和。

    >>> solution(2)
    1
    >>> solution(3)
    2
    >>> solution(4)
    4
    >>> solution(5)
    10
    """
    total = 0
    for m in range(2, n + 1):
        x1 = 2 / (m + 1)
        p = 1.0
        for i in range(1, m + 1):
            xi = i * x1
            p *= xi**i
        total += int(p)
    return total


if __name__ == "__main__":
    print(f"{solution() = }")
